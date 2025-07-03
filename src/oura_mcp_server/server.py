"""Oura Ring MCP Server implementation."""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, Tool, TextContent
from pydantic import BaseModel, Field

load_dotenv()


class OuraRingAPI:
    """Oura Ring API client."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.ouraring.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Make a request to the Oura Ring API."""
        url = f"{self.base_url}/{endpoint}"
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        if next_token:
            params["next_token"] = next_token
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_personal_info(self) -> Dict[str, Any]:
        """Get personal info from Oura Ring API."""
        url = f"{self.base_url}/usercollection/personal_info"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_sessions(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get session data from Oura Ring API."""
        return self._make_request("usercollection/session", start_date, end_date, next_token)
    
    def get_daily_activity(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get daily activity data from Oura Ring API."""
        return self._make_request("usercollection/daily_activity", start_date, end_date, next_token)
    
    def get_daily_sleep(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get daily sleep data from Oura Ring API."""
        return self._make_request("usercollection/daily_sleep", start_date, end_date, next_token)
    
    def get_daily_spo2(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get daily SpO2 data from Oura Ring API."""
        return self._make_request("usercollection/daily_spo2", start_date, end_date, next_token)
    
    def get_daily_readiness(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get daily readiness data from Oura Ring API."""
        return self._make_request("usercollection/daily_readiness", start_date, end_date, next_token)
    
    def get_sleep(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get sleep data from Oura Ring API."""
        return self._make_request("usercollection/sleep", start_date, end_date, next_token)
    
    def get_sleep_time(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get sleep time data from Oura Ring API."""
        return self._make_request("usercollection/sleep_time", start_date, end_date, next_token)
    
    def get_workout(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get workout data from Oura Ring API."""
        return self._make_request("usercollection/workout", start_date, end_date, next_token)
    
    def get_enhanced_tag(self, start_date: str, end_date: str, next_token: Optional[str] = None) -> Dict[str, Any]:
        """Get enhanced tag data from Oura Ring API."""
        return self._make_request("usercollection/enhanced_tag", start_date, end_date, next_token)


# Initialize FastMCP server
mcp = FastMCP("Oura Ring MCP Server")

# Initialize Oura Ring API client
oura_token = os.getenv("OURA_ACCESS_TOKEN")
if not oura_token:
    raise ValueError("OURA_ACCESS_TOKEN environment variable is required")

oura_api = OuraRingAPI(oura_token)


# Resources
@mcp.resource("oura://personal_info")
def get_personal_info_resource() -> str:
    """Get personal info from Oura Ring."""
    try:
        info = oura_api.get_personal_info()
        return f"Personal Info:\n\n{info}"
    except Exception as e:
        return f"Error fetching personal info: {str(e)}"


@mcp.resource("oura://sessions/recent")
def get_recent_sessions() -> str:
    """Get recent session data from the last 7 days."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        sessions = oura_api.get_sessions(start_date, end_date)
        return f"Recent Sessions ({start_date} to {end_date}):\n\n{sessions}"
    except Exception as e:
        return f"Error fetching recent sessions: {str(e)}"


@mcp.resource("oura://activity/recent")
def get_recent_activity() -> str:
    """Get recent daily activity data from the last 7 days."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        activity = oura_api.get_daily_activity(start_date, end_date)
        return f"Recent Daily Activity ({start_date} to {end_date}):\n\n{activity}"
    except Exception as e:
        return f"Error fetching recent activity: {str(e)}"


@mcp.resource("oura://sleep/recent")
def get_recent_sleep() -> str:
    """Get recent daily sleep data from the last 7 days."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        sleep = oura_api.get_daily_sleep(start_date, end_date)
        return f"Recent Daily Sleep ({start_date} to {end_date}):\n\n{sleep}"
    except Exception as e:
        return f"Error fetching recent sleep: {str(e)}"


@mcp.resource("oura://readiness/recent")
def get_recent_readiness() -> str:
    """Get recent daily readiness data from the last 7 days."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    try:
        readiness = oura_api.get_daily_readiness(start_date, end_date)
        return f"Recent Daily Readiness ({start_date} to {end_date}):\n\n{readiness}"
    except Exception as e:
        return f"Error fetching recent readiness: {str(e)}"


# Tools
@mcp.tool()
def get_oura_personal_info() -> str:
    """
    Get personal info from Oura Ring.
    
    Returns:
        JSON string containing personal information
    """
    try:
        info = oura_api.get_personal_info()
        return str(info)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_sessions(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring session data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing session data
    """
    try:
        sessions = oura_api.get_sessions(start_date, end_date, next_token)
        return str(sessions)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_daily_activity(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring daily activity data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing daily activity data
    """
    try:
        activity = oura_api.get_daily_activity(start_date, end_date, next_token)
        return str(activity)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_daily_sleep(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring daily sleep data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing daily sleep data
    """
    try:
        sleep = oura_api.get_daily_sleep(start_date, end_date, next_token)
        return str(sleep)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_daily_spo2(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring daily SpO2 data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing daily SpO2 data
    """
    try:
        spo2 = oura_api.get_daily_spo2(start_date, end_date, next_token)
        return str(spo2)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_daily_readiness(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring daily readiness data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing daily readiness data
    """
    try:
        readiness = oura_api.get_daily_readiness(start_date, end_date, next_token)
        return str(readiness)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_sleep(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring sleep data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing sleep data
    """
    try:
        sleep = oura_api.get_sleep(start_date, end_date, next_token)
        return str(sleep)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_sleep_time(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring sleep time data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing sleep time data
    """
    try:
        sleep_time = oura_api.get_sleep_time(start_date, end_date, next_token)
        return str(sleep_time)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_workout(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring workout data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing workout data
    """
    try:
        workout = oura_api.get_workout(start_date, end_date, next_token)
        return str(workout)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_oura_enhanced_tag(
    start_date: str,
    end_date: str,
    next_token: Optional[str] = None
) -> str:
    """
    Get Oura Ring enhanced tag data for a specific date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        next_token: Optional pagination token for getting more results
    
    Returns:
        JSON string containing enhanced tag data
    """
    try:
        tags = oura_api.get_enhanced_tag(start_date, end_date, next_token)
        return str(tags)
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Run the MCP server."""
    import sys
    print("Starting Oura Ring MCP Server...", file=sys.stderr)
    print("Tools: get_oura_personal_info, get_oura_sessions, get_oura_daily_activity, get_oura_daily_sleep, get_oura_daily_spo2, get_oura_daily_readiness, get_oura_sleep, get_oura_sleep_time, get_oura_workout, get_oura_enhanced_tag", file=sys.stderr)
    print("Resources: oura://personal_info, oura://sessions/recent, oura://activity/recent, oura://sleep/recent, oura://readiness/recent", file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()