from telegram import Update
import os
import sys

# Import translation
from translation import Translation

# Import helper functions from start.py
from handlers.start import check_blacklist, add_chat, PTB_VERSION

# Import ContextTypes if available (v20.x)
try:
    from telegram.ext import ContextTypes
except ImportError:
    pass

def help_handler(update, context):
    """Handle /help command"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        if PTB_VERSION >= 20:
            # v20.x style (async)
            async def async_reply():
                await update.message.reply_text("You are B A N N E D 🤣🤣🤣🤣")
            return async_reply()
        else:
            # v13.x style (sync)
            return update.message.reply_text("You are B A N N E D 🤣🤣🤣🤣")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Send help message
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_reply():
            await update.message.reply_text(
                Translation.HELP_USER,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        return async_reply()
    else:
        # v13.x style (sync)
        return update.message.reply_text(
            Translation.HELP_USER,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
