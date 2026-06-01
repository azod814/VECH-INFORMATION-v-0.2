"""
exports.py
Vehicle Info System v2.0

Export Manager
"""

import os
import csv
import json
from datetime import datetime

from config import (
    EXPORT_DIR,
    RESULT_DIR,
    ENABLE_JSON_EXPORT,
    ENABLE_CSV_EXPORT,
    ENABLE_TXT_EXPORT
)


# =====================================
# SAFE FILENAME
# =====================================

def safe_filename(name):

    invalid_chars = r'\/:*?"<>|'

    for ch in invalid_chars:
        name = name.replace(ch, "_")

    return name


# =====================================
# TIMESTAMP
# =====================================

def timestamp():

    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


# =====================================
# EXPORT PATH
# =====================================

def build_path(rc, ext):

    rc = safe_filename(rc)

    return os.path.join(
        EXPORT_DIR,
        f"{rc}.{ext}"
    )


# =====================================
# JSON EXPORT
# =====================================

def export_json(rc, data):

    if not ENABLE_JSON_EXPORT:
        return None

    path = build_path(rc, "json")

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return path


# =====================================
# TXT EXPORT
# =====================================

def export_txt(rc, data):

    if not ENABLE_TXT_EXPORT:
        return None

    path = build_path(rc, "txt")

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"Vehicle Report\n"
        )

        f.write(
            "=" * 50 + "\n\n"
        )

        f.write(
            f"RC NUMBER : {rc}\n\n"
        )

        for key, value in data.items():

            field = (
                str(key)
                .replace("_", " ")
                .upper()
            )

            f.write(
                f"{field} : {value}\n"
            )

    return path


# =====================================
# CSV EXPORT
# =====================================

def export_csv(rc, data):

    if not ENABLE_CSV_EXPORT:
        return None

    path = build_path(rc, "csv")

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["FIELD", "VALUE"]
        )

        for key, value in data.items():

            writer.writerow(
                [key, value]
            )

    return path


# =====================================
# SAVE RAW RESULT
# =====================================

def save_result(rc, data):

    path = os.path.join(
        RESULT_DIR,
        f"{safe_filename(rc)}.json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return path


# =====================================
# EXPORT ALL
# =====================================

def export_all(rc, data):

    results = {}

    json_file = export_json(
        rc,
        data
    )

    txt_file = export_txt(
        rc,
        data
    )

    csv_file = export_csv(
        rc,
        data
    )

    results["json"] = json_file
    results["txt"] = txt_file
    results["csv"] = csv_file

    return results


# =====================================
# BULK CSV EXPORT
# =====================================

def export_bulk_csv(
    filename,
    records
):

    path = os.path.join(
        EXPORT_DIR,
        f"{filename}.csv"
    )

    if not records:
        return None

    headers = set()

    for item in records:

        headers.update(
            item.keys()
        )

    headers = list(headers)

    with open(
        path,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=headers
        )

        writer.writeheader()

        for item in records:

            writer.writerow(item)

    return path


# =====================================
# EXPORT SUMMARY
# =====================================

def export_summary():

    files = os.listdir(
        EXPORT_DIR
    )

    return {
        "total_files": len(files),
        "files": files
    }


# =====================================
# CLEAR EXPORTS
# =====================================

def clear_exports():

    removed = 0

    for file in os.listdir(
        EXPORT_DIR
    ):

        try:

            os.remove(
                os.path.join(
                    EXPORT_DIR,
                    file
                )
            )

            removed += 1

        except Exception:
            pass

    return removed


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    sample = {
        "owner": "Demo User",
        "vehicle": "Swift",
        "fuel": "Petrol",
        "year": 2022
    }

    export_all(
        "UP14AB1234",
        sample
    )

    print(
        export_summary()
    )
