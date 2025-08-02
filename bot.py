#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import json
import sys
from flask import Flask, request

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()
logger.info("Loaded environment variables from .env file")

# Initialize database
from database import get_stuff, set_stuff

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Detect python-telegram-bot version
try:
    # Try importing v20.x classes
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
    PTB_VERSION = 20
    logger.info("Using python-telegram-bot v20.x")
except ImportError:
    try:
        # Try importing v13.x classes
        from telegram import Update
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
        PTB_VERSION = 13
        logger.info("Using python-telegram-bot v13.x")
    except ImportError:
        logger.error("Failed to import python-telegram-bot. Please install it with: pip install python-telegram-bot")
        sys.exit(1)

# Import start and help handlers
from handlers.start import start_handler, help_handler

# Import URL handler
from handlers.url_handler import url_handler

from handlers.blacklist_handlers import blacklist_handlers
from handlers.broadcast_handlers import broadcast_handlers
from handlers.thumbnail_handlers import thumbnail_handlers

# Flask app for webhook
app = Flask(__name__)

def create_application():
    """Create and configure the telegram application or updater based on version"""
    if PTB_VERSION >= 20:
        # v20.x style with proper async support
        application = Application.builder().token(Config.TG_BOT_TOKEN).build()
        
        # Add handlers - for v20.x with async handlers
        # We've updated the handler functions to be async
        application.add_handler(CommandHandler("start", start_handler))
        application.add_handler(CommandHandler("help", help_handler))
        
        # Add URL handler for v20.x
        application.add_handler(CommandHandler("url", url_handler))
        
        # Add other handlers
        for handler in blacklist_handlers:
            application.add_handler(handler)
        
        for handler in broadcast_handlers:
            application.add_handler(handler)
            
        for handler in thumbnail_handlers:
            application.add_handler(handler)
        
        return application
    else:
        # v13.x style
        updater = Updater(Config.TG_BOT_TOKEN)
        dispatcher = updater.dispatcher
        
        # Add handlers
        dispatcher.add_handler(CommandHandler("start", start_handler))
        dispatcher.add_handler(CommandHandler("help", help_handler))
        
        # Add URL handler for v13.x
        dispatcher.add_handler(CommandHandler("url", url_handler))
        
        # Add message handler for URLs
        from telegram.ext import MessageHandler, Filters
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, url_handler))
        
        # Add callback query handler for button clicks
        dispatcher.add_handler(CallbackQueryHandler(url_handler))
        
        # Add other handlers
        for handler in blacklist_handlers:
            dispatcher.add_handler(handler)
        
        for handler in broadcast_handlers:
            dispatcher.add_handler(handler)
            
        for handler in thumbnail_handlers:
            dispatcher.add_handler(handler)
        
        return updater

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates"""
    json_data = request.get_json()
    
    if PTB_VERSION >= 20:
        # v20.x style
        update = Update.de_json(json_data, telegram_app.bot)
        telegram_app.process_update(update)
    else:
        # v13.x style
        update = Update.de_json(json_data, telegram_app.dispatcher.bot)
        telegram_app.dispatcher.process_update(update)
    
    return 'OK'

if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    
    # Add authorized user if not already in config
    if hasattr(Config, 'AUTH_USERS'):
        Config.AUTH_USERS.add(683538773)
    
    # Create telegram application or updater
    telegram_app = create_application()
    
    if bool(os.environ.get("WEBHOOK", False)):
        # Webhook mode for production
        webhook_url = os.environ.get("WEBHOOK_URL", "")
        port = int(os.environ.get("PORT", 5000))
        
        # Set webhook based on version
        if PTB_VERSION >= 20:
            # v20.x style
            telegram_app.bot.set_webhook(url=f"{webhook_url}/webhook")
        else:
            # v13.x style
            telegram_app.bot.set_webhook(url=f"{webhook_url}/webhook")
        
        # Run Flask app
        logger.info(f"Starting webhook on port {port}")
        app.run(host='0.0.0.0', port=port)
    else:
        # Polling mode for development
        logger.info("Starting polling mode")
        if PTB_VERSION >= 20:
            # v20.x style
            telegram_app.run_polling()
        else:
            # v13.x style
            telegram_app.start_polling()
