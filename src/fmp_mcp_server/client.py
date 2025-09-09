"""Financial Modelling Prep API client."""

import os
from typing import Any

import httpx


class FMPClient:
    """Client for Financial Modelling Prep API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        """Initialize FMP client.

        Args:
            api_key: FMP API key (defaults to FMP_API_KEY env var)
            base_url: Base URL for API (defaults to FMP_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        self.base_url = base_url or os.getenv(
            "FMP_BASE_URL",
            "https://financialmodelingprep.com/api/v3",
        )

        if not self.api_key:
            raise ValueError("FMP API key is required")

        self.client = httpx.AsyncClient(timeout=30.0)

    async def _request(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make API request to FMP.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            JSON response data
        """
        if params is None:
            params = {}

        params["apikey"] = self.api_key
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_company_profile(self, symbol: str) -> list[dict[str, Any]]:
        """Get company profile information."""
        result = await self._request(f"profile/{symbol}")
        return result if isinstance(result, list) else [result]

    async def get_quote(self, symbol: str) -> list[dict[str, Any]]:
        """Get real-time stock quote."""
        result = await self._request(f"quote/{symbol}")
        return result if isinstance(result, list) else [result]

    async def get_income_statement(
        self,
        symbol: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get income statement data."""
        result = await self._request(
            f"income-statement/{symbol}",
            {"period": period, "limit": limit},
        )
        return result if isinstance(result, list) else [result]

    async def get_balance_sheet(
        self,
        symbol: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get balance sheet data."""
        result = await self._request(
            f"balance-sheet-statement/{symbol}",
            {"period": period, "limit": limit},
        )
        return result if isinstance(result, list) else [result]

    async def get_cash_flow(
        self,
        symbol: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get cash flow statement data."""
        result = await self._request(
            f"cash-flow-statement/{symbol}",
            {"period": period, "limit": limit},
        )
        return result if isinstance(result, list) else [result]

    async def get_key_metrics(
        self,
        symbol: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get key financial metrics."""
        result = await self._request(
            f"key-metrics/{symbol}",
            {"period": period, "limit": limit},
        )
        return result if isinstance(result, list) else [result]

    async def get_financial_ratios(
        self,
        symbol: str,
        period: str = "annual",
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Get financial ratios."""
        result = await self._request(
            f"ratios/{symbol}",
            {"period": period, "limit": limit},
        )
        return result if isinstance(result, list) else [result]

    async def get_dcf_valuation(self, symbol: str) -> list[dict[str, Any]]:
        """Get DCF valuation."""
        result = await self._request(f"discounted-cash-flow/{symbol}")
        return result if isinstance(result, list) else [result]

    async def get_financial_score(self, symbol: str) -> list[dict[str, Any]]:
        """Get financial score."""
        result = await self._request(f"score/{symbol}")
        return result if isinstance(result, list) else [result]

    async def get_market_cap(self, symbol: str) -> list[dict[str, Any]]:
        """Get market capitalization."""
        result = await self._request(f"market-capitalization/{symbol}")
        return result if isinstance(result, list) else [result]

    async def search_companies(
        self,
        query: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for companies."""
        result = await self._request("search", {"query": query, "limit": limit})
        return result if isinstance(result, list) else [result]

    async def get_sector_performance(self) -> list[dict[str, Any]]:
        """Get sector performance data."""
        result = await self._request("sector-performance")
        return result if isinstance(result, list) else [result]

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()
