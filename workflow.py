import storage


def _check_approver(approved_by):
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("approver cannot be blank")
    return approved_by.strip()


def _require_status(record, expected, action):
    if record["status"] != expected:
        raise ValueError(
            f"cannot {action} {record['id']}: status is '{record['status']}', "
            f"must be '{expected}'"
        )


def approve_request(request_id, approved_by):
    record = storage.get_request(request_id)
    approver = _check_approver(approved_by)
    _require_status(record, "requested", "approve")
    return storage.update_request(request_id, "approved", approver)


def issue_card(request_id):
    record = storage.get_request(request_id)
    _require_status(record, "approved", "issue")
    if not record["approved_by"]:
        raise ValueError(f"cannot issue {request_id}: no approver recorded")
    return storage.update_request(request_id, "issued", record["approved_by"])


def return_card(request_id):
    record = storage.get_request(request_id)
    _require_status(record, "issued", "return")
    return storage.update_request(request_id, "returned", record["approved_by"])
    