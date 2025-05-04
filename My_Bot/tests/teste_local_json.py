"""
Script to test the local JSON data implementation for the FURIA handler
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("test-script")

# Add project directory to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Import the JSON reader
from api.bot.utils.leitor_json import json_reader

def is_valid_date(date_str):
    """Check if a string is a valid date in any of the supported formats"""
    formats = [
        '%Y-%m-%d',  # formato ISO
        '%d/%m/%Y'   # formato BR
    ]
    
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    
    return False

async def test_json_reader():
    """Test function to verify JSON reader functionality"""
    
    logger.info("Starting JSON reader test...")
    
    try:
        # Test getting supported games
        games = json_reader.get_supported_games()
        if not games:
            logger.error("No supported games found!")
            return False
            
        logger.info(f"Supported games: {games}")
        
        test_results = {}
        
        for game in games:
            logger.info(f"Testing data for {game}...")
            game_success = True
            
            try:
                # Test getting team info
                logger.info(f"Testing team info for {game}...")
                team_info = json_reader.get_team_info(game)
                if not team_info:
                    logger.warning(f"No team info found for {game}")
                    game_success = False
                else:
                    logger.info(f"Team name: {team_info.get('name')}")
                    logger.info(f"World ranking: {team_info.get('world_ranking')}")
                
                # Test getting players
                logger.info(f"Testing players for {game}...")
                players = json_reader.get_players(game)
                if not players:
                    logger.warning(f"No players found for {game}")
                    game_success = False
                else:
                    logger.info(f"Found {len(players)} players")
                    if players:
                        logger.info(f"First player: {players[0].get('nickname')}")
                
                # Test getting upcoming matches
                logger.info(f"Testing upcoming matches for {game}...")
                upcoming = json_reader.get_upcoming_matches(game)
                logger.info(f"Found {len(upcoming)} upcoming matches")
                if upcoming:
                    next_match = upcoming[0]
                    logger.info(f"Next match vs {next_match.get('opponent')} on {next_match.get('date')}")
                    
                    # Validate date format
                    if 'date' in next_match:
                        date_valid = is_valid_date(next_match['date'])
                        if date_valid:
                            logger.info("Date format is valid")
                        else:
                            logger.error(f"Invalid date format in upcoming match: {next_match.get('date')}")
                            game_success = False
                
                # Test getting past matches
                logger.info(f"Testing past matches for {game}...")
                past = json_reader.get_past_matches(game)
                logger.info(f"Found {len(past)} past matches")
                if past:
                    last_match = past[0]
                    logger.info(f"Last match vs {last_match.get('opponent')}, score: {last_match.get('score')}")
                    
                    # Validate score format (should contain '-' or 'vs')
                    if 'score' in last_match:
                        score = last_match['score']
                        if not ('-' in score or 'vs' in score.lower()):
                            logger.warning(f"Score format might be incorrect: {score}")
                
                # Test getting tournaments
                logger.info(f"Testing tournaments for {game}...")
                tournaments = json_reader.get_tournaments(game)
                logger.info(f"Found {len(tournaments)} tournaments")
                if tournaments:
                    logger.info(f"Recent tournament: {tournaments[0].get('name')}")
                
                test_results[game] = game_success
                
            except Exception as e:
                logger.error(f"Error testing {game}: {e}")
                test_results[game] = False
                
            logger.info(f"All tests for {game} completed. Success: {game_success}")
            logger.info("-" * 50)
        
        # Test cache functionality
        logger.info("Testing cache functionality...")
        cache_size_before = len(json_reader.cache)
        logger.info(f"Current cache entries: {cache_size_before}")
        
        # Clear cache for specific game
        if games:
            first_game = games[0]
            logger.info(f"Clearing cache for {first_game}...")
            json_reader.clear_cache(first_game)
            
            # Verify cache entries updated
            cache_size_after = len(json_reader.cache)
            logger.info(f"Cache entries after partial clear: {cache_size_after}")
            
            # Verify the specific game cache was cleared
            cleared = True
            for cache_key in json_reader.cache:
                if first_game.lower().replace(" ", "") in cache_key:
                    cleared = False
                    logger.warning(f"Cache for {first_game} was not completely cleared: {cache_key} still exists")
            
            if cleared:
                logger.info(f"Cache for {first_game} was successfully cleared")
        
        # Clear all cache
        logger.info("Clearing all cache...")
        json_reader.clear_cache()
        
        if len(json_reader.cache) > 0:
            logger.warning(f"Cache was not fully cleared. Remaining entries: {len(json_reader.cache)}")
        else:
            logger.info("All cache was successfully cleared")
        
        # Overall test summary
        failures = [game for game, success in test_results.items() if not success]
        if failures:
            logger.warning(f"Tests failed for the following games: {failures}")
            logger.info(f"Test completion rate: {(len(games) - len(failures))/len(games)*100:.1f}%")
        else:
            logger.info("All game tests completed successfully!")
        
        return all(test_results.values())
        
    except Exception as e:
        logger.error(f"Critical error in test execution: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_json_reader())
    logger.info(f"Test suite completed. Overall success: {success}")
    sys.exit(0 if success else 1)