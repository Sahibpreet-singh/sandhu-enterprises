import mysql.connector
import json
import os

def get_connection():
    # Load config from config.json
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        db_config = config.get('database', {})
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to hardcoded values if config file is missing or invalid
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "9246",
            "database": "sandhu_enterprises"
        }

    return mysql.connector.connect(**db_config)

