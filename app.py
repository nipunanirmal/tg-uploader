#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cPanel Python Application Entry Point
This file serves as the main entry point for cPanel Python applications
"""

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the Flask app from cpanel_webhook
try:
    from cpanel_webhook import app
    
    # This is the WSGI application object that cPanel will use
    application = app
    
    if __name__ == "__main__":
        # For local testing
        app.run(debug=True, host='0.0.0.0', port=5000)
        
except ImportError as e:
    print(f"Error importing cpanel_webhook: {e}")
    print("Make sure all dependencies are installed")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)
