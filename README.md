# Oura Ring MCP Server

A comprehensive Model Context Protocol (MCP) server for integrating with the Oura Ring API, providing access to all health and wellness data endpoints.

## Features

- **Complete API Coverage**: Access to all 10 Oura Ring API endpoints
- **Personal Info**: Get user profile and device information
- **Health Metrics**: Daily activity, sleep, readiness, and SpO2 data
- **Session Tracking**: Detailed session and workout data
- **Enhanced Tags**: Custom tags and notes
- **Real-time Resources**: Auto-updating recent data (7-day windows)
- **Pagination Support**: Handle large datasets with pagination tokens
- **Date Range Filtering**: Flexible date-based queries

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

**Production Mode:**
```bash
uv run python -m src.oura_mcp_server.server
```

**Development Mode with Inspector:**
```bash
uv run mcp dev src/oura_mcp_server/server.py:mcp
```

The development mode launches the MCP Inspector at `http://localhost:6274` where you can:
- Test all tools interactively
- View real-time protocol messages
- Explore available resources
- Debug server functionality

### Available Tools

1. **get_oura_personal_info**: Get personal information and device details
2. **get_oura_sessions**: Get session data for date ranges
3. **get_oura_daily_activity**: Get daily activity metrics (steps, calories, distance)
4. **get_oura_daily_sleep**: Get daily sleep data and scores
5. **get_oura_daily_spo2**: Get daily SpO2 measurements
6. **get_oura_daily_readiness**: Get daily readiness scores
7. **get_oura_sleep**: Get detailed sleep session data
8. **get_oura_sleep_time**: Get sleep timing and duration data
9. **get_oura_workout**: Get workout and exercise sessions
10. **get_oura_enhanced_tag**: Get custom tags and notes

### Available Resources

1. **oura://personal_info**: User profile and device information
2. **oura://sessions/recent**: Recent session data (last 7 days)
3. **oura://activity/recent**: Recent daily activity (last 7 days)
4. **oura://sleep/recent**: Recent sleep data (last 7 days)
5. **oura://readiness/recent**: Recent readiness scores (last 7 days)

## API Integration

This server integrates with **all** Oura Ring API v2 endpoints:

- `/v2/usercollection/personal_info`
- `/v2/usercollection/session`
- `/v2/usercollection/daily_activity`
- `/v2/usercollection/daily_sleep`
- `/v2/usercollection/daily_spo2`
- `/v2/usercollection/daily_readiness`
- `/v2/usercollection/sleep`
- `/v2/usercollection/sleep_time`
- `/v2/usercollection/workout`
- `/v2/usercollection/enhanced_tag`

**Features:**
- Bearer token authentication
- Date range filtering
- Pagination support
- Comprehensive error handling
- Unified API client architecture

## Development

The server is built using:
- **FastMCP**: High-level MCP framework
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management
- **Pydantic**: Data validation

## Testing with MCP Inspector

The easiest way to test and explore the server is using the MCP Inspector:

1. **Start the development server:**
   ```bash
   uv run mcp dev src/oura_mcp_server/server.py:mcp
   ```

2. **Open the inspector URL** (shown in terminal output):
   ```
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<your-token>
   ```

3. **Test tools interactively:**
   - Try `get_oura_daily_activity` with dates like `2024-01-01` to `2024-01-07`
   - Explore `get_oura_personal_info` (no parameters needed)
   - View resources like `oura://activity/recent`

## Example Tool Calls

```bash
# Get daily activity data
get_oura_daily_activity(start_date="2024-01-01", end_date="2024-01-07")

# Get sleep data
get_oura_daily_sleep(start_date="2024-01-01", end_date="2024-01-07")

# Get personal info
get_oura_personal_info()

# Get workout sessions
get_oura_workout(start_date="2024-01-01", end_date="2024-01-07")
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