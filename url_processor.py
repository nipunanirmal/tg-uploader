#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Standalone URL processor module

import os
import re
import time
import logging
import asyncio
import yt_dlp
import tempfile
import shutil
from pathlib import Path
from utils import safe_float, safe_int, safe_compare_greater, sanitize_formats_list, format_file_size

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = 2040108421  # ~2GB (Telegram limit)
DOWNLOAD_LOCATION = "./DOWNLOADS"

class URLProcessor:
    """
    Standalone URL processor that handles downloading from various sources
    and preparing files for upload to Telegram.
    """
    
    def __init__(self, download_location=DOWNLOAD_LOCATION):
        """Initialize the URL processor"""
        self.download_location = download_location
        # Create download directory if it doesn't exist
        os.makedirs(download_location, exist_ok=True)
    
    async def process_url(self, url, custom_caption=None):
        """
        Process a URL and prepare it for upload
        
        Args:
            url (str): The URL to process
            custom_caption (str, optional): Custom caption for the file
            
        Returns:
            dict: Information about the downloaded file(s)
        """
        logger.info(f"Processing URL: {url}")
        
        # Extract custom caption if provided in URL format: url * caption
        if not custom_caption and " * " in url:
            url, custom_caption = url.split(" * ", 1)
            url = url.strip()
            custom_caption = custom_caption.strip()
            logger.info(f"Extracted custom caption: {custom_caption}")
        
        # Create a unique download directory for this URL
        download_dir = os.path.join(
            self.download_location, 
            f"{int(time.time())}"
        )
        os.makedirs(download_dir, exist_ok=True)
        
        try:
            # Check if it's a zoom URL
            if "zoom.us" in url.lower():
                return await self._process_zoom_url(url, download_dir, custom_caption)
            
            # Use yt-dlp for downloading
            return await self._download_with_ytdlp(url, download_dir, custom_caption)
        
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            # Clean up download directory
            shutil.rmtree(download_dir, ignore_errors=True)
            raise
    
    async def get_available_formats(self, url):
        """
        Get available formats for a URL without downloading
        
        Args:
            url (str): The URL to check
            
        Returns:
            dict: Available formats and video information
        """
        logger.info(f"Fetching available formats for: {url}")
        
        # Set up yt-dlp options for format listing only
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'listformats': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            # Filter and organize formats
            formats = []
            if info.get('formats'):
                # Group by resolution for video formats
                video_formats = []
                audio_formats = []
                
                for f in info.get('formats', []):
                    format_id = f.get('format_id')
                    ext = f.get('ext')
                    resolution = f.get('resolution', 'N/A')
                    filesize = f.get('filesize')
                    # Use safe utility function for file size formatting
                    filesize_str = format_file_size(filesize)
                    format_note = f.get('format_note', '')
                    vcodec = f.get('vcodec', 'none')
                    acodec = f.get('acodec', 'none')
                    
                    # Skip formats without video or audio
                    if vcodec == 'none' and acodec == 'none':
                        continue
                    
                    # Create format description
                    if vcodec != 'none':
                        format_desc = f"{resolution} ({format_note}) [{ext}] {filesize_str}"
                        video_formats.append({
                            'format_id': format_id,
                            'ext': ext,
                            'resolution': resolution,
                            'filesize': filesize_str,
                            'description': format_desc,
                            'is_video': True
                        })
                    elif acodec != 'none':
                        format_desc = f"Audio {format_note} [{ext}] {filesize_str}"
                        audio_formats.append({
                            'format_id': format_id,
                            'ext': ext,
                            'resolution': 'Audio only',
                            'filesize': filesize_str,
                            'description': format_desc,
                            'is_video': False
                        })
                
                # Sort video formats by resolution (highest first)
                video_formats.sort(key=lambda x: x.get('resolution', ''), reverse=True)
                formats = video_formats + audio_formats
            
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration'),
                'formats': sanitize_formats_list(formats),
                'thumbnail': info.get('thumbnail'),
                'webpage_url': info.get('webpage_url'),
                'uploader': info.get('uploader'),
            }
        except Exception as e:
            logger.error(f"Error fetching formats: {e}")
            raise
    
    async def _download_with_ytdlp(self, url, download_dir, custom_caption=None, format_id=None):
        """
        Download a file using yt-dlp
        
        Args:
            url (str): The URL to download
            download_dir (str): Directory to save the downloaded file
            custom_caption (str, optional): Custom caption for the file
            
        Returns:
            dict: Information about the downloaded file(s)
        """
        logger.info(f"Downloading with yt-dlp: {url}")
        
        # Set up yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': False,
            'no_warnings': False,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'progress_hooks': [lambda d: print(f"Downloaded: {d['filename']}")],
        }
        
        # If format_id is specified, use it
        if format_id:
            ydl_opts['format'] = format_id
        
        # Download the file
        downloaded_files = []
        download_progress = {}
        
        def progress_hook(d):
            status = d.get('status')
            if status == 'downloading':
                # Track download progress
                filename = d.get('filename', 'Unknown')
                downloaded = float(d.get('downloaded_bytes', 0))
                total = float(d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0))
                speed = float(d.get('speed', 0))
                eta = int(d.get('eta', 0))
                
                # Store progress info
                download_progress[filename] = {
                    'downloaded': downloaded,
                    'total': total,
                    'speed': speed,
                    'eta': eta,
                    'percent': (downloaded / total * 100) if safe_compare_greater(total, 0) else 0,
                    'timestamp': time.time()
                }
                
                # Print progress for logging
                percent = f"{downloaded / total * 100:.1f}%" if safe_compare_greater(total, 0) else "Unknown"
                speed_str = f"{speed / 1024 / 1024:.1f} MB/s" if safe_compare_greater(speed, 0) else "Unknown"
                print(f"Download progress: {percent} at {speed_str}, ETA: {eta} seconds")
                
            elif status == 'finished':
                downloaded_files.append(d['filename'])
                print(f"Download complete: {d['filename']}")
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
        
        logger.info(f"Downloaded files: {downloaded_files}")
        
        # Get downloaded file information
        if 'entries' in info:
            # Playlist
            files = []
            for i, entry in enumerate(info['entries']):
                if entry and i < len(downloaded_files):
                    file_path = downloaded_files[i]
                    files.append(self._get_file_info_from_path(file_path, entry, custom_caption))
            return {"files": files, "is_playlist": True}
        else:
            # Single file
            if downloaded_files:
                file_path = downloaded_files[0]
                file_info = self._get_file_info_from_path(file_path, info, custom_caption)
                return {"files": [file_info], "is_playlist": False}
            else:
                raise FileNotFoundError("No files were downloaded")
    
    async def _process_zoom_url(self, url, download_dir, custom_caption=None):
        """
        Process a Zoom recording URL
        
        Args:
            url (str): The Zoom URL to process
            download_dir (str): Directory to save the downloaded file
            custom_caption (str, optional): Custom caption for the file
            
        Returns:
            dict: Information about the downloaded file(s)
        """
        logger.info(f"Processing Zoom URL: {url}")
        
        # Check if it's a password-protected Zoom link
        passcode = None
        if "|" in url:
            url, passcode = url.split("|", 1)
            url = url.strip()
            passcode = passcode.strip()
            logger.info("Zoom URL is password protected")
        
        # TODO: Implement Zoom-specific download logic
        # For now, use yt-dlp with cookies if needed
        
        return await self._download_with_ytdlp(url, download_dir, custom_caption)
    
    def _get_file_info_from_path(self, file_path, info, custom_caption=None):
        """
        Get information about a downloaded file from its path
        
        Args:
            file_path (str): Path to the downloaded file
            info (dict): File information from yt-dlp
            custom_caption (str, optional): Custom caption for the file
            
        Returns:
            dict: File information
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Downloaded file not found at {file_path}")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Check if file needs to be split (over Telegram's limit)
        needs_splitting = safe_compare_greater(file_size, MAX_FILE_SIZE)
        
        # Use custom caption or video title
        caption = custom_caption or info.get('title', os.path.basename(file_path))
        
        return {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "file_size": file_size,
            "caption": caption,
            "duration": info.get('duration'),
            "width": info.get('width'),
            "height": info.get('height'),
            "needs_splitting": needs_splitting
        }
        
    def _get_file_info(self, download_dir, info, custom_caption=None):
        """
        Get information about a downloaded file
        
        Args:
            download_dir (str): Directory where the file was downloaded
            info (dict): File information from yt-dlp
            custom_caption (str, optional): Custom caption for the file
            
        Returns:
            dict: File information
        """
        # Find the downloaded file
        filename = info.get('_filename')
        if not filename:
            # Try to find the file based on title and extension
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')
            
            # Clean the title for filesystem compatibility
            title = re.sub(r'[\\/*?:"<>|]', "", title)
            
            # Look for the file in the download directory
            for file in os.listdir(download_dir):
                if file.startswith(title) and file.endswith(f".{ext}"):
                    filename = os.path.join(download_dir, file)
                    break
        
        if not filename or not os.path.exists(filename):
            raise FileNotFoundError(f"Downloaded file not found for {info.get('title', 'unknown')}")
        
        return self._get_file_info_from_path(filename, info, custom_caption)
    
    async def split_large_file(self, file_path, chunk_size=MAX_FILE_SIZE):
        """
        Split a large file into smaller chunks for Telegram upload
        
        Args:
            file_path (str): Path to the file to split
            chunk_size (int): Maximum size of each chunk
            
        Returns:
            list: List of paths to the split file chunks
        """
        logger.info(f"Splitting large file: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size <= chunk_size:
            return [file_path]  # No need to split
        
        # Create a directory for the split files
        base_name = os.path.basename(file_path)
        split_dir = os.path.join(os.path.dirname(file_path), f"split_{int(time.time())}")
        os.makedirs(split_dir, exist_ok=True)
        
        # Calculate number of chunks
        num_chunks = (file_size + chunk_size - 1) // chunk_size
        
        # Split the file
        chunk_paths = []
        with open(file_path, 'rb') as f:
            for i in range(num_chunks):
                chunk_path = os.path.join(split_dir, f"{base_name}.part{i+1:03d}")
                with open(chunk_path, 'wb') as chunk:
                    chunk.write(f.read(chunk_size))
                chunk_paths.append(chunk_path)
        
        logger.info(f"Split file into {len(chunk_paths)} chunks")
        return chunk_paths

# Example usage
async def main():
    """Example usage of the URL processor"""
    processor = URLProcessor()
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        result = await processor.process_url(url, "Custom Caption")
        print(f"Downloaded {len(result['files'])} files:")
        
        for file_info in result['files']:
            print(f"File: {file_info['file_name']}")
            print(f"Size: {file_info['file_size']} bytes")
            print(f"Caption: {file_info['caption']}")
            
            if file_info['needs_splitting']:
                chunks = await processor.split_large_file(file_info['file_path'])
                print(f"Split into {len(chunks)} chunks")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
