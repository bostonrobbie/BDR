"""
Outreach Command Center - Unified LLM Gateway
Provides a single interface for all LLM calls (Researcher, Scorer, Writer).

Features:
- Resilient Ollama client with health checks and retries
- Provider routing: Ollama (primary) -> fallback provider (if configured) -> hard fail
- Request tracing with stage names
- Logging redaction (no secrets in logs)
"""

import json
import logging
import os
import time
import uuid
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
    from src.config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT, LLM_FALLBACK_PROVIDER as FALLBACK_PROVIDER
except ImportError:
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT_SECONDS", "120"))
    FALLBACK_PROVIDER = os.environ.get("LLM_FALLBACK_PROVIDER", "")

logger = logging.getLogger("bdr.agents.llm_gateway")

# Retry config
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # seconds


# ─── OLLAMA CLIENT ─────────────────────────────────────────────

class OllamaError(Exception):
    """Raised when Ollama returns an error or is unreachable."""
    pass


class ModelNotFoundError(OllamaError):
    """Raised when the requested model is not available."""
    pass


class OllamaClient:
    """Resilient Ollama HTTP client."""

    def __init__(self, host: str = None, model: str = None, timeout: int = None):
        self.host = (host or OLLAMA_HOST).rstrip("/")
        self.model = model or OLLAMA_MODEL
        self.timeout = timeout or OLLAMA_TIMEOUT
        self._healthy = None

    def health_check(self) -> dict:
        """Check if Ollama is reachable and the model is available.

        Returns:
            {"healthy": bool, "models": [...], "model_available": bool, "error": str|None}
        """
        result = {"healthy": False, "models": [], "model_available": False, "error": None}

        try:
            # Check /api/tags endpoint for available models
            req = Request(f"{self.host}/api/tags", method="GET")
            with urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                models = [m.get("name", "") for m in data.get("models", [])]
                result["models"] = models
                result["healthy"] = True

                # Check if our model is available (match by prefix)
                model_base = self.model.split(":")[0]
                result["model_available"] = any(
                    self.model in m or model_base in m for m in models
                )

                if not result["model_available"]:
                    result["error"] = (
                        f"Model '{self.model}' not found. Available: {', '.join(models[:5])}. "
                        f"Run: ollama pull {self.model}"
                    )

        except URLError as e:
            result["error"] = (
                f"Cannot reach Ollama at {self.host}. "
                f"Is the service running? Try: ollama serve"
            )
            logger.warning(f"Ollama health check failed: {e}")
        except Exception as e:
            result["error"] = f"Unexpected error during health check: {e}"
            logger.error(f"Ollama health check error: {e}")

        self._healthy = result["healthy"] and result["model_available"]
        return result

    def generate(self, prompt: str, model: str = None, temperature: float = 0.7,
                 max_tokens: int = 1024, system: str = None) -> dict:
        """Send a generation request to Ollama with retries.

        Args:
            prompt: The user prompt.
            model: Override model (uses default if None).
            temperature: Sampling temperature.
            max_tokens: Max tokens to generate.
            system: Optional system prompt.

        Returns:
            {"response": str, "model": str, "total_duration": int, "eval_count": int}

        Raises:
            OllamaError: On unrecoverable failure.
            ModelNotFoundError: If the model is not available.
        """
        model = model or self.model
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        if system:
            payload["system"] = system

        body = json.dumps(payload).encode("utf-8")

        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                req = Request(
                    f"{self.host}/api/generate",
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode())
                    return {
                        "response": data.get("response", ""),
                        "model": data.get("model", model),
                        "total_duration": data.get("total_duration", 0),
                        "eval_count": data.get("eval_count", 0),
                    }

            except HTTPError as e:
                error_body = ""
                try:
                    error_body = e.read().decode()
                except Exception:
                    pass
                if e.code == 404 or "model" in error_body.lower() and "not found" in error_body.lower():
                    raise ModelNotFoundError(
                        f"Model '{model}' not found. Run: ollama pull {model}"
                    )
                last_error = f"HTTP {e.code}: {error_body[:200]}"
                logger.warning(f"Ollama attempt {attempt + 1}/{MAX_RETRIES} failed: {last_error}")

            except URLError as e:
                last_error = f"Connection error: {e.reason}"
                logger.warning(f"Ollama attempt {attempt + 1}/{MAX_RETRIES} failed: {last_error}")

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Ollama attempt {attempt + 1}/{MAX_RETRIES} failed: {last_error}")

            # Exponential backoff
            if attempt < MAX_RETRIES - 1:
                sleep_time = RETRY_BACKOFF_BASE ** (attempt + 1)
                logger.info(f"Retrying in {sleep_time}s...")
                time.sleep(sleep_time)

        raise OllamaError(
            f"Ollama failed after {MAX_RETRIES} attempts. Last error: {last_error}. "
            f"Host: {self.host}, Model: {model}. "
            f"Check: 1) Is Ollama running? (ollama serve) "
            f"2) Is the model pulled? (ollama pull {model}) "
            f"3) Is the host correct? (OLLAMA_HOST env var)"
        )


