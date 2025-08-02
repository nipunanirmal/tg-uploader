"""
Simple imghdr replacement module for python-telegram-bot compatibility
"""

import os
import struct

def what(file, h=None):
    """
    Simplified version of the imghdr.what function
    Returns the type of image contained in a file or header bytes.
    """
    if h is None:
        if isinstance(file, str):
            with open(file, 'rb') as f:
                h = f.read(32)
        else:
            location = file.tell()
            h = file.read(32)
            file.seek(location)
            
    if h.startswith(b'\xff\xd8'):
        return 'jpeg'
    elif h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    elif h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'
    elif h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'
    elif h.startswith(b'BM'):
        return 'bmp'
    return None

# Add other functions that might be needed by python-telegram-bot
def test_jpeg(h, f=None):
    """Test for JPEG data"""
    if h[0:2] == b'\xff\xd8':
        return 'jpeg'
    return None
