import asyncio
import aiohttp
from understat import Understat

async def _fetch_players(league, season):
    async with aiohttp.ClientSession() as session:
        us = Understat(session)
        players = await us.get_league_players(league, season)
        return players

def fetch_understat_players(league, season):
    """
    Synchronous wrapper for Understat async API
    """
    return asyncio.run(_fetch_players(league, season))
