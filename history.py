"""
history.py
Vehicle Info System v2.0

Search History Manager
"""

import json
import os
from datetime import datetime

from config import HISTORY_FILE


# =====================================
# INITIALIZE HISTORY FILE
# =====================================

def initialize_history():

    if not os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [],
                f,
                indent=4
            )


# =====================================
# LOAD HISTORY
# =====================================

def load_history():

    initialize_history()

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return []


# =====================================
# SAVE HISTORY
# =====================================

def save_history(history):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================
# ADD SEARCH ENTRY
# =====================================

def add_search(
    rc,
    status="SUCCESS",
    source="API"
):

    history = load_history()

    entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "rc": rc.upper(),
        "status": status,
        "source": source
    }

    history.append(entry)

    save_history(history)


# =====================================
# GET ALL HISTORY
# =====================================

def get_history():

    return load_history()


# =====================================
# LAST N SEARCHES
# =====================================

def get_recent_searches(limit=10):

    history = load_history()

    return history[-limit:][::-1]


# =====================================
# SEARCH BY RC
# =====================================

def search_history(rc):

    rc = rc.upper()

    history = load_history()

    result = []

    for item in history:

        if item["rc"] == rc:

            result.append(item)

    return result


# =====================================
# TOTAL SEARCH COUNT
# =====================================

def total_searches():

    return len(load_history())


# =====================================
# UNIQUE SEARCH COUNT
# =====================================

def unique_searches():

    history = load_history()

    unique = set()

    for item in history:

        unique.add(item["rc"])

    return len(unique)


# =====================================
# TOP SEARCHED RCs
# =====================================

def top_searched(limit=10):

    history = load_history()

    counter = {}

    for item in history:

        rc = item["rc"]

        counter[rc] = (
            counter.get(rc, 0) + 1
        )

    ranked = sorted(
        counter.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:limit]


# =====================================
# SUCCESS / FAILED STATS
# =====================================

def history_stats():

    history = load_history()

    success = 0
    failed = 0

    for item in history:

        if item["status"] == "SUCCESS":

            success += 1

        else:

            failed += 1

    return {
        "total": len(history),
        "success": success,
        "failed": failed
    }


# =====================================
# DELETE HISTORY
# =====================================

def clear_history():

    save_history([])

    return True


# =====================================
# DELETE SPECIFIC RC HISTORY
# =====================================

def delete_rc_history(rc):

    rc = rc.upper()

    history = load_history()

    filtered = []

    removed = 0

    for item in history:

        if item["rc"] == rc:

            removed += 1

        else:

            filtered.append(item)

    save_history(filtered)

    return removed


# =====================================
# EXPORT HISTORY
# =====================================

def export_history():

    return load_history()


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    add_search(
        "UP14AB1234",
        "SUCCESS",
        "CACHE"
    )

    add_search(
        "DL8CAF1234",
        "SUCCESS",
        "API"
    )

    print(
        get_recent_searches()
    )

    print(
        top_searched()
    )

    print(
        history_stats()
    )
