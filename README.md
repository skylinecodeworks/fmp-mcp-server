# FMP MCP Server

A Model Context Protocol (MCP) server that provides tools, resources, and prompts for financial analysis using the Financial Modelling Prep API.

## Features

### Tools
- **get_company_profile**: Get comprehensive company information
- **get_stock_quote**: Real-time stock quotes and market data
- **get_financial_statements**: Income statement, balance sheet, and cash flow data
- **get_key_metrics**: Key financial metrics and KPIs
- **get_financial_ratios**: Comprehensive financial ratios for analysis
- **get_dcf_valuation**: Discounted cash flow valuation
- **search_companies**: Search for companies by name or symbol
- **get_sector_performance**: Market sector performance overview

### Resources
- **Market Sectors**: Real-time sector performance data
- **Company Profiles**: Detailed company information
- **Financial Statements**: Complete financial statement data

### Prompts
- **financial_analysis**: Comprehensive financial analysis workflow
- **investment_research**: Detailed investment research report
- **sector_analysis**: Sector performance and comparison analysis

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure API access**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Financial Modelling Prep API key
   ```

3. **Get API Key**:
   - Visit [Financial Modelling Prep](https://financialmodelingprep.com/developer/docs)
   - Sign up for an account
   - Copy your API key to the `.env` file

## Usage

### With Claude Code

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "fmp": {
      "command": "uv",
      "args": ["run", "python", "-m", "fmp_mcp_server.server"],
      "env": {
        "FMP_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Direct Usage

```bash
# Run the server
uv run python -m fmp_mcp_server.server

# Or use the installed script
uv run fmp-mcp-server
```

## Docker Usage

### Build and run with Docker
```bash
# Build the image
docker build -t fmp-mcp-server .

# Run with environment file
docker run --env-file .env fmp-mcp-server
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using pre-built image from GitHub Container Registry
```bash
docker run --env-file .env ghcr.io/ccdatatraits/fmp-mcp-server:latest
```

## Development

1. **Install with development dependencies**:
   ```bash
   uv sync --dev
   ```

2. **Run tests**:
   ```bash
   uv run pytest
   ```

3. **Format code**:
   ```bash
   uv run black src/
   uv run ruff check src/
   ```

4. **Type checking**:
   ```bash
   uv run mypy src/
   ```

## API Rate Limits

The Financial Modelling Prep API has rate limits depending on your subscription:
- Free: 250 requests/day
- Starter: 300 requests/minute
- Professional: 2000 requests/minute

Configure rate limiting in your `.env` file if needed.

## License

MIT License