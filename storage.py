import json
import os
import re

VALID_CARD_TYPES = ("visitor", "student", "staff")
VALID_STATUSES = ("requested", "approved", "issued", "returned")
REQUIRED_KEYS = {"id", "fellow_id", "card_type", "status", "approved_by"}
ID_PATTERN = re.compile(r"A[0-9]{3,}")

_requests = {}


def is_valid_id(request_id):
    return isinstance(request_id, str) and ID_PATTERN.fullmatch(request_id) is not None


def _next_id():
    if not _requests:
        return "A001"
    highest = max(int(rid[1:]) for rid in _requests)
    return f"A{highest + 1:03d}"


def clear_requests():
    _requests.clear()


def create_request(fellow_id, card_type):
    if not isinstance(fellow_id, str):
        raise ValueError("fellow_id must be text")
    if not fellow_id.strip():
        raise ValueError("fellow_id cannot be blank")
    if not isinstance(card_type, str):
        raise ValueError("card_type must be text")
    if card_type not in VALID_CARD_TYPES:
        raise ValueError(f"card_type must be one of {VALID_CARD_TYPES}")

    record = {
        "id": _next_id(),
        "fellow_id": fellow_id.strip(),
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }
    _requests[record["id"]] = record
    return dict(record)


def get_request(request_id):
    if not is_valid_id(request_id):
        raise ValueError(f"malformed request ID: {request_id!r}")
    if request_id not in _requests:
        raise ValueError(f"unknown request ID: {request_id}")
    return dict(_requests[request_id])


def list_requests():
    return [dict(_requests[rid]) for rid in sorted(_requests)]


def update_request(request_id, status, approved_by):
    if not is_valid_id(request_id):
        raise ValueError(f"malformed request ID: {request_id!r}")
    if request_id not in _requests:
        raise ValueError(f"unknown request ID: {request_id}")
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status!r}")
    updated = dict(_requests[request_id])
    updated["status"] = status
    updated["approved_by"] = approved_by
    _requests[request_id] = updated
    return dict(updated)

def save_requests(path):
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump([_requests[rid] for rid in sorted(_requests)], f, indent=2)
        os.replace(tmp_path, path)
    except (OSError, TypeError) as error:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise ValueError(f"could not save to {path}: {error}")


def _validate_record(item, position):
    if not isinstance(item, dict):
        raise ValueError(f"record {position} is not an object")
    if set(item.keys()) != REQUIRED_KEYS:
        raise ValueError(f"record {position} has missing or extra keys")
    if not is_valid_id(item["id"]):
        raise ValueError(f"record {position} has a malformed id")
    if not isinstance(item["fellow_id"], str) or not item["fellow_id"].strip():
        raise ValueError(f"record {position} has a blank fellow_id")
    if item["card_type"] not in VALID_CARD_TYPES:
        raise ValueError(f"record {position} has an invalid card_type")
    if item["status"] not in VALID_STATUSES:
        raise ValueError(f"record {position} has an invalid status")
    approver = item["approved_by"]
    if approver is not None and (not isinstance(approver, str) or not approver.strip()):
        raise ValueError(f"record {position} has an invalid approved_by")
    if item["status"] == "requested" and approver is not None:
        raise ValueError(f"record {position} is 'requested' but has an approver")
    if item["status"] != "requested" and approver is None:
        raise ValueError(f"record {position} is '{item['status']}' but has no approver")


def load_requests(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}")
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error}")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"could not read {path}: {error}")

    if not isinstance(data, list):
        raise ValueError("file must contain a list of requests")

    loaded = {}
    for position, item in enumerate(data, start=1):
        _validate_record(item, position)
        if item["id"] in loaded:
            raise ValueError(f"duplicate id {item['id']}")
        loaded[item["id"]] = dict(item)

    _requests.clear()
    _requests.update(loaded)
