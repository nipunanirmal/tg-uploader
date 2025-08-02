# Deployment Guide for X-Uploader Telegram Bot

This guide provides instructions for deploying the X-Uploader Telegram bot in various environments, with a focus on simple hosting environments like cPanel.

## Prerequisites

- Python 3.7+ installed
- A Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather))
- A publicly accessible server with HTTPS support (required for Telegram webhooks)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
TG_BOT_TOKEN=your_telegram_bot_token
WEBHOOK=True
WEBHOOK_URL=https://your-domain.com
PORT=8443
AUTH_USERS=123456789 987654321  # Space-separated list of authorized user IDs
```

## Local Deployment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/x-uploader.git
   cd x-uploader
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the bot in polling mode:
   ```
   python bot.py
   ```

## cPanel Deployment

### Step 1: Set Up Python Application

1. Log in to your cPanel account.
2. Navigate to "Setup Python App" or similar (varies by host).
3. Create a new Python application with:
   - Python version: 3.7+ (3.9 recommended)
   - Application root: /path/to/your/bot
   - Application URL: https://your-domain.com
   - Application startup file: cpanel_webhook.py

### Step 2: Upload Files

1. Upload all bot files to your cPanel server using File Manager or FTP.
2. Make sure to include all necessary files:
   - All Python files
   - requirements.txt
   - .env file (with your environment variables)

### Step 3: Install Dependencies

1. Connect to your server via SSH or use cPanel's Terminal.
2. Navigate to your bot directory:
   ```
   cd /path/to/your/bot
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Step 4: Configure Webhook

1. Make sure your `.env` file contains:
   ```
   WEBHOOK=True
   WEBHOOK_URL=https://your-domain.com
   PORT=8443
   ```
   
   > **IMPORTANT**: The `WEBHOOK_URL` must use HTTPS (not HTTP) as Telegram requires secure webhooks.

2. You can set up the webhook in two ways:

   **Option A**: Using the built-in endpoint
   - After starting your application, visit:
   ```
   https://your-domain.com/set_webhook
   ```
   
   **Option B**: Using the Telegram API directly
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-domain.com/<YOUR_BOT_TOKEN>
   ```
   
3. To verify your webhook is properly set up, visit:
   ```
   https://your-domain.com/webhook_info
   ```
   
   You should see information about your webhook, including the URL and pending updates.

### Step 5: Start the Application

1. In cPanel, restart your Python application.
2. Check the application logs for any errors.
3. Test your bot by sending a message to it on Telegram.

## Troubleshooting

### Common Issues

1. **Webhook Connection Failed**:
   - Ensure your server has a valid SSL certificate
   - Check that the webhook URL is correct and accessible
   - Verify that your server allows incoming connections on the specified port

2. **Dependencies Installation Failed**:
   - Some cPanel hosts limit certain packages. Try using compatible versions:
   ```
   pip install python-telegram-bot==13.15
   pip install urllib3==1.26.15
   ```

3. **Application Not Starting**:
   - Check application logs in cPanel
   - Ensure all required environment variables are set
   - Verify that the Python version is compatible (3.7+)

4. **Bot Not Responding**:
   - Check if the webhook is properly set up
   - Verify that your bot token is correct
   - Ensure the bot is not blocked by Telegram

### Checking Webhook Status

To check if your webhook is properly set up:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

## Alternative Deployment Options

If cPanel deployment is challenging, consider these alternatives:

1. **PythonAnywhere**:
   - Free tier available
   - Easy Python setup
   - Built-in webhook support

2. **Heroku**:
   - Free tier available (with limitations)
   - Easy deployment via Git
   - Supports webhooks

3. **Railway.app**:
   - Generous free tier
   - Simple deployment
   - Good for small to medium bots

## Support

If you encounter any issues during deployment, please open an issue on the GitHub repository or contact the maintainer.
