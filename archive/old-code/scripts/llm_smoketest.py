#!/usr/bin/env python3
"""
LLM Smoketest - Checks Ollama health and runs a tiny prompt.

Usage:
    python scripts/llm_smoketest.py

Environment variables:
    OLLAMA_HOST (default: http://127.0.0.1:11434)
    OLLAMA_MODEL (default: qwen2.5:7b)

Exit codes:
    0 - OK (Ollama reachable and model responds)
    1 - FAIL (Ollama unreachable or model error)
    2 - DEGRADED (Ollama reachable but model not found)
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.llm_gateway import OllamaClient, OllamaError, ModelNotFoundError


def main():
    print("=" * 50)
    print("LLM SMOKETEST")
    print("=" * 50)

    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    print(f"Host:  {host}")
    print(f"Model: {model}")
    print()

    client = OllamaClient(host=host, model=model)

    # Step 1: Health check
    print("[1/2] Health check...")
    health = client.health_check()

    if not health["healthy"]:
        print(f"  FAIL: {health.get('error', 'Unknown error')}")
        print()
        print("Troubleshooting:")
        print(f"  1. Is Ollama running? Try: ollama serve")
        print(f"  2. Is the host correct? Current: {host}")
        print(f"  3. Set OLLAMA_HOST env var if needed")
        return 1

    print(f"  OK: Ollama reachable")
    print(f"  Models: {', '.join(health['models'][:5])}")

    if not health["model_available"]:
        print(f"  WARN: Model '{model}' not found")
        print(f"  Run: ollama pull {model}")
        return 2

    print(f"  OK: Model '{model}' available")

    # Step 2: Test prompt
    print()
    print("[2/2] Test prompt...")
    start = time.time()
    try:
        result = client.generate(
            prompt="Reply with exactly: OLLAMA_OK",
            temperature=0.0,
            max_tokens=20,
        )
        duration = time.time() - start
        response = result["response"].strip()
        print(f"  Response: {response}")
        print(f"  Model: {result['model']}")
        print(f"  Time: {duration:.1f}s")
        print(f"  Tokens: {result.get('eval_count', '?')}")

        if "OLLAMA_OK" in response.upper():
            print()
            print("OK - LLM is working")
            return 0
        else:
            print()
            print(f"OK - LLM responded (content: '{response[:50]}')")
            return 0

    except ModelNotFoundError as e:
        print(f"  FAIL: {e}")
        return 2
    except OllamaError as e:
        print(f"  FAIL: {e}")
        return 1
    except Exception as e:
        print(f"  FAIL: Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
