"""MCP server for Financial Modelling Prep API."""

import asyncio
import json
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    GetPromptResult,
    ReadResourceResult,
    ListPromptsResult,
    ListResourcesResult,
    ListToolsResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel

from .client import FMPClient


class FMPServer:
    """MCP server for Financial Modelling Prep API."""
    
    def __init__(self):
        """Initialize the FMP MCP server."""
        self.fmp_client: Optional[FMPClient] = None
        self.server = Server("fmp-mcp-server")
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_company_profile",
                        description="Get comprehensive company profile information including business description, sector, industry, and key metrics",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="get_stock_quote",
                        description="Get real-time stock quote with current price, volume, and market data",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="get_financial_statements",
                        description="Get financial statements (income statement, balance sheet, cash flow) for a company",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                },
                                "statement_type": {
                                    "type": "string",
                                    "enum": ["income", "balance", "cashflow"],
                                    "description": "Type of financial statement to retrieve"
                                },
                                "period": {
                                    "type": "string",
                                    "enum": ["annual", "quarter"],
                                    "default": "annual",
                                    "description": "Reporting period"
                                },
                                "limit": {
                                    "type": "integer",
                                    "default": 5,
                                    "description": "Number of periods to retrieve"
                                }
                            },
                            "required": ["symbol", "statement_type"]
                        }
                    ),
                    Tool(
                        name="get_key_metrics",
                        description="Get key financial metrics and ratios for fundamental analysis",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                },
                                "period": {
                                    "type": "string",
                                    "enum": ["annual", "quarter"],
                                    "default": "annual",
                                    "description": "Reporting period"
                                },
                                "limit": {
                                    "type": "integer",
                                    "default": 5,
                                    "description": "Number of periods to retrieve"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="get_financial_ratios",
                        description="Get comprehensive financial ratios for valuation and analysis",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                },
                                "period": {
                                    "type": "string",
                                    "enum": ["annual", "quarter"],
                                    "default": "annual",
                                    "description": "Reporting period"
                                },
                                "limit": {
                                    "type": "integer",
                                    "default": 5,
                                    "description": "Number of periods to retrieve"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="get_dcf_valuation",
                        description="Get discounted cash flow valuation analysis",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "Stock ticker symbol (e.g., AAPL, TSLA)"
                                }
                            },
                            "required": ["symbol"]
                        }
                    ),
                    Tool(
                        name="search_companies",
                        description="Search for companies by name or symbol",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query (company name or symbol)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "default": 10,
                                    "description": "Maximum number of results"
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    Tool(
                        name="get_sector_performance",
                        description="Get sector performance overview",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "additionalProperties": False
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            if not self.fmp_client:
                self.fmp_client = FMPClient()
            
            try:
                if name == "get_company_profile":
                    result = await self.fmp_client.get_company_profile(arguments["symbol"])
                elif name == "get_stock_quote":
                    result = await self.fmp_client.get_quote(arguments["symbol"])
                elif name == "get_financial_statements":
                    symbol = arguments["symbol"]
                    statement_type = arguments["statement_type"]
                    period = arguments.get("period", "annual")
                    limit = arguments.get("limit", 5)
                    
                    if statement_type == "income":
                        result = await self.fmp_client.get_income_statement(symbol, period, limit)
                    elif statement_type == "balance":
                        result = await self.fmp_client.get_balance_sheet(symbol, period, limit)
                    elif statement_type == "cashflow":
                        result = await self.fmp_client.get_cash_flow(symbol, period, limit)
                    else:
                        raise ValueError(f"Invalid statement type: {statement_type}")
                elif name == "get_key_metrics":
                    result = await self.fmp_client.get_key_metrics(
                        arguments["symbol"],
                        arguments.get("period", "annual"),
                        arguments.get("limit", 5)
                    )
                elif name == "get_financial_ratios":
                    result = await self.fmp_client.get_financial_ratios(
                        arguments["symbol"],
                        arguments.get("period", "annual"),
                        arguments.get("limit", 5)
                    )
                elif name == "get_dcf_valuation":
                    result = await self.fmp_client.get_dcf_valuation(arguments["symbol"])
                elif name == "search_companies":
                    result = await self.fmp_client.search_companies(
                        arguments["query"],
                        arguments.get("limit", 10)
                    )
                elif name == "get_sector_performance":
                    result = await self.fmp_client.get_sector_performance()
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))]
                )
            
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            """List available resources."""
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri="fmp://market/sectors",
                        name="Market Sectors Performance",
                        description="Real-time sector performance data",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="fmp://company/{symbol}/profile",
                        name="Company Profile",
                        description="Company profile information (use {symbol} placeholder)",
                        mimeType="application/json"
                    ),
                    Resource(
                        uri="fmp://company/{symbol}/financials",
                        name="Financial Statements",
                        description="Complete financial statements for a company (use {symbol} placeholder)",
                        mimeType="application/json"
                    )
                ]
            )
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> ReadResourceResult:
            """Get resource content."""
            if not self.fmp_client:
                self.fmp_client = FMPClient()
            
            try:
                if uri == "fmp://market/sectors":
                    result = await self.fmp_client.get_sector_performance()
                elif uri.startswith("fmp://company/") and uri.endswith("/profile"):
                    symbol = uri.split("/")[2]
                    result = await self.fmp_client.get_company_profile(symbol)
                elif uri.startswith("fmp://company/") and uri.endswith("/financials"):
                    symbol = uri.split("/")[2]
                    # Get all financial statements
                    income = await self.fmp_client.get_income_statement(symbol, limit=3)
                    balance = await self.fmp_client.get_balance_sheet(symbol, limit=3)
                    cashflow = await self.fmp_client.get_cash_flow(symbol, limit=3)
                    result = {
                        "income_statement": income,
                        "balance_sheet": balance,
                        "cash_flow": cashflow
                    }
                else:
                    raise ValueError(f"Unknown resource: {uri}")
                
                return ReadResourceResult(
                    contents=[TextContent(type="text", text=json.dumps(result, indent=2))]
                )
            
            except Exception as e:
                return ReadResourceResult(
                    contents=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
        
        @self.server.list_prompts()
        async def list_prompts() -> ListPromptsResult:
            """List available prompts."""
            return ListPromptsResult(
                prompts=[
                    Prompt(
                        name="financial_analysis",
                        description="Comprehensive financial analysis of a company",
                        arguments=[
                            PromptArgument(
                                name="symbol",
                                description="Stock ticker symbol",
                                required=True
                            )
                        ]
                    ),
                    Prompt(
                        name="investment_research",
                        description="Investment research report with valuation analysis",
                        arguments=[
                            PromptArgument(
                                name="symbol",
                                description="Stock ticker symbol",
                                required=True
                            )
                        ]
                    ),
                    Prompt(
                        name="sector_analysis",
                        description="Sector performance and comparison analysis",
                        arguments=[]
                    )
                ]
            )
        
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
            """Get prompt content."""
            if name == "financial_analysis":
                symbol = arguments.get("symbol", "").upper()
                return GetPromptResult(
                    description=f"Comprehensive financial analysis for {symbol}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"""Please provide a comprehensive financial analysis for {symbol}. Include:

1. Company Overview
   - Use get_company_profile to get basic company information
   - Business description, sector, and industry

2. Current Market Position
   - Use get_stock_quote for current stock price and trading data
   - Market capitalization and trading volume

3. Financial Health Analysis
   - Use get_financial_statements for income, balance sheet, and cash flow
   - Analyze revenue trends, profitability, and cash generation
   - Use get_key_metrics for important financial metrics

4. Valuation Analysis
   - Use get_financial_ratios for valuation ratios (P/E, P/B, etc.)
   - Use get_dcf_valuation for intrinsic value estimation
   - Compare ratios to industry averages

5. Investment Recommendation
   - Summarize strengths and weaknesses
   - Provide investment thesis and risk factors
   - Rate as Buy/Hold/Sell with rationale

Please format the analysis in a clear, structured manner with data-driven insights."""
                            )
                        )
                    ]
                )
            
            elif name == "investment_research":
                symbol = arguments.get("symbol", "").upper()
                return GetPromptResult(
                    description=f"Investment research report for {symbol}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=f"""Create a detailed investment research report for {symbol}. Structure it as follows:

## Executive Summary
- Investment thesis in 2-3 sentences
- Target price and recommendation

## Company Analysis
- Use get_company_profile for company background
- Business model and competitive advantages
- Recent developments and catalysts

## Financial Analysis
- Use get_financial_statements for 5 years of data
- Revenue growth analysis and sustainability
- Margin analysis and profitability trends
- Balance sheet strength and debt levels
- Cash flow generation and capital allocation

## Valuation
- Use get_financial_ratios for current valuation metrics
- Use get_dcf_valuation for intrinsic value
- Compare to peers and historical averages
- Multiple valuation approaches (P/E, EV/EBITDA, etc.)

## Risks and Catalysts
- Key risk factors to monitor
- Potential positive catalysts
- Scenario analysis

## Investment Recommendation
- Buy/Hold/Sell recommendation
- Target price with 12-month horizon
- Position sizing suggestion

Please provide specific numbers and ratios to support all conclusions."""
                            )
                        )
                    ]
                )
            
            elif name == "sector_analysis":
                return GetPromptResult(
                    description="Sector performance and comparison analysis",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text="""Provide a comprehensive sector analysis using the available data:

## Market Overview
- Use get_sector_performance to get current sector performance
- Identify best and worst performing sectors
- Analyze performance trends and momentum

## Sector Deep Dive
For the top 3 performing sectors:
1. Key drivers of outperformance
2. Representative companies in each sector
3. Valuation levels and opportunities

## Investment Implications
- Sectors to overweight/underweight
- Rotation opportunities
- Risk factors by sector

## Market Outlook
- Economic factors affecting different sectors
- Interest rate sensitivity analysis
- Growth vs. value sector positioning

Please format with clear sections and data-driven insights."""
                            )
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown prompt: {name}")
    
    async def run(self) -> None:
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="fmp-mcp-server",
                    server_version="0.1.0"
                )
            )
    
    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.fmp_client:
            await self.fmp_client.close()


async def main() -> None:
    """Main entry point."""
    server = FMPServer()
    try:
        await server.run()
    finally:
        await server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())