"""Tests for the memory layer loader module."""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.memory.loader import MemoryLoader


@pytest.fixture
def loader():
    """Create a MemoryLoader pointing to the real memory directory."""
    memory_root = os.path.join(os.path.dirname(__file__), "../../memory")
    return MemoryLoader(memory_root=memory_root)


class TestToolResolution:
    def test_direct_name(self, loader):
        assert loader.resolve_tool_name("selenium") == "selenium"

    def test_alias(self, loader):
        assert loader.resolve_tool_name("webdriver") == "selenium"

    def test_alias_tricentis(self, loader):
        assert loader.resolve_tool_name("tricentis") == "tosca"

    def test_alias_qtp(self, loader):
        assert loader.resolve_tool_name("qtp") == "uft"

    def test_case_insensitive(self, loader):
        assert loader.resolve_tool_name("Selenium") == "selenium"
        assert loader.resolve_tool_name("CYPRESS") == "cypress"

    def test_unknown_tool(self, loader):
        assert loader.resolve_tool_name("unknown_tool_xyz") is None


class TestBattleCards:
    def test_load_selenium(self, loader):
        card = loader.get_battle_card("selenium")
        assert card is not None
        assert card["tool"] == "selenium"
        assert card["threat_level"] == "high"
        assert "sections" in card
        assert len(card["sections"]) > 0

    def test_load_via_alias(self, loader):
        card = loader.get_battle_card("webdriver")
        assert card is not None
        assert card["tool"] == "selenium"

    def test_load_all_cards(self, loader):
        tools = ["selenium", "cypress", "playwright", "katalon", "tosca", "mabl", "testim", "uft"]
        for tool in tools:
            card = loader.get_battle_card(tool)
            assert card is not None, f"Battle card missing for {tool}"
            assert card["tool"] == tool
            assert "sections" in card

    def test_unknown_card(self, loader):
        card = loader.get_battle_card("nonexistent_tool")
        assert card is None

    def test_card_caching(self, loader):
        card1 = loader.get_battle_card("selenium")
        card2 = loader.get_battle_card("selenium")
        assert card1 is card2  # Same object (cached)


class TestDisplacementAngles:
    def test_selenium_angles(self, loader):
        angles = loader.get_displacement_angles("selenium")
        assert len(angles) > 0
        for a in angles:
            assert "weakness" in a
            assert "testsigma_angle" in a

    def test_all_tools_have_angles(self, loader):
        tools = ["selenium", "cypress", "playwright", "katalon", "tosca", "mabl", "testim", "uft"]
        for tool in tools:
            angles = loader.get_displacement_angles(tool)
            assert len(angles) > 0, f"No displacement angles for {tool}"


class TestObjectionResponses:
    def test_selenium_objection(self, loader):
        obj = loader.get_objection_response("selenium")
        assert obj is not None
        assert "objection" in obj
        assert "response" in obj

    def test_objection_matching(self, loader):
        obj = loader.get_objection_response("selenium", "Our team knows Selenium, we've invested years")
        assert obj is not None
        assert "response" in obj

    def test_all_tools_have_objections(self, loader):
        tools = ["selenium", "cypress", "playwright", "katalon", "tosca", "mabl", "testim", "uft"]
        for tool in tools:
            obj = loader.get_objection_response(tool)
            assert obj is not None, f"No objection response for {tool}"


class TestTalkTracks:
    def test_selenium_talk_track(self, loader):
        track = loader.get_talk_track("selenium")
        assert track is not None
        assert len(track) > 50  # Should be substantive

    def test_all_tools_have_talk_tracks(self, loader):
        tools = ["selenium", "cypress", "playwright", "katalon", "tosca", "mabl", "testim", "uft"]
        for tool in tools:
            track = loader.get_talk_track(tool)
            assert track is not None, f"No talk track for {tool}"


class TestProspectContext:
    def test_with_known_tools(self, loader):
        ctx = loader.get_prospect_context(known_tools=["selenium", "cypress"])
        assert len(ctx["battle_cards"]) == 2
        assert len(ctx["displacement_angles"]) > 0
        assert len(ctx["objection_responses"]) == 2

    def test_with_unknown_tools(self, loader):
        ctx = loader.get_prospect_context(known_tools=["random_tool"])
        assert len(ctx["battle_cards"]) == 0

    def test_empty_context(self, loader):
        ctx = loader.get_prospect_context()
        assert ctx["battle_cards"] == []
        assert ctx["displacement_angles"] == []


class TestWinLossPatterns:
    def test_win_patterns_empty(self, loader):
        """With no win reports, should return empty pattern dict."""
        patterns = loader.get_win_patterns()
        assert "note" in patterns or "total_wins" in patterns

    def test_get_wins(self, loader):
        wins = loader.get_wins()
        assert isinstance(wins, list)
        # Template files should be excluded
        for w in wins:
            assert not w["filename"].startswith("_")

    def test_get_losses(self, loader):
        losses = loader.get_losses()
        assert isinstance(losses, list)


class TestCallNotes:
    def test_get_call_notes(self, loader):
        notes = loader.get_call_notes()
        assert isinstance(notes, list)
        # Template files should be excluded
        for n in notes:
            assert not n["filename"].startswith("_")


class TestMarketIntel:
    def test_get_market_intel(self, loader):
        intel = loader.get_market_intel()
        assert isinstance(intel, dict)
        assert "industry-trends.md" in intel
        assert "analyst-coverage.md" in intel

    def test_get_competitor_moves(self, loader):
        moves = loader.get_competitor_moves()
        assert isinstance(moves, str)
        assert "Tricentis" in moves or "mabl" in moves


class TestPlaybook:
    def test_get_playbook(self, loader):
        playbook = loader.get_playbook()
        assert playbook is not None
        assert "Pain Hook" in playbook
        assert "Proof Point" in playbook
