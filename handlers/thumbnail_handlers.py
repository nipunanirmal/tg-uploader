from telegram import Update
import os
import shutil

# Detect python-telegram-bot version
try:
    # Try importing v20.x classes
    from telegram.ext import ContextTypes, CommandHandler
    PTB_VERSION = 20
except ImportError:
    # v13.x doesn't have ContextTypes
    from telegram.ext import CommandHandler
    PTB_VERSION = 13

# Import helper functions from start.py
from handlers.start import check_blacklist, add_chat

def save_thumb_handler(update, context):
    """Handle /savethumb command - save custom thumbnail"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("You are B A N N E D ")
            return async_reply()
        else:
            return update.message.reply_text("You are B A N N E D ")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Check if thumbnail is provided
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("Reply to an image to save as thumbnail.")
            return async_reply()
        else:
            return update.message.reply_text("Reply to an image to save as thumbnail.")
    
    # Create download directory if it doesn't exist
    download_location = f"./DOWNLOADS/{user_id}"
    os.makedirs(download_location, exist_ok=True)
    
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_save_thumb():
            # Download and save thumbnail
            photo = update.message.reply_to_message.photo[-1]  # Get highest resolution
            photo_file = await context.bot.get_file(photo.file_id)
            await photo_file.download_to_drive(f"{download_location}/thumbnail.jpg")
            
            # Send confirmation message
            await update.message.reply_text(
                "Custom thumbnail saved. This image will be used in your next uploads.",
                parse_mode='HTML'
            )
        return async_save_thumb()
    else:
        # v13.x style (sync)
        # Download and save thumbnail
        photo = update.message.reply_to_message.photo[-1]  # Get highest resolution
        photo_file = context.bot.get_file(photo.file_id)
        photo_file.download(f"{download_location}/thumbnail.jpg")
        
        # Send confirmation message
        return update.message.reply_text(
            "Custom thumbnail saved. This image will be used in your next uploads.",
            parse_mode='HTML'
        )

def delete_thumb_handler(update, context):
    """Handle /deletethumbnail command - delete custom thumbnail"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("You are B A N N E D ")
            return async_reply()
        else:
            return update.message.reply_text("You are B A N N E D ")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Check if thumbnail exists
    thumb_path = f"./DOWNLOADS/{user_id}/thumbnail.jpg"
    if not os.path.exists(thumb_path):
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("No custom thumbnail found.")
            return async_reply()
        else:
            return update.message.reply_text("No custom thumbnail found.")
    
    # Delete thumbnail
    os.remove(thumb_path)
    
    # Send confirmation message
    if PTB_VERSION >= 20:
        async def async_reply():
            await update.message.reply_text(
                "Custom thumbnail cleared successfully.",
                parse_mode='HTML'
            )
        return async_reply()
    else:
        return update.message.reply_text(
            "Custom thumbnail cleared successfully.",
            parse_mode='HTML'
        )

def save_cookies_handler(update, context):
    """Handle /savecookies command - save cookies file"""
    user_id = update.effective_user.id
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("You are B A N N E D ")
            return async_reply()
        else:
            return update.message.reply_text("You are B A N N E D ")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Check if file is provided
    if not update.message.reply_to_message or not update.message.reply_to_message.document:
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("Reply to a cookies.txt file.")
            return async_reply()
        else:
            return update.message.reply_text("Reply to a cookies.txt file.")
    
    # Create download directory if it doesn't exist
    download_location = f"./DOWNLOADS/{user_id}"
    os.makedirs(download_location, exist_ok=True)
    
    # Download and save cookies file
    document = update.message.reply_to_message.document
    if document.file_name != "cookies.txt":
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("Please send a file named cookies.txt")
            return async_reply()
        else:
            return update.message.reply_text("Please send a file named cookies.txt")
    
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_save_cookies():
            doc_file = await context.bot.get_file(document.file_id)
            await doc_file.download_to_drive(f"{download_location}/cookies.txt")
            
            # Send confirmation message
            await update.message.reply_text(
                "Cookies file saved successfully.",
                parse_mode='HTML'
            )
        return async_save_cookies()
    else:
        # v13.x style (sync)
        doc_file = context.bot.get_file(document.file_id)
        doc_file.download(f"{download_location}/cookies.txt")
        
        # Send confirmation message
        return update.message.reply_text(
            "Cookies file saved successfully.",
            parse_mode='HTML'
        )

# Export handlers list
thumbnail_handlers = [
    CommandHandler("savethumb", save_thumb_handler),
    CommandHandler("deletethumbnail", delete_thumb_handler),
    CommandHandler("savecookies", save_cookies_handler),
]
