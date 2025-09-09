"""MCP server for Financial Modelling Prep API using FastMCP."""

from typing import Literal, Optional

from mcp.server.fastmcp import FastMCP

from .client import FMPClient

# Initialize FastMCP server
mcp = FastMCP(
    "fmp",
    instructions="A server that provides tools to access the Financial Modelling Prep API."
)

# Global FMPClient instance, initialized on first use
fmp_client: Optional[FMPClient] = None


async def get_client() -> FMPClient:
    """Get or create the FMPClient instance."""
    global fmp_client
    if fmp_client is None:
        fmp_client = FMPClient()
    return fmp_client


@mcp.tool()
async def get_company_profile(symbol: str) -> list[dict]:
    """
    Get comprehensive company profile information including business description,
    sector, industry, and key metrics.
    """
    client = await get_client()
    return await client.get_company_profile(symbol)


@mcp.tool()
async def get_stock_quote(symbol: str) -> list[dict]:
    """
    Get real-time stock quote with current price, volume, and market data.
    """
    client = await get_client()
    return await client.get_quote(symbol)


@mcp.tool()
async def get_financial_statements(
    symbol: str,
    statement_type: Literal["income", "balance", "cashflow"],
    period: Literal["annual", "quarter"] = "annual",
    limit: int = 5,
) -> list[dict]:
    """
    Get financial statements (income statement, balance sheet, cash flow) for a company.
    """
    client = await get_client()
    if statement_type == "income":
        return await client.get_income_statement(symbol, period, limit)
    if statement_type == "balance":
        return await client.get_balance_sheet(symbol, period, limit)
    if statement_type == "cashflow":
        return await client.get_cash_flow(symbol, period, limit)
    # This part should not be reached due to Literal type hint validation
    raise ValueError(f"Invalid statement type: {statement_type}")


@mcp.tool()
async def get_key_metrics(
    symbol: str,
    period: Literal["annual", "quarter"] = "annual",
    limit: int = 5,
) -> list[dict]:
    """
    Get key financial metrics and ratios for fundamental analysis.
    """
    client = await get_client()
    return await client.get_key_metrics(symbol, period, limit)


@mcp.tool()
async def get_financial_ratios(
    symbol: str,
    period: Literal["annual", "quarter"] = "annual",
    limit: int = 5,
) -> list[dict]:
    """
    Get comprehensive financial ratios for valuation and analysis.
    """
    client = await get_client()
    return await client.get_financial_ratios(symbol, period, limit)


@mcp.tool()
async def get_dcf_valuation(symbol: str) -> list[dict]:
    """
    Get discounted cash flow valuation analysis.
    """
    client = await get_client()
    return await client.get_dcf_valuation(symbol)


@mcp.tool()
async def search_companies(query: str, limit: int = 10) -> list[dict]:
    """
    Search for companies by name or symbol.
    """
    client = await get_client()
    return await client.search_companies(query, limit)


@mcp.tool()
async def get_sector_performance() -> list[dict]:
    """
    Get sector performance overview.
    """
    client = await get_client()
    return await client.get_sector_performance()


if __name__ == "__main__":
    # For stdio transport, FastMCP handles the lifecycle.
    # The server runs until the client disconnects.
    # Cleanup of the FMPClient is not explicitly handled here,
    # as the process will terminate. For persistent servers (e.g., SSE),
    # a more graceful shutdown hook for client.close() would be needed.
    mcp.run()
