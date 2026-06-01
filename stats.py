"""
stats.py
Vehicle Info System v2.0

Statistics Manager
"""

import json
import os

from config import STATS_FILE


# =====================================
# DEFAULT STATS
# =====================================

DEFAULT_STATS = {
    "total_searches": 0,
    "api_calls": 0,
    "cache_hits": 0,
    "cache_misses": 0,
    "success_requests": 0,
    "failed_requests": 0,
    "offline_hits": 0,
    "total_response_time": 0.0
}


# =====================================
# INIT
# =====================================

def initialize_stats():

    if not os.path.exists(STATS_FILE):

        with open(
            STATS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                DEFAULT_STATS,
                f,
                indent=4
            )


# =====================================
# LOAD
# =====================================

def load_stats():

    initialize_stats()

    try:

        with open(
            STATS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return DEFAULT_STATS.copy()


# =====================================
# SAVE
# =====================================

def save_stats(data):

    with open(
        STATS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# =====================================
# GENERIC INCREMENT
# =====================================

def increment(field, amount=1):

    stats = load_stats()

    if field not in stats:
        return False

    stats[field] += amount

    save_stats(stats)

    return True


# =====================================
# SEARCH COUNT
# =====================================

def add_search():

    increment("total_searches")


# =====================================
# API CALL
# =====================================

def add_api_call():

    increment("api_calls")


# =====================================
# CACHE HIT
# =====================================

def add_cache_hit():

    increment("cache_hits")


# =====================================
# CACHE MISS
# =====================================

def add_cache_miss():

    increment("cache_misses")


# =====================================
# SUCCESS
# =====================================

def add_success():

    increment("success_requests")


# =====================================
# FAILURE
# =====================================

def add_failure():

    increment("failed_requests")


# =====================================
# OFFLINE HIT
# =====================================

def add_offline_hit():

    increment("offline_hits")


# =====================================
# RESPONSE TIME
# =====================================

def add_response_time(ms):

    stats = load_stats()

    stats["total_response_time"] += float(ms)

    save_stats(stats)


# =====================================
# AVG RESPONSE
# =====================================

def average_response_time():

    stats = load_stats()

    total_requests = (
        stats["success_requests"]
        + stats["failed_requests"]
    )

    if total_requests == 0:
        return 0

    return round(
        stats["total_response_time"]
        / total_requests,
        2
    )


# =====================================
# SUCCESS RATE
# =====================================

def success_rate():

    stats = load_stats()

    total = (
        stats["success_requests"]
        + stats["failed_requests"]
    )

    if total == 0:
        return 0

    return round(
        (stats["success_requests"] / total)
        * 100,
        2
    )


# =====================================
# DASHBOARD DATA
# =====================================

def dashboard():

    stats = load_stats()

    return {
        "Total Searches":
            stats["total_searches"],

        "API Calls":
            stats["api_calls"],

        "Cache Hits":
            stats["cache_hits"],

        "Cache Misses":
            stats["cache_misses"],

        "Offline Hits":
            stats["offline_hits"],

        "Success Requests":
            stats["success_requests"],

        "Failed Requests":
            stats["failed_requests"],

        "Success Rate":
            f"{success_rate()}%",

        "Avg Response":
            f"{average_response_time()} ms"
    }


# =====================================
# RESET STATS
# =====================================

def reset_stats():

    save_stats(
        DEFAULT_STATS.copy()
    )

    return True


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    add_search()
    add_api_call()
    add_cache_hit()
    add_success()
    add_response_time(123)

    print(
        dashboard()
    )
