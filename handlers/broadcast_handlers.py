from telegram import Update
import os
import asyncio

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
from database import get_stuff

# Admin user IDs (from original code)
ADMIN_USERS = [-1001517978805, 1023936257, 1845875276, 1298181668]

# Simple get all chats function
def get_all_chats():
    chats = get_stuff("ALLCHATS")
    if "USERS" not in chats:
        return []
    return chats["USERS"]

def broadcast_handler(update, context):
    """Handle /broadcast command - send message to all users"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS and update.effective_chat.id not in ADMIN_USERS:
        return
    
    # Check if there's a message to broadcast
    if not context.args and not update.message.reply_to_message:
        if PTB_VERSION >= 20:
            async def async_reply():
                await update.message.reply_text("Please provide a message to broadcast or reply to a message.")
            return async_reply()
        else:
            return update.message.reply_text("Please provide a message to broadcast or reply to a message.")
    
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_broadcast():
            # Get message to broadcast
            if update.message.reply_to_message:
                broadcast_msg = update.message.reply_to_message
            else:
                broadcast_msg = update.message
                broadcast_msg.text = " ".join(context.args)
            
            # Get all chats
            all_chats = get_all_chats()
            
            # Send status message
            status_msg = await update.message.reply_text(f"Broadcasting to {len(all_chats)} chats...")
            
            # Broadcast message
            success = 0
            failed = 0
            
            for chat_id in all_chats:
                try:
                    # Forward message to each chat
                    await broadcast_msg.copy(chat_id=chat_id)
                    success += 1
                except Exception as e:
                    failed += 1
                    print(f"Failed to broadcast to {chat_id}: {e}")
                
                # Update status every 20 chats
                if (success + failed) % 20 == 0:
                    await status_msg.edit_text(f"Progress: {success+failed}/{len(all_chats)}\nSuccess: {success}\nFailed: {failed}")
                    await asyncio.sleep(0.5)  # Small delay to avoid rate limits
            
            # Final status update
            await status_msg.edit_text(f"Broadcast completed!\nTotal: {len(all_chats)}\nSuccess: {success}\nFailed: {failed}")
        
        return async_broadcast()
    else:
        # v13.x style (sync)
        # Get message to broadcast
        if update.message.reply_to_message:
            broadcast_msg = update.message.reply_to_message
        else:
            broadcast_msg = update.message
            broadcast_msg.text = " ".join(context.args)
        
        # Get all chats
        all_chats = get_all_chats()
        
        # Send status message
        status_msg = update.message.reply_text(f"Broadcasting to {len(all_chats)} chats...")
        
        # Broadcast message (simplified for v13.x)
        success = 0
        failed = 0
        
        for chat_id in all_chats:
            try:
                # Forward message to each chat
                broadcast_msg.forward(chat_id=chat_id)
                success += 1
            except Exception as e:
                failed += 1
                print(f"Failed to broadcast to {chat_id}: {e}")
            
            # Update status every 20 chats
            if (success + failed) % 20 == 0:
                status_msg.edit_text(f"Progress: {success+failed}/{len(all_chats)}\nSuccess: {success}\nFailed: {failed}")
        
        # Final status update
        status_msg.edit_text(f"Broadcast completed!\nTotal: {len(all_chats)}\nSuccess: {success}\nFailed: {failed}")
        
        return

def stats_handler(update, context):
    """Handle /stats command - show bot statistics"""
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in ADMIN_USERS and update.effective_chat.id not in ADMIN_USERS:
        return
    
    # Get all chats
    all_chats = get_all_chats()
    
    # Send stats message
    if PTB_VERSION >= 20:
        # v20.x style (async)
        async def async_reply():
            await update.message.reply_text(f"Total users: {len(all_chats)}")
        return async_reply()
    else:
        # v13.x style (sync)
        return update.message.reply_text(f"Total users: {len(all_chats)}")

# Export handlers list
broadcast_handlers = [
    CommandHandler("broadcast", broadcast_handler),
    CommandHandler("stats", stats_handler),
]