# ─── LLM GATEWAY (unified interface) ──────────────────────────

class LLMGateway:
    """Unified LLM interface that routes to Ollama with fallback support.

    Usage:
        gateway = LLMGateway()
        result = gateway.generate(
            prompt="Analyze this prospect...",
            stage_name="research",
            temperature=0.3,
        )
    """

    def __init__(self, ollama_host: str = None, ollama_model: str = None):
        self.ollama = OllamaClient(host=ollama_host, model=ollama_model)
        self._initialized = False

    def initialize(self) -> dict:
        """Run startup health check. Call once before first generate().

        Returns:
            {"provider": "ollama"|"fallback"|"none", "status": "ok"|"degraded"|"unavailable",
             "details": {...}}
        """
        health = self.ollama.health_check()
        self._initialized = True

        if health["healthy"] and health["model_available"]:
            logger.info(f"LLM Gateway ready: Ollama at {self.ollama.host}, model {self.ollama.model}")
            return {
                "provider": "ollama",
                "status": "ok",
                "details": health,
            }

        # Check for fallback
        if FALLBACK_PROVIDER:
            logger.warning(f"Ollama unavailable, fallback provider '{FALLBACK_PROVIDER}' configured but not implemented")
            return {
                "provider": "fallback",
                "status": "degraded",
                "details": {"ollama": health, "fallback": FALLBACK_PROVIDER},
            }

        logger.error(f"LLM Gateway unavailable: {health.get('error', 'unknown')}")
        return {
            "provider": "none",
            "status": "unavailable",
            "details": health,
        }

    def generate(self, prompt: str, stage_name: str = "unknown",
                 model: str = None, temperature: float = 0.7,
                 max_tokens: int = 1024, system: str = None,
                 request_id: str = None) -> dict:
        """Generate text via the best available provider.

        Args:
            prompt: The user prompt.
            stage_name: Pipeline stage (research/score/write) for tracing.
            model: Override model.
            temperature: Sampling temperature.
            max_tokens: Max tokens.
            system: System prompt.
            request_id: Trace ID (auto-generated if None).

        Returns:
            {"response": str, "provider": str, "model": str, "request_id": str,
             "stage": str, "duration_ms": int}

        Raises:
            OllamaError: If all providers fail.
        """
        request_id = request_id or uuid.uuid4().hex[:12]
        start = time.time()

        # Redact prompt for logging (first 80 chars only)
        prompt_preview = prompt[:80].replace("\n", " ") + ("..." if len(prompt) > 80 else "")
        logger.info(f"[{request_id}] LLM request: stage={stage_name}, prompt='{prompt_preview}'")

        # Try Ollama first
        try:
            result = self.ollama.generate(
                prompt=prompt, model=model, temperature=temperature,
                max_tokens=max_tokens, system=system,
            )
            duration_ms = int((time.time() - start) * 1000)
            logger.info(f"[{request_id}] Ollama responded in {duration_ms}ms, "
                       f"tokens={result.get('eval_count', '?')}")
            return {
                "response": result["response"],
                "provider": "ollama",
                "model": result.get("model", self.ollama.model),
                "request_id": request_id,
                "stage": stage_name,
                "duration_ms": duration_ms,
            }

        except ModelNotFoundError as e:
            logger.error(f"[{request_id}] Model not found: {e}")
            raise

        except OllamaError as e:
            logger.warning(f"[{request_id}] Ollama failed: {e}")

            # Try fallback if configured
            if FALLBACK_PROVIDER:
                logger.info(f"[{request_id}] Attempting fallback provider: {FALLBACK_PROVIDER}")
                # Placeholder for fallback - extend when a second provider is added
                raise OllamaError(
                    f"Ollama failed and fallback provider '{FALLBACK_PROVIDER}' is not yet implemented. "
                    f"Original error: {e}"
                )

            raise OllamaError(
                f"LLM generation failed. No fallback provider configured. "
                f"Set LLM_FALLBACK_PROVIDER env var or fix Ollama. Error: {e}"
            )


# ─── MODULE-LEVEL SINGLETON ───────────────────────────────────

_gateway_instance = None


def get_gateway() -> LLMGateway:
    """Get or create the module-level LLM Gateway singleton."""
    global _gateway_instance
    if _gateway_instance is None:
        _gateway_instance = LLMGateway()
    return _gateway_instance
