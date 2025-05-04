"""
Simplified test script for JsonDataReader
"""

import json
import logging
import sys
import os
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("test-script")

# Add project directory to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Base path for local data files
BASE_DATA_PATH = project_root / "local_data" / "data"

def validate_json_structure(game_name, data_type, data):
    """Validate JSON data structure based on game and data type"""
    
    expected_fields = {
        'team': ['name', 'world_ranking'],
        'players': ['nickname', 'name'],
        'upcoming_matches': ['opponent', 'date'],
        'past_matches': ['opponent', 'score', 'date'],
        'tournaments': ['name']
    }
    
    if data_type not in expected_fields:
        logger.warning(f"No validation rules for data type: {data_type}")
        return True
        
    # If data is a list, validate first item
    if isinstance(data, list) and data:
        item = data[0]
        missing_fields = [field for field in expected_fields[data_type] if field not in item]
        
        if missing_fields:
            logger.error(f"Missing expected fields in {game_name} {data_type}: {missing_fields}")
            return False
    elif isinstance(data, dict):
        missing_fields = [field for field in expected_fields[data_type] if field not in data]
        
        if missing_fields:
            logger.error(f"Missing expected fields in {game_name} {data_type}: {missing_fields}")
            return False
    else:
        logger.error(f"Unexpected data format for {game_name} {data_type}")
        return False
        
    return True

def test_json_reader():
    """Test function for directly reading JSON data files"""
    
    logger.info("Starting direct JSON file test...")
    logger.info(f"Using data path: {BASE_DATA_PATH}")
    
    if not BASE_DATA_PATH.exists():
        logger.error(f"Data path does not exist: {BASE_DATA_PATH}")
        return False
    
    # Check game folders
    game_folders = [f for f in BASE_DATA_PATH.iterdir() if f.is_dir()]
    
    if not game_folders:
        logger.error(f"No game folders found in {BASE_DATA_PATH}")
        return False
        
    logger.info(f"Found {len(game_folders)} game folders: {[f.name for f in game_folders]}")
    
    # Track test results
    success = True
    results = {}
    
    # Test JSON files from each game folder
    for game_folder in game_folders:
        game_name = game_folder.name
        logger.info(f"Testing game folder: {game_name}")
        
        json_files = list(game_folder.glob("*.json"))
        if not json_files:
            logger.warning(f"No JSON files found in {game_name}")
            results[game_name] = False
            success = False
            continue
            
        logger.info(f"Found {len(json_files)} JSON files: {[f.name for f in json_files]}")
        
        # Test results for this game
        game_success = True
        
        # Test each file
        for file_path in json_files:
            file_name = file_path.name
            data_type = file_name.replace(f"{game_name}_", "").replace(".json", "")
            
            try:
                # Check if file is empty
                if os.path.getsize(file_path) == 0:
                    logger.error(f"Empty file: {file_name}")
                    game_success = False
                    continue
                
                # Read and parse JSON
                logger.info(f"Reading {file_name}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Basic structure validation
                if isinstance(data, list):
                    logger.info(f"  - List with {len(data)} items")
                    if not data:
                        logger.warning(f"  - Empty data list in {file_name}")
                    else:
                        sample = data[0]
                        logger.info(f"  - Sample item keys: {list(sample.keys())}")
                        
                        # Validate against expected structure
                        if not validate_json_structure(game_name, data_type, data):
                            game_success = False
                            
                elif isinstance(data, dict):
                    logger.info(f"  - Object with keys: {list(data.keys())}")
                    
                    # Validate against expected structure
                    if not validate_json_structure(game_name, data_type, data):
                        game_success = False
                else:
                    logger.error(f"  - Invalid data format in {file_name}: {type(data)}")
                    game_success = False
                    
                logger.info(f"Successfully read {file_name}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {file_name}: {e}")
                game_success = False
            except Exception as e:
                logger.error(f"Error reading {file_name}: {e}")
                game_success = False
                
        results[game_name] = game_success
        if not game_success:
            success = False
            
        logger.info(f"Tests for {game_name} completed. Success: {game_success}")
        logger.info("-" * 50)
    
    # Overall test summary
    failures = [game for game, result in results.items() if not result]
    if failures:
        logger.warning(f"Tests failed for the following games: {failures}")
        logger.info(f"Test completion rate: {(len(results) - len(failures))/len(results)*100:.1f}%")
    else:
        logger.info("All game tests completed successfully!")
        
    return success

if __name__ == "__main__":
    success = test_json_reader()
    logger.info(f"Test suite completed. Overall success: {success}")
    sys.exit(0 if success else 1)