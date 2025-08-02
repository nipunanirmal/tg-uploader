import os

# In-memory key-value store
DB = {
    "ALLCHATS": {"USERS": []},
    "BLACKLIST": {"USERS": []}
}

# Initialize database function
def init_db():
    """Initialize the in-memory database"""
    # Nothing to do for in-memory DB, it's already initialized above
    # This function exists for compatibility with the bot.py initialization
    return True

def get_stuff(key):
    """Get value from in-memory database"""
    if key not in DB:
        DB[key] = {}
    return DB[key]

def set_stuff(key, value):
    """Set value in in-memory database"""
    DB[key] = value
    return True