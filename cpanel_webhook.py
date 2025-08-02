#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Webhook deployment script for cPanel and other simple hosting environments
This script uses Flask to create a simple webhook server for the Telegram bot
"""

import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token and webhook info from environment variables
TOKEN = os.environ.get("TG_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No TG_BOT_TOKEN found in environment variables")

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("No WEBHOOK_URL found in environment variables")

PORT = int(os.environ.get("PORT", 8443))

# Initialize database
from database import init_db
init_db()

# Create Flask app
app = Flask(__name__)

# Import handlers
from handlers.start import start_handler, help_handler
from handlers.url_handler import url_handler
from handlers.blacklist_handlers import blacklist_handlers
from handlers.broadcast_handlers import broadcast_handlers
from handlers.thumbnail_handlers import thumbnail_handlers

# Detect python-telegram-bot version and set up bot
try:
    # Try importing v20.x classes
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    from telegram.ext import CallbackQueryHandler
    
    PTB_VERSION = 20
    print("Using python-telegram-bot v20.x")
    
    # Create the bot with v20.x
    application = Application.builder().token(TOKEN).build()
    bot = application.bot
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("url", url_handler))
    
    # Add message handler for URL processing (this was missing!)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, url_handler))
    
    # Add callback query handler for button interactions
    from handlers.url_handler import handle_callback_query
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Add all other handlers
    for handler in blacklist_handlers + broadcast_handlers + thumbnail_handlers:
        application.add_handler(handler)
    
    # Process updates function for webhook
    def process_update(update_json):
        update = Update.de_json(update_json, bot)
        application.process_update(update)
        
except ImportError:
    # v13.x doesn't have Application
    from telegram import Update, Bot
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    from telegram.ext import CallbackQueryHandler, Dispatcher
    
    PTB_VERSION = 13
    print("Using python-telegram-bot v13.x")
    
    # Create the bot with v13.x
    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0)
    
    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("help", help_handler))
    dispatcher.add_handler(CommandHandler("url", url_handler))
    
    # Add message handler for URL processing (this was missing!)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, url_handler))
    
    # Add callback query handler for button interactions
    from handlers.url_handler import handle_callback_query
    dispatcher.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Add all other handlers
    for handler in blacklist_handlers + broadcast_handlers + thumbnail_handlers:
        dispatcher.add_handler(handler)
    
    # Process updates function for webhook
    def process_update(update_json):
        update = Update.de_json(update_json, bot)
        dispatcher.process_update(update)

# Flask route for webhook
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """Handle webhook requests from Telegram"""
    if request.method == "POST":
        update_json = request.get_json(force=True)
        process_update(update_json)
        return jsonify({"status": "ok"})

# Health check endpoint
@app.route('/', methods=['GET'])
def index():
    """Health check endpoint"""
    return "Bot is running!"

# Set webhook URL
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set webhook URL for Telegram"""
    webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
    
    # Check if URL is HTTPS (required by Telegram)
    if not webhook_url.startswith('https://'):
        warning_message = (
            "<b>Warning:</b> Telegram requires HTTPS URLs for webhooks.<br><br>"
            "Your current webhook URL is: <code>" + webhook_url + "</code><br><br>"
            "This will work for testing the webhook endpoint locally, but "
            "<b>will not work</b> for actual webhook registration with Telegram.<br><br>"
            "For production deployment:<br>"
            "1. Ensure your server has a valid SSL certificate<br>"
            "2. Set WEBHOOK_URL in .env to your HTTPS domain<br>"
            "3. Deploy to a server with HTTPS support (e.g., cPanel with SSL)<br><br>"
            "<i>Note: For local testing, you can use ngrok or similar tools to create a temporary HTTPS tunnel.</i>"
        )
        
        # For local testing, still try to set the webhook but with a warning
        logger.warning("Attempting to set webhook with HTTP URL (will likely fail)")
    
    try:
        # Use more parameters for better webhook setup
        if PTB_VERSION >= 20:
            # v20.x style
            success = bot.set_webhook(
                url=webhook_url,
                allowed_updates=['message', 'callback_query', 'inline_query'],
                drop_pending_updates=True,
                max_connections=40
            )
        else:
            # v13.x style
            success = bot.set_webhook(
                url=webhook_url,
                allowed_updates=['message', 'callback_query', 'inline_query'],
                drop_pending_updates=True,
                max_connections=40
            )
        
        if success:
            if not webhook_url.startswith('https://'):
                return f"<html><body>{warning_message}<hr>Webhook attempted to be set to {webhook_url}, but may not work without HTTPS.</body></html>"
            else:
                return f"Webhook successfully set to {webhook_url}"
        else:
            if not webhook_url.startswith('https://'):
                return f"<html><body>{warning_message}<hr>Failed to set webhook (Telegram requires HTTPS URLs)</body></html>", 400
            else:
                return "Failed to set webhook", 500
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        if not webhook_url.startswith('https://'):
            return f"<html><body>{warning_message}<hr>Error setting webhook: {str(e)}</body></html>", 400
        else:
            return f"Error setting webhook: {str(e)}", 500

# Remove webhook
@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    """Remove webhook from Telegram"""
    success = bot.delete_webhook()
    if success:
        return "Webhook removed"
    else:
        return "Failed to remove webhook", 500

# Get webhook info
@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    """Get webhook info from Telegram"""
    info = bot.get_webhook_info()
    return str(info)

if __name__ == '__main__':
    # Run Flask app
    print(f"Starting Flask server on port {PORT}...")
    print(f"Webhook URL: {WEBHOOK_URL}/{TOKEN}")
    print("Visit /set_webhook to set the webhook")
    print("Visit /webhook_info to check webhook status")
    app.run(host='0.0.0.0', port=PORT)
