# 🚀 cPanel Python Application Deployment Guide

## Complete Instructions for Hosting Telegram Bot on cPanel

### 📋 Prerequisites
- cPanel hosting account with Python support (Python 3.8+)
- Domain with SSL certificate (HTTPS required for Telegram webhooks)
- Your bot token from @BotFather
- SSH access (recommended) or File Manager access

---

## 🔧 Step 1: Prepare Your Environment

### 1.1 Create Environment File
Create a `.env` file in your project root with the following content:

```bash
# Telegram Bot Configuration
TG_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://yourdomain.com
PORT=5000

# Database Configuration (if using PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost/database_name

# Optional: Update Channel
UPDATE_CHANNEL=@your_channel

# Optional: Admin User ID
ADMIN_USER_ID=your_telegram_user_id
```

### 1.2 Update Requirements.txt
Ensure your `requirements.txt` includes all necessary packages:

```
python-telegram-bot[webhooks]==20.7
flask==2.3.3
python-dotenv==1.0.0
yt-dlp==2023.10.13
requests==2.31.0
beautifulsoup4==4.12.2
Pillow==10.0.1
aiohttp==3.8.6
psycopg2-binary==2.9.7
hachoir==3.1.3
numpy==1.24.3
```

---

## 🌐 Step 2: Upload Files to cPanel

### Option A: Using File Manager
1. Login to cPanel
2. Open **File Manager**
3. Navigate to your domain's public_html folder
4. Create a new folder (e.g., `telegram-bot`)
5. Upload all your project files to this folder

### Option B: Using SSH (Recommended)
```bash
# Connect to your server
ssh username@yourdomain.com

# Navigate to your domain folder
cd public_html

# Create bot directory
mkdir telegram-bot
cd telegram-bot

# Upload files using scp or git clone
```

---

## 🐍 Step 3: Create Python Application in cPanel

### 3.1 Access Python App Manager
1. Login to cPanel
2. Find **Python App** in the Software section
3. Click **Create Application**

### 3.2 Configure Application Settings
```
Application Root: telegram-bot
Application URL: telegram-bot (or leave blank for root)
Application Startup File: cpanel_webhook.py
Application Entry Point: app
Python Version: 3.8+ (highest available)
```

### 3.3 Set Environment Variables
In the Python App interface, add these environment variables:
```
TG_BOT_TOKEN = your_actual_bot_token
WEBHOOK_URL = https://yourdomain.com/telegram-bot
PORT = 5000
```

---

## 📦 Step 4: Install Dependencies

### 4.1 Access Terminal (if available)
```bash
# Navigate to your app directory
cd ~/public_html/telegram-bot

# Activate virtual environment (cPanel usually creates this automatically)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4.2 Alternative: Use cPanel Python App Interface
1. In Python App manager, click on your application
2. Click **Add Package**
3. Install packages one by one from requirements.txt

---

## 🔧 Step 5: Configure Application Files

### 5.1 Create startup.py (Alternative Entry Point)
```python
#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the Flask app
from cpanel_webhook import app

if __name__ == "__main__":
    app.run()
```

### 5.2 Create .htaccess for URL Rewriting (Optional)
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ cpanel_webhook.py/$1 [QSA,L]
```

---

## 🚀 Step 6: Deploy and Test

### 6.1 Start the Application
1. In cPanel Python App manager
2. Click **Restart** on your application
3. Check the **Status** - should show "Running"

### 6.2 Test the Application
Visit these URLs to test:
```
https://yourdomain.com/telegram-bot/
https://yourdomain.com/telegram-bot/set_webhook
https://yourdomain.com/telegram-bot/webhook_info
```

### 6.3 Set Telegram Webhook
1. Visit: `https://yourdomain.com/telegram-bot/set_webhook`
2. You should see: "Webhook successfully set to https://yourdomain.com/telegram-bot/YOUR_BOT_TOKEN"
3. Test your bot by sending `/start` in Telegram

---

## 🛠️ Step 7: Troubleshooting

### 7.1 Common Issues and Solutions

**Issue: "Module not found" errors**
```bash
# Solution: Install missing packages
pip install package_name
```

**Issue: "Permission denied" errors**
```bash
# Solution: Fix file permissions
chmod 755 cpanel_webhook.py
chmod -R 755 handlers/
```

**Issue: Webhook not working**
- Ensure your domain has SSL certificate
- Check that WEBHOOK_URL in .env is HTTPS
- Verify bot token is correct

**Issue: Database connection errors**
```python
# Add this to your config for SQLite (simpler for shared hosting)
import sqlite3
# Use SQLite instead of PostgreSQL for shared hosting
```

### 7.2 Check Logs
```bash
# View application logs
tail -f ~/logs/telegram-bot/error.log
tail -f ~/logs/telegram-bot/access.log
```

---

## 📁 Step 8: File Structure on Server

Your final structure should look like:
```
public_html/telegram-bot/
├── cpanel_webhook.py          # Main Flask app
├── bot.py                     # Original bot (not used in webhook mode)
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── utils.py                   # Utility functions
├── url_processor.py           # URL processing
├── translation.py             # Translations
├── handlers/                  # Bot handlers
│   ├── __init__.py
│   ├── start.py
│   ├── url_handler.py
│   └── ...
├── database/                  # Database modules
│   ├── __init__.py
│   └── ...
├── DOWNLOADS/                 # Temporary downloads (auto-cleaned)
└── venv/                      # Virtual environment (auto-created)
```

---

## 🔒 Step 9: Security Considerations

### 9.1 Secure Your Environment
```bash
# Set proper permissions
chmod 600 .env
chmod 755 cpanel_webhook.py
```

### 9.2 Hide Sensitive Files
Create `.htaccess` in your app root:
```apache
<Files ".env">
    Order allow,deny
    Deny from all
</Files>

<Files "*.py">
    Order allow,deny
    Deny from all
</Files>

# Only allow access to the main webhook endpoint
<Files "cpanel_webhook.py">
    Order deny,allow
    Allow from all
</Files>
```

---

## 📊 Step 10: Monitoring and Maintenance

### 10.1 Monitor Application
- Check Python App status regularly in cPanel
- Monitor disk usage (downloads are auto-cleaned)
- Check webhook status: `/webhook_info`

### 10.2 Updates
```bash
# To update the bot:
cd ~/public_html/telegram-bot
git pull origin main  # if using git
# Or upload new files via File Manager
# Then restart the Python app in cPanel
```

---

## 🆘 Support and Debugging

### Debug Mode
Add to your `.env`:
```
DEBUG=True
LOG_LEVEL=DEBUG
```

### Test Commands
```bash
# Test webhook locally
curl -X POST https://yourdomain.com/telegram-bot/YOUR_BOT_TOKEN \
  -H "Content-Type: application/json" \
  -d '{"update_id": 1, "message": {"message_id": 1, "date": 1234567890, "chat": {"id": 123, "type": "private"}, "from": {"id": 123, "is_bot": false, "first_name": "Test"}, "text": "/start"}}'
```

---

## ✅ Final Checklist

- [ ] All files uploaded to cPanel
- [ ] Python application created and configured
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Application running (green status)
- [ ] Webhook URL accessible
- [ ] Webhook set successfully
- [ ] Bot responds to `/start` command
- [ ] File cleanup working (check DOWNLOADS folder)

---

## 🎉 Congratulations!

Your Telegram bot is now hosted on cPanel and ready to serve users 24/7!

For support or issues, check the troubleshooting section above or review the application logs in cPanel.
