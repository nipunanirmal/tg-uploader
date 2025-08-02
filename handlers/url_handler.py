from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
import re
import asyncio
import tempfile
import shutil
import json
import time
import threading
from pathlib import Path

# Detect python-telegram-bot version
try:
    # Try importing v20.x classes
    from telegram.ext import ContextTypes
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    PTB_VERSION = 20
except ImportError:
    # v13.x doesn't have ContextTypes
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    PTB_VERSION = 13

# Import translation
from translation import Translation

# Import helper functions from start.py
from handlers.start import check_blacklist, add_chat

# Import database functions
from database import get_stuff, set_stuff

# Import URL processor
from url_processor import URLProcessor

# Simple add blacklist function
def add_blacklist(user_id):
    blacklist = get_stuff("BLACKLIST")
    if "USERS" not in blacklist:
        blacklist["USERS"] = []
    if user_id not in blacklist["USERS"]:
        blacklist["USERS"].append(user_id)
    set_stuff("BLACKLIST", blacklist)

# Store user data (URL, format selection, etc.)
user_data = {}

# Store active downloads/uploads for cancellation
active_tasks = {}

def url_handler(update, context):
    """Handle URL messages - main functionality"""
    # Check if this is a callback query (button press)
    if hasattr(update, 'callback_query') and update.callback_query:
        return handle_callback_query(update, context)
    
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Check if user is blacklisted
    if check_blacklist(user_id):
        return update.message.reply_text("You are B A N N E D 🤣🤣🤣🤣 Go find another bot to upload porn🖕")
    
    # Add user to chat list
    add_chat(user_id)
    
    # Check if message contains URL
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, message_text)
    
    if not urls:
        return update.message.reply_text("Please send a valid URL.")
    
    url = urls[0]
    
    # Check for banned content
    banned_keywords = ["porn", "sex", "sexy", "adult"]
    for keyword in banned_keywords:
        if keyword in url.lower():
            add_blacklist(user_id)
            return update.message.reply_text(f"<b>Sorry! No {keyword} content here. 🙂</b>", parse_mode='HTML')
    
    # Get config
    if bool(os.environ.get("WEBHOOK", False)):
        from sample_config import Config
    else:
        from config import Config
    
    # Check UPDATE_CHANNEL if configured
    if hasattr(Config, 'UPDATE_CHANNEL') and Config.UPDATE_CHANNEL:
        try:
            member = context.bot.get_chat_member(Config.UPDATE_CHANNEL, user_id)
            if member.status in ['kicked', 'left']:
                return update.message.reply_text("🤭 Sorry Dude, You are **B A N N E D 🤣🤣🤣**")
        except Exception:
            pass
    
    # Send processing message
    processing_msg = update.message.reply_text(
        "<b>Fetching available formats...⏳</b>",
        parse_mode='HTML'
    )
    
    try:
        # Initialize URL processor
        processor = URLProcessor()
        
        # Extract custom caption if provided
        custom_caption = None
        if " * " in url:
            url, custom_caption = url.split(" * ", 1)
            url = url.strip()
            custom_caption = custom_caption.strip()
        
        # Store user data
        user_data[user_id] = {
            'url': url,
            'custom_caption': custom_caption,
            'processing_msg_id': processing_msg.message_id,
            'chat_id': update.effective_chat.id
        }
        
        # Fetch available formats
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        formats_info = loop.run_until_complete(processor.get_available_formats(url))
        loop.close()
        
        # Store formats in user data
        user_data[user_id]['formats_info'] = formats_info
        
        # Debug: Print available formats
        print(f"DEBUG: Total formats available: {len(formats_info.get('formats', []))}")
        for i, fmt in enumerate(formats_info.get('formats', [])):
            print(f"DEBUG: Format {i}: {fmt.get('format_id')} - Video: {fmt.get('is_video', False)} - Size: {fmt.get('filesize', 'N/A')}")
        
        # Create format selection buttons (2 per row)
        keyboard = []
        row = []
        
        # Add video formats - show all video formats
        video_formats = [f for f in formats_info['formats'] if f.get('is_video', False)]
        filtered_video_formats = []
        
        # Include all video formats, prioritize those with known size
        for fmt in video_formats:
            # Always include the format, but prefer those with valid size info
            has_valid_size = False
            if 'filesize' in fmt and fmt['filesize']:
                try:
                    filesize = float(fmt['filesize'])
                    if filesize > 0:
                        has_valid_size = True
                except (ValueError, TypeError):
                    pass
            
            # Add format regardless of size info (for now, to debug)
            filtered_video_formats.append(fmt)
        
        # Use filtered formats
        for i, fmt in enumerate(filtered_video_formats):
            format_id = fmt['format_id']
            desc = fmt['description']
            # Create button with format info
            btn = InlineKeyboardButton(
                f"🎬 {desc}", 
                callback_data=f"fmt_{user_id}_{format_id}_video"
            )
            row.append(btn)
            
            # Add 2 buttons per row
            if len(row) == 2 or i == len(filtered_video_formats) - 1:
                keyboard.append(row)
                row = []
        
        # Add audio formats - show all audio formats
        audio_formats = [f for f in formats_info['formats'] if not f.get('is_video', True)]
        filtered_audio_formats = []
        
        # Include all audio formats, prioritize those with known size
        for fmt in audio_formats:
            # Always include the format, but prefer those with valid size info
            has_valid_size = False
            if 'filesize' in fmt and fmt['filesize']:
                try:
                    filesize = float(fmt['filesize'])
                    if filesize > 0:
                        has_valid_size = True
                except (ValueError, TypeError):
                    pass
            
            # Add format regardless of size info (for now, to debug)
            filtered_audio_formats.append(fmt)
        
        # Use filtered formats
        for i, fmt in enumerate(filtered_audio_formats):
            format_id = fmt['format_id']
            desc = fmt['description']
            # Create button with format info
            btn = InlineKeyboardButton(
                f"🎵 {desc}", 
                callback_data=f"fmt_{user_id}_{format_id}_audio"
            )
            row.append(btn)
            
            # Add 2 buttons per row
            if len(row) == 2 or i == len(filtered_audio_formats) - 1:
                keyboard.append(row)
                row = []
        
        # Create reply markup
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Update message with format selection
        title = formats_info.get('title', 'Unknown')
        uploader = formats_info.get('uploader', 'Unknown')
        duration = formats_info.get('duration', 0)
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
        
        processing_msg.edit_text(
            f"<b>{title}</b>\n\n" +
            f"<b>Uploader:</b> {uploader}\n" +
            f"<b>Duration:</b> {duration_str}\n\n" +
            f"<b>Select format to download:</b>",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        
    except Exception as e:
        # Handle errors
        processing_msg.edit_text(
            f"<b>❌ Error processing URL:</b> {str(e)}",
            parse_mode='HTML'
        )
        return

def handle_callback_query(update, context):
    """Handle button callbacks for format selection"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Answer callback query to stop loading animation
    query.answer()
    
    # Parse callback data
    data = query.data
    
    if data.startswith('cancel_'):
        # Cancel download callback
        parts = data.split('_')
        if len(parts) >= 3:
            callback_user_id = int(parts[1])
            task_id = '_'.join(parts[2:])  # Combine remaining parts as task_id
            
            # Check if this is the user who initiated the request
            if callback_user_id != user_id:
                return query.edit_message_text(
                    "You are not authorized to cancel this download.",
                    parse_mode='HTML'
                )
            
            # Show confirmation dialog
            confirm_button = InlineKeyboardButton(
                "✅ Yes, Cancel Download", 
                callback_data=f"confirm_cancel_{user_id}_{task_id}"
            )
            decline_button = InlineKeyboardButton(
                "🔄 Continue Download", 
                callback_data=f"continue_{user_id}_{task_id}"
            )
            keyboard = [[confirm_button], [decline_button]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            query.edit_message_text(
                "<b>⚠️ Are you sure you want to cancel this download?</b>\n\n" +
                "This will immediately stop the current process.",
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            return
    
    elif data.startswith('confirm_cancel_'):
        # Confirmed cancellation
        parts = data.split('_')
        if len(parts) >= 4:
            callback_user_id = int(parts[2])
            task_id = '_'.join(parts[3:])  # Combine remaining parts as task_id
            
            # Check if this is the user who initiated the request
            if callback_user_id != user_id:
                return query.answer("You are not authorized to cancel this download.")
            
            # Find the task
            if task_id in active_tasks:
                task_info = active_tasks[task_id]
                download_task = task_info['task']
                
                # Cancel the task
                if not download_task.done():
                    download_task.cancel()
                    
                    # Update message
                    query.edit_message_text(
                        "<b>❌ Download cancelled by user.</b>",
                        parse_mode='HTML'
                    )
                    
                    # Clean up
                    if user_id in user_data:
                        del user_data[user_id]
                    del active_tasks[task_id]
                    return
            
            query.edit_message_text(
                "<b>⚠️ Could not cancel download. It may have already completed or been cancelled.</b>",
                parse_mode='HTML'
            )
            return
    
    elif data.startswith('continue_'):
        # User declined cancellation
        parts = data.split('_')
        if len(parts) >= 3:
            callback_user_id = int(parts[1])
            task_id = '_'.join(parts[2:])  # Combine remaining parts as task_id
            
            # Check if this is the user who initiated the request
            if callback_user_id != user_id:
                return query.answer("You are not authorized for this action.")
            
            # Find the task
            if task_id in active_tasks:
                task_info = active_tasks[task_id]
                
                # Resume with a simple message
                query.edit_message_text(
                    "<b>Downloading resumed...</b>\n\n" +
                    "<i>Progress updates will continue shortly.</i>",
                    parse_mode='HTML'
                )
                return
            
            query.edit_message_text(
                "<b>⚠️ Could not continue download. It may have already completed or been cancelled.</b>",
                parse_mode='HTML'
            )
            return
    
    elif data.startswith('fmt_'):
        # Format selection callback
        parts = data.split('_')
        if len(parts) >= 4:
            callback_user_id = int(parts[1])
            format_id = parts[2]
            file_type = parts[3]  # 'video' or 'audio'
            
            # Check if this is the user who initiated the request
            if callback_user_id != user_id:
                return query.edit_message_text(
                    "You are not authorized to use these buttons.",
                    parse_mode='HTML'
                )
            
            # Get user data
            if user_id not in user_data:
                return query.edit_message_text(
                    "Session expired. Please send the URL again.",
                    parse_mode='HTML'
                )
            
            user_info = user_data[user_id]
            url = user_info['url']
            custom_caption = user_info['custom_caption']
            formats_info = user_info.get('formats_info', {})
            
            # Update message to show download progress
            query.edit_message_text(
                f"<b>Downloading:</b> {formats_info.get('title', 'Video')}\n\n" +
                f"<b>Format:</b> {format_id} ({file_type})\n\n" +
                "<i>This may take a while depending on file size...</i>",
                parse_mode='HTML'
            )
            
            try:
                # Initialize URL processor
                processor = URLProcessor()
                
                # Create a unique download directory
                download_dir = os.path.join(
                    "./DOWNLOADS", 
                    f"{int(time.time())}"
                )
                os.makedirs(download_dir, exist_ok=True)
                
                # Download with selected format
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Start download in background
                download_task = loop.create_task(
                    processor._download_with_ytdlp(url, download_dir, custom_caption, format_id)
                )
                
                # Store task for possible cancellation
                task_id = f"task_{user_id}_{int(time.time())}"
                active_tasks[task_id] = {
                    'task': download_task,
                    'loop': loop,
                    'status': 'downloading',
                    'user_id': user_id,
                    'chat_id': update.effective_chat.id,
                    'message_id': query.message.message_id
                }
                
                # Update progress while downloading
                last_update = time.time()
                while not download_task.done():
                    # Only update UI every 3 seconds to avoid flooding
                    if time.time() - last_update > 3:
                        try:
                            # Get current progress from logs
                            progress_text = "<b>Downloading:</b> {}".format(formats_info.get('title', 'Video'))
                            progress_text += "\n\n<b>Format:</b> {} ({})".format(format_id, file_type)
                            
                            # Get progress from processor if available
                            if hasattr(processor, 'download_progress') and processor.download_progress:
                                for filename, progress in processor.download_progress.items():
                                    percent = progress.get('percent', 0)
                                    speed = progress.get('speed', 0)
                                    eta = progress.get('eta', 0)
                                    
                                    # Format progress information
                                    progress_text += f"\n\n<i>Downloaded: {percent:.1f}%</i>"
                                    if speed > 0:
                                        speed_text = f"{speed / 1024 / 1024:.1f} MB/s"
                                        progress_text += f"\n<i>Speed: {speed_text}</i>"
                                    if eta > 0:
                                        progress_text += f"\n<i>ETA: {eta} seconds</i>"
                            else:
                                progress_text += "\n\n<i>Downloading... Please wait.</i>"
                                progress_text += "\n\n⏳ Progress will update every few seconds"
                            
                            # Create cancel button
                            cancel_button = InlineKeyboardButton(
                                "❌ Cancel Download", 
                                callback_data=f"cancel_{user_id}_{task_id}"
                            )
                            keyboard = [[cancel_button]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            
                            # Update message with current progress and cancel button
                            query.edit_message_text(
                                progress_text,
                                parse_mode='HTML',
                                reply_markup=reply_markup
                            )
                            last_update = time.time()
                        except Exception as e:
                            logging.error(f"Error updating progress: {e}")
                    
                    # Sleep briefly to avoid CPU hogging
                    loop.run_until_complete(asyncio.sleep(0.5))
                
                # Clean up task tracking
                if task_id in active_tasks:
                    del active_tasks[task_id]
                
                # Get download result (if not cancelled)
                try:
                    if not download_task.cancelled():
                        result = download_task.result()
                    else:
                        # Task was cancelled
                        loop.close()
                        return
                except asyncio.CancelledError:
                    # Task was cancelled
                    loop.close()
                    return
                except Exception as e:
                    # Task failed
                    query.edit_message_text(
                        f"<b>❌ Error during download:</b> {str(e)}",
                        parse_mode='HTML'
                    )
                    loop.close()
                    return
                
                loop.close()
                
                if not result or not result.get('files'):
                    return query.edit_message_text(
                        "<b>❌ Failed to download file.</b>",
                        parse_mode='HTML'
                    )
                
                # Upload each file
                uploaded_files = []  # Track files for cleanup
                for file_info in result['files']:
                    file_path = file_info['file_path']
                    caption = file_info['caption']
                    
                    # Update processing message
                    query.edit_message_text(
                        f"<b>Uploading:</b> {os.path.basename(file_path)}\n\n<i>Please wait...</i>",
                        parse_mode='HTML'
                    )
                    
                    # Check if file needs splitting
                    if file_info['needs_splitting']:
                        # Run async function in sync context
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        chunks = loop.run_until_complete(processor.split_large_file(file_path))
                        loop.close()
                        
                        # Upload each chunk
                        chunk_files = []  # Track chunk files for cleanup
                        for i, chunk_path in enumerate(chunks):
                            chunk_caption = f"{caption} (Part {i+1}/{len(chunks)})"
                            
                            # Send file based on type
                            if file_type == 'video' and file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                                with open(chunk_path, 'rb') as file:
                                    context.bot.send_video(
                                        chat_id=update.effective_chat.id,
                                        video=file,
                                        caption=chunk_caption,
                                        parse_mode='HTML',
                                        supports_streaming=True
                                    )
                            else:
                                with open(chunk_path, 'rb') as file:
                                    context.bot.send_document(
                                        chat_id=update.effective_chat.id,
                                        document=file,
                                        caption=chunk_caption,
                                        parse_mode='HTML'
                                    )
                            
                            # Add chunk to cleanup list
                            chunk_files.append(chunk_path)
                        
                        # Clean up chunk files after upload
                        for chunk_path in chunk_files:
                            try:
                                if os.path.exists(chunk_path):
                                    os.remove(chunk_path)
                                    print(f"Deleted chunk file: {chunk_path}")
                            except Exception as e:
                                print(f"Failed to delete chunk file {chunk_path}: {e}")
                        
                        # Clean up split directory if empty
                        try:
                            split_dir = os.path.dirname(chunk_files[0]) if chunk_files else None
                            if split_dir and os.path.exists(split_dir) and not os.listdir(split_dir):
                                os.rmdir(split_dir)
                                print(f"Deleted empty split directory: {split_dir}")
                        except Exception as e:
                            print(f"Failed to delete split directory: {e}")
                    else:
                        # Send file based on type
                        if file_type == 'video' and file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                            with open(file_path, 'rb') as file:
                                context.bot.send_video(
                                    chat_id=update.effective_chat.id,
                                    video=file,
                                    caption=caption,
                                    parse_mode='HTML',
                                    supports_streaming=True
                                )
                        else:
                            with open(file_path, 'rb') as file:
                                context.bot.send_document(
                                    chat_id=update.effective_chat.id,
                                    document=file,
                                    caption=caption,
                                    parse_mode='HTML'
                                )
                    
                    # Add file to cleanup list
                    uploaded_files.append(file_path)
                
                # Clean up downloaded files after successful upload
                for file_path in uploaded_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            print(f"Deleted uploaded file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete file {file_path}: {e}")
                
                # Clean up download directories if empty
                download_dirs = set()
                for file_path in uploaded_files:
                    download_dir = os.path.dirname(file_path)
                    if download_dir:
                        download_dirs.add(download_dir)
                
                for download_dir in download_dirs:
                    try:
                        if os.path.exists(download_dir) and not os.listdir(download_dir):
                            os.rmdir(download_dir)
                            print(f"Deleted empty download directory: {download_dir}")
                    except Exception as e:
                        print(f"Failed to delete directory {download_dir}: {e}")
                
                # Final success message
                query.edit_message_text(
                    f"<b>✅ Successfully processed URL!</b>\n\n{len(result['files'])} file(s) uploaded.\n<i>Files cleaned up to save space.</i>",
                    parse_mode='HTML'
                )
                
                # Clean up user data
                if user_id in user_data:
                    del user_data[user_id]
                
            except Exception as e:
                # Handle errors
                query.edit_message_text(
                    f"<b>❌ Error processing URL:</b> {str(e)}",
                    parse_mode='HTML'
                )
                return
