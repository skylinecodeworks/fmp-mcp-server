"""Tests for FMP client."""

from unittest.mock import MagicMock, patch

import pytest

from fmp_mcp_server.client import FMPClient


class TestFMPClient:
    """Test FMP client functionality."""

    def test_init_requires_api_key(self):
        """Test that API key is required."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="FMP API key is required"):
                FMPClient()

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = FMPClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://financialmodelingprep.com/api/v3"

    @pytest.mark.asyncio
    async def test_request_adds_api_key(self):
        """Test that API key is added to requests."""
        client = FMPClient(api_key="test_key")

        with patch.object(client.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"test": "data"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = await client._request("test-endpoint")

            mock_get.assert_called_once_with(
                "https://financialmodelingprep.com/api/v3/test-endpoint",
                params={"apikey": "test_key"},
            )
            assert result == {"test": "data"}

    @pytest.mark.asyncio
    async def test_get_company_profile(self):
        """Test get company profile."""
        client = FMPClient(api_key="test_key")

        with patch.object(client, "_request") as mock_request:
            mock_request.return_value = {"symbol": "AAPL"}

            result = await client.get_company_profile("AAPL")

            mock_request.assert_called_once_with("profile/AAPL")
            assert result == [{"symbol": "AAPL"}]
