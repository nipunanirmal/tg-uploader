#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Environment setup script

import os
import sys

def setup_environment():
    """Set up environment variables for the bot"""
    # Check if TG_BOT_TOKEN is set
    if not os.environ.get("TG_BOT_TOKEN"):
        token = input("Enter your Telegram Bot Token: ")
        os.environ["TG_BOT_TOKEN"] = token
        print(f"Bot token set: {token[:5]}...")
    else:
        print(f"Bot token already set: {os.environ.get('TG_BOT_TOKEN')[:5]}...")
    
    # Check if APP_ID is set
    if not os.environ.get("APP_ID"):
        app_id = input("Enter your Telegram APP_ID: ")
        os.environ["APP_ID"] = app_id
        print(f"APP_ID set: {app_id}")
    else:
        print(f"APP_ID already set: {os.environ.get('APP_ID')}")
    
    # Check if API_HASH is set
    if not os.environ.get("API_HASH"):
        api_hash = input("Enter your Telegram API_HASH: ")
        os.environ["API_HASH"] = api_hash
        print(f"API_HASH set: {api_hash[:5]}...")
    else:
        print(f"API_HASH already set: {os.environ.get('API_HASH')[:5]}...")
    
    # Set AUTH_USERS if not set
    if not os.environ.get("AUTH_USERS"):
        auth_users = input("Enter authorized user IDs (comma-separated): ")
        os.environ["AUTH_USERS"] = auth_users
        print(f"AUTH_USERS set: {auth_users}")
    else:
        print(f"AUTH_USERS already set: {os.environ.get('AUTH_USERS')}")
    
    print("\nEnvironment variables set successfully!")
    print("You can now run the bot with: python bot.py")

if __name__ == "__main__":
    setup_environment()
