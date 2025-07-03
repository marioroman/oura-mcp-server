# Oura Ring MCP Server

A Model Context Protocol (MCP) server for integrating with the Oura Ring API, providing access to session data and health metrics.

## Features

- **Session Data Access**: Retrieve Oura Ring session data for specified date ranges
- **Recent Sessions Resource**: Get session data from the last 7 days
- **Session Summary Tool**: Generate summaries of session data with counts and types
- **Pagination Support**: Handle large datasets with pagination tokens

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure API credentials**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Oura Ring access token
   ```

3. **Get your Oura Ring API token**:
   - Go to https://cloud.ouraring.com/personal-access-tokens
   - Create a new personal access token
   - Add it to your `.env` file as `OURA_ACCESS_TOKEN`

## Usage

### Running the MCP Server

```bash
uv run oura-mcp-server
```

### Available Tools

1. **get_oura_sessions**: Get session data for a specific date range
   - Parameters: `start_date`, `end_date`, `next_token` (optional)
   - Returns: JSON session data

2. **get_session_summary**: Get a summary of sessions for a date range
   - Parameters: `start_date`, `end_date`
   - Returns: Summary with session counts and types

### Available Resources

1. **oura://sessions/recent**: Recent session data from the last 7 days

## API Integration

This server integrates with the Oura Ring API v2, specifically the `/v2/usercollection/session` endpoint. It provides:

- Bearer token authentication
- Date range filtering
- Pagination support
- Error handling and validation

## Development

The server is built using:
- **FastMCP**: High-level MCP framework
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management
- **Pydantic**: Data validation

## Example Usage

```python
# Get sessions for the last week
sessions = get_oura_sessions("2024-01-01", "2024-01-07")

# Get a summary of recent sessions
summary = get_session_summary("2024-01-01", "2024-01-07")
```

## Error Handling

The server includes comprehensive error handling for:
- Invalid API tokens
- Network connectivity issues
- Invalid date formats
- API rate limiting
- HTTP errors

## Security

- API tokens are stored in environment variables
- No sensitive data is logged
- HTTPS is used for all API communications