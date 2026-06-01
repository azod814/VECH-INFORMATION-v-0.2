"""
validator.py
Vehicle Info System v2.0

Input Validation Module
"""

import re
from config import MAX_BATCH_LOOKUP


# =====================================
# RC NUMBER VALIDATION
# =====================================

RC_PATTERN = re.compile(
    r'^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{1,4}$'
)


def clean_rc(rc: str) -> str:
    """
    Clean user input

    Example:
    up14 ab1234
    ->
    UP14AB1234
    """

    if not rc:
        return ""

    rc = str(rc).strip().upper()
    rc = rc.replace(" ", "")

    return rc


def validate_rc(rc: str) -> bool:
    """
    Validate RC Number

    Example:
    UP14AB1234 -> True
    DL8CAF1234 -> True
    INVALID123 -> False
    """

    rc = clean_rc(rc)

    return bool(RC_PATTERN.match(rc))


# =====================================
# BATCH VALIDATION
# =====================================

def validate_batch(rc_list):
    """
    Validate list of RC numbers

    Returns:
    {
        "valid": [],
        "invalid": []
    }
    """

    valid = []
    invalid = []

    for rc in rc_list:

        rc = clean_rc(rc)

        if validate_rc(rc):
            valid.append(rc)
        else:
            invalid.append(rc)

    return {
        "valid": valid,
        "invalid": invalid
    }


# =====================================
# REMOVE DUPLICATES
# =====================================

def remove_duplicates(rc_list):
    """
    Remove duplicate RC entries
    """

    seen = set()
    unique = []

    for rc in rc_list:

        rc = clean_rc(rc)

        if rc not in seen:
            seen.add(rc)
            unique.append(rc)

    return unique


# =====================================
# BATCH LIMIT CHECK
# =====================================

def check_batch_limit(rc_list):
    """
    Prevent huge batch requests
    """

    return len(rc_list) <= MAX_BATCH_LOOKUP


# =====================================
# FILTER VALID RCs ONLY
# =====================================

def get_valid_rcs(rc_list):

    result = []

    for rc in rc_list:

        rc = clean_rc(rc)

        if validate_rc(rc):
            result.append(rc)

    return result


# =====================================
# FILTER INVALID RCs ONLY
# =====================================

def get_invalid_rcs(rc_list):

    result = []

    for rc in rc_list:

        rc = clean_rc(rc)

        if not validate_rc(rc):
            result.append(rc)

    return result


# =====================================
# MASK TEXT
# =====================================

def mask_text(text):
    """
    Example:

    Suryansh Sharma

    ->
    S*******h S****a
    """

    if not text:
        return "N/A"

    words = str(text).split()

    masked_words = []

    for word in words:

        if len(word) <= 2:
            masked_words.append("*" * len(word))
            continue

        masked = (
            word[0]
            + "*" * (len(word) - 2)
            + word[-1]
        )

        masked_words.append(masked)

    return " ".join(masked_words)


# =====================================
# TEST BLOCK
# =====================================

if __name__ == "__main__":

    test_rcs = [
        "up14ab1234",
        "DL8CAF1234",
        "invalid",
        "hr26aa0001",
        "UP14AB1234"
    ]

    print("Original:")
    print(test_rcs)

    print("\nUnique:")
    print(remove_duplicates(test_rcs))

    print("\nValidation:")
    print(validate_batch(test_rcs))

    print("\nMasked:")
    print(mask_text("Suryansh Sharma"))
