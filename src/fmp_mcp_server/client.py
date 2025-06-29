"""Financial Modelling Prep API client."""

import os
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv

load_dotenv()


class FMPClient:
    """Client for Financial Modelling Prep API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize FMP client.
        
        Args:
            api_key: FMP API key (defaults to FMP_API_KEY env var)
            base_url: Base URL for API (defaults to FMP_BASE_URL env var)
        """
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        self.base_url = base_url or os.getenv("FMP_BASE_URL", "https://financialmodelingprep.com/api/v3")
        
        if not self.api_key:
            raise ValueError("FMP API key is required")
        
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
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
    
    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile information."""
        return await self._request(f"profile/{symbol}")
    
    async def get_quote(self, symbol: str) -> List[Dict[str, Any]]:
        """Get real-time stock quote."""
        return await self._request(f"quote/{symbol}")
    
    async def get_income_statement(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get income statement data."""
        return await self._request(f"income-statement/{symbol}", {"period": period, "limit": limit})
    
    async def get_balance_sheet(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get balance sheet data."""
        return await self._request(f"balance-sheet-statement/{symbol}", {"period": period, "limit": limit})
    
    async def get_cash_flow(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get cash flow statement data."""
        return await self._request(f"cash-flow-statement/{symbol}", {"period": period, "limit": limit})
    
    async def get_key_metrics(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get key financial metrics."""
        return await self._request(f"key-metrics/{symbol}", {"period": period, "limit": limit})
    
    async def get_financial_ratios(self, symbol: str, period: str = "annual", limit: int = 5) -> List[Dict[str, Any]]:
        """Get financial ratios."""
        return await self._request(f"ratios/{symbol}", {"period": period, "limit": limit})
    
    async def get_dcf_valuation(self, symbol: str) -> List[Dict[str, Any]]:
        """Get DCF valuation."""
        return await self._request(f"discounted-cash-flow/{symbol}")
    
    async def get_financial_score(self, symbol: str) -> List[Dict[str, Any]]:
        """Get financial score."""
        return await self._request(f"score/{symbol}")
    
    async def get_market_cap(self, symbol: str) -> List[Dict[str, Any]]:
        """Get market capitalization."""
        return await self._request(f"market-capitalization/{symbol}")
    
    async def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies."""
        return await self._request("search", {"query": query, "limit": limit})
    
    async def get_sector_performance(self) -> List[Dict[str, Any]]:
        """Get sector performance data."""
        return await self._request("sector-performance")
    
    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()