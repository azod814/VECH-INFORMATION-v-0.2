"""
config.py
Vehicle Info System v2.0
Central Configuration File
"""

import os

# ==========================
# APP INFO
# ==========================

APP_NAME = "Vehicle Information System"
VERSION = "2.0"
AUTHOR = "azod814"

# ==========================
# THEME
# ==========================

THEME_COLOR = "#0f9d58"

# ==========================
# DIRECTORIES
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_DIR = os.path.join(BASE_DIR, "cache")
LOG_DIR = os.path.join(BASE_DIR, "logs")
RESULT_DIR = os.path.join(BASE_DIR, "results")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
HISTORY_DIR = os.path.join(BASE_DIR, "history")

# ==========================
# FILES
# ==========================

ACTIVITY_LOG = os.path.join(LOG_DIR, "activity.log")

STATS_FILE = os.path.join(LOG_DIR, "stats.json")

HISTORY_FILE = os.path.join(
    HISTORY_DIR,
    "search_history.json"
)

SETTINGS_FILE = os.path.join(
    BASE_DIR,
    "settings.json"
)

# ==========================
# CACHE
# ==========================

CACHE_EXPIRY_DAYS = 7

# ==========================
# API CONFIG
# ==========================

REQUEST_TIMEOUT = 15

APIS = [
    "https://api1.com/lookup",
    "https://api2.com/lookup",
    "https://api3.com/lookup"
]

# ==========================
# EXPORT OPTIONS
# ==========================

ENABLE_JSON_EXPORT = True
ENABLE_CSV_EXPORT = True
ENABLE_TXT_EXPORT = True

# ==========================
# PRIVACY
# ==========================

MASK_OWNER_NAME = True

# ==========================
# SEARCH LIMITS
# ==========================

MAX_BATCH_LOOKUP = 50

# ==========================
# DEFAULT SETTINGS
# ==========================

DEFAULT_SETTINGS = {
    "theme_color": THEME_COLOR,
    "mask_owner_name": True,
    "cache_expiry_days": CACHE_EXPIRY_DAYS,
    "json_export": True,
    "csv_export": True,
    "txt_export": True
}

# ==========================
# CREATE REQUIRED FOLDERS
# ==========================

REQUIRED_DIRS = [
    CACHE_DIR,
    LOG_DIR,
    RESULT_DIR,
    EXPORT_DIR,
    HISTORY_DIR
]
