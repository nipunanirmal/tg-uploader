from telegram import Update
import os

# Detect python-telegram-bot version
try:
    # Try importing v20.x classes
    from telegram.ext import ContextTypes, CommandHandler
    PTB_VERSION = 20
except ImportError:
    # v13.x doesn't have ContextTypes
    from telegram.ext import CommandHandler
    PTB_VERSION = 13

# Import database functions
from database import get_stuff, set_stuff

# Import add_blacklist from url_handler
from handlers.url_handler import add_blacklist

# Admin user IDs (from original code)
ADMIN_USERS = [-1001517978805, 1023936257, 1845875276, 1298181668]

# Simple remove blacklist function
def remove_blacklist(user_id):
    blacklist = get_stuff("BLACKLIST")
    if "USERS" not in blacklist or user_id not in blacklist["USERS"]:
        return "User not found in blacklist!"
    
    blacklist["USERS"].remove(user_id)
    set_stuff("BLACKLIST", blacklist)
    return f"User {user_id} removed from blacklist!"

# Simple get blacklisted function
def get_blacklisted():
    blacklist = get_stuff("BLACKLIST")
    if "USERS" not in blacklist:
        return []
    return blacklist["USERS"]

def black_user_handler(update, context):
    """Handle /black command - blacklist a user"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS and update.effective_chat.id not in ADMIN_USERS:
        return
    
    try:
        target_user = int(context.args[0])
        add_blacklist(target_user)
        
        if PTB_VERSION >= 20:
            # v20.x style (async)
            async def async_reply():
                await update.message.reply_text(f"Blacklisted {target_user} !")
            return async_reply()
        else:
            # v13.x style (sync)
            return update.message.reply_text(f"Blacklisted {target_user} !")
    except (IndexError, ValueError):
        if PTB_VERSION >= 20:
            # v20.x style (async)
            async def async_reply():
                await update.message.reply_text("Whom to Blacklist ?")
            return async_reply()
        else:
            # v13.x style (sync)
            return update.message.reply_text("Whom to Blacklist ?")

def unblack_user_handler(update, context):
    """Handle /unblack command - remove user from blacklist"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS and update.effective_chat.id not in ADMIN_USERS:
        return
    
    try:
        target_user = int(context.args[0])
        result = remove_blacklist(target_user)
        
        if PTB_VERSION >= 20:
            # v20.x style (async)
            async def async_reply():
                await update.message.reply_text(result)
            return async_reply()
        else:
            # v13.x style (sync)
            return update.message.reply_text(result)
    except (IndexError, ValueError):
        if PTB_VERSION >= 20:
            # v20.x style (async)
            async def async_reply():
                await update.message.reply_text("Whom to remove from blacklist ?")
            return async_reply()
        else:
            # v13.x style (sync)
            return update.message.reply_text("Whom to remove from blacklist ?")

def list_blacklisted_handler(update, context):
    """Handle /listblack command - list blacklisted users"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS and update.effective_chat.id not in ADMIN_USERS:
        return
    
    blacklisted = get_blacklisted()
    text = "List of Blacklisted Users !"
    for user in blacklisted:
        text += f"\n{user}"
    
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_reply():
            await update.message.reply_text(text)
        return async_reply()
    else:
        # v13.x style (sync)
        return update.message.reply_text(text)

# Export handlers list
blacklist_handlers = [
    CommandHandler("black", black_user_handler),
    CommandHandler("unblack", unblack_user_handler),
    CommandHandler("listblack", list_blacklisted_handler),
]
