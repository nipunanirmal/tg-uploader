from telegram import Update
import os
import sys

# Import translation
from translation import Translation

# Import database functions
from database import get_stuff, set_stuff

# Detect python-telegram-bot version
try:
    # Try importing v20.x classes
    from telegram.ext import ContextTypes
    PTB_VERSION = 20
except ImportError:
    # v13.x doesn't have ContextTypes
    PTB_VERSION = 13

# Simple blacklist check function
def check_blacklist(user_id):
    blacklist = get_stuff("BLACKLIST")
    if "USERS" in blacklist and user_id in blacklist["USERS"]:
        return True
    return False

# Simple add chat function
def add_chat(user_id):
    chats = get_stuff("ALLCHATS")
    if "USERS" not in chats:
        chats["USERS"] = []
    if user_id not in chats["USERS"]:
        chats["USERS"].append(user_id)
    set_stuff("ALLCHATS", chats)

def start_handler(update, context):
    """Handle /start command"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        return update.message.reply_text("You are B A N N E D 🤣🤣🤣🤣")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Send start message
    return update.message.reply_text(
        Translation.START_TEXT,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

def help_handler(update, context):
    """Handle /help command"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        return update.message.reply_text("You are B A N N E D 🤣🤣🤣🤣")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Send help message
    return update.message.reply_text(
        Translation.HELP_USER,
        parse_mode='HTML',
        disable_web_page_preview=True
    )
