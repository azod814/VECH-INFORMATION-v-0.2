"""
cache.py
Vehicle Info System v2.0

Cache Management Module
"""

import os
import json
import time
import hashlib

from config import (
    CACHE_DIR,
    CACHE_EXPIRY_DAYS
)


# ==========================================
# HASHED CACHE FILE NAME
# ==========================================

def cache_filename(key: str) -> str:
    """
    Convert lookup key into safe filename
    """

    hashed = hashlib.md5(
        key.encode()
    ).hexdigest()

    return os.path.join(
        CACHE_DIR,
        f"{hashed}.json"
    )


# ==========================================
# SAVE CACHE
# ==========================================

def save_cache(key, data):
    """
    Save data into cache
    """

    file_path = cache_filename(key)

    payload = {
        "created_at": time.time(),
        "data": data
    }

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            payload,
            f,
            indent=4,
            ensure_ascii=False
        )

    return True


# ==========================================
# LOAD CACHE
# ==========================================

def load_cache(key):
    """
    Load cache if exists
    """

    file_path = cache_filename(key)

    if not os.path.exists(file_path):
        return None

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            payload = json.load(f)

        return payload

    except Exception:

        return None


# ==========================================
# CACHE EXISTS
# ==========================================

def cache_exists(key):

    return os.path.exists(
        cache_filename(key)
    )


# ==========================================
# CACHE AGE
# ==========================================

def get_cache_age_days(key):
    """
    Returns cache age in days
    """

    payload = load_cache(key)

    if not payload:
        return None

    created = payload.get(
        "created_at",
        0
    )

    age_seconds = (
        time.time() - created
    )

    age_days = age_seconds / 86400

    return round(age_days, 2)


# ==========================================
# EXPIRED ?
# ==========================================

def is_cache_expired(key):

    age = get_cache_age_days(key)

    if age is None:
        return True

    return age > CACHE_EXPIRY_DAYS


# ==========================================
# GET VALID CACHE
# ==========================================

def get_cache(key):
    """
    Returns cached data if valid
    """

    if not cache_exists(key):
        return None

    if is_cache_expired(key):
        return None

    payload = load_cache(key)

    if not payload:
        return None

    return payload.get("data")


# ==========================================
# DELETE CACHE
# ==========================================

def delete_cache(key):

    file_path = cache_filename(key)

    if os.path.exists(file_path):

        os.remove(file_path)

        return True

    return False


# ==========================================
# CLEAR ALL CACHE
# ==========================================

def clear_cache():

    removed = 0

    for file in os.listdir(CACHE_DIR):

        if file.endswith(".json"):

            try:

                os.remove(
                    os.path.join(
                        CACHE_DIR,
                        file
                    )
                )

                removed += 1

            except Exception:
                pass

    return removed


# ==========================================
# CLEAN EXPIRED CACHE
# ==========================================

def clean_expired_cache():

    removed = 0

    for file in os.listdir(CACHE_DIR):

        path = os.path.join(
            CACHE_DIR,
            file
        )

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                payload = json.load(f)

            created = payload.get(
                "created_at",
                0
            )

            age_days = (
                time.time() - created
            ) / 86400

            if age_days > CACHE_EXPIRY_DAYS:

                os.remove(path)

                removed += 1

        except Exception:

            pass

    return removed


# ==========================================
# CACHE STATS
# ==========================================

def cache_stats():

    total_files = 0
    total_size = 0

    for file in os.listdir(CACHE_DIR):

        path = os.path.join(
            CACHE_DIR,
            file
        )

        if os.path.isfile(path):

            total_files += 1

            total_size += os.path.getsize(
                path
            )

    return {
        "files": total_files,
        "size_kb": round(
            total_size / 1024,
            2
        )
    }


# ==========================================
# OFFLINE CACHE ACCESS
# ==========================================

def get_offline_cache(key):
    """
    Return cache even if expired
    """

    payload = load_cache(key)

    if not payload:
        return None

    return payload.get("data")


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    sample = {
        "vehicle": "Sample Car",
        "fuel": "Petrol"
    }

    save_cache(
        "UP14AB1234",
        sample
    )

    print(
        get_cache(
            "UP14AB1234"
        )
    )

    print(
        cache_stats()
    )
