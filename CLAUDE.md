# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FMP MCP Server - A Model Context Protocol server that provides tools, resources, and prompts for financial analysis using the Financial Modelling Prep API.

## Tech Stack

- **Language**: Python 3.10+
- **Package Manager**: uv (Astral's fast Python package manager)
- **Framework**: MCP (Model Context Protocol)
- **API Client**: httpx for async HTTP requests
- **Configuration**: python-dotenv for environment variables
- **Data Validation**: pydantic for data models
- **Testing**: pytest with asyncio support
- **Code Quality**: black, ruff, mypy

## Development Commands

### Setup
```bash
# Install dependencies
uv sync

# Install with development dependencies
uv sync --dev

# Copy environment template
cp .env.example .env
# Then edit .env with your FMP API key
```

### Testing
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/fmp_mcp_server
```

### Code Quality
```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Running the Server
```bash
# Run via module
uv run python -m fmp_mcp_server.server

# Or via installed script
uv run fmp-mcp-server

# Docker build and run
docker build -t fmp-mcp-server .
docker run --env-file .env fmp-mcp-server

# Docker Compose
docker-compose up -d
```

## Architecture

### Core Components

1. **FMPClient** (`src/fmp_mcp_server/client.py`)
   - Handles all Financial Modelling Prep API interactions
   - Async HTTP client with proper error handling
   - Methods for different API endpoints (profiles, quotes, financials, etc.)

2. **FMPServer** (`src/fmp_mcp_server/server.py`)
   - Main MCP server implementation
   - Implements tools, resources, and prompts
   - Handles MCP protocol communication

### MCP Components

**Tools** (8 available):
- `get_company_profile`: Company information and metrics
- `get_stock_quote`: Real-time stock data
- `get_financial_statements`: Income, balance sheet, cash flow
- `get_key_metrics`: Financial KPIs and ratios
- `get_financial_ratios`: Comprehensive ratio analysis
- `get_dcf_valuation`: Discounted cash flow valuation
- `search_companies`: Company search functionality
- `get_sector_performance`: Market sector overview

**Resources** (3 available):
- `fmp://market/sectors`: Sector performance data
- `fmp://company/{symbol}/profile`: Company profiles
- `fmp://company/{symbol}/financials`: Financial statements

**Prompts** (3 available):
- `financial_analysis`: Comprehensive analysis workflow
- `investment_research`: Investment research report
- `sector_analysis`: Sector comparison analysis

## API Configuration

### Required Environment Variables
- `FMP_API_KEY`: Your Financial Modelling Prep API key (required)
- `FMP_BASE_URL`: API base URL (optional, defaults to official FMP API)
- `RATE_LIMIT_REQUESTS_PER_MINUTE`: Rate limiting (optional)

### API Key Setup
1. Sign up at https://financialmodelingprep.com/developer/docs
2. Get your API key from the dashboard
3. Add to `.env` file: `FMP_API_KEY=your_key_here`

## Usage Patterns

When working with this codebase:

1. **Adding new API endpoints**: Extend `FMPClient` with new methods
2. **Adding new tools**: Add to `list_tools()` and `call_tool()` handlers
3. **Adding new resources**: Add to `list_resources()` and `get_resource()` handlers
4. **Adding new prompts**: Add to `list_prompts()` and `get_prompt()` handlers

## Testing

- All API calls are mocked in tests
- Use `pytest-asyncio` for async test functions
- Test files mirror source structure in `tests/` directory
- Mock external HTTP calls to avoid API rate limits during testing

## CI/CD Pipeline

GitHub Actions workflows:
- **CI Pipeline**: Runs tests, linting, type checking across Python 3.10-3.12
- **Docker Pipeline**: Builds and pushes Docker images to GitHub Container Registry
- **Coverage**: Reports code coverage to Codecov

## Docker Deployment

- Multi-stage Docker build with uv for fast dependency installation
- Non-root user for security
- Health checks included
- Docker Compose for easy local development
- Pre-built images available at `ghcr.io/ccdatatraits/fmp-mcp-server`

## Rate Limits

Financial Modelling Prep API has different rate limits:
- Free tier: 250 requests/day
- Paid tiers: 300-2000 requests/minute

The client handles rate limiting gracefully and will raise appropriate errors.