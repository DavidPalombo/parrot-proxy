import json

from parrot_proxy.db.database import SessionLocal
from parrot_proxy.db.models import ReplayHistoryModel, RequestModel

def save_request(parsed_request: dict):
    db = SessionLocal()

    request = RequestModel(
        method = parsed_request["method"],
        path = parsed_request["path"],
        version = parsed_request["version"],
        headers = json.dumps(parsed_request["headers"]),
        body = parsed_request["body"],
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    db.close()

    return request

def get_all_requests():
    db = SessionLocal()

    requests = db.query(RequestModel).all()

    db.close()

    return requests

def get_request_by_id(request_id: int):
    db = SessionLocal()

    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()

    db.close()

    return request

def export_request_raw(request_id: int):
    request = get_request_by_id(request_id)

    if not request:
        return None

    headers = json.loads(request.headers)

    raw = f"{request.method} {request.path} {request.version}\n"

    for k, v in headers.items():
        raw += f"{k}: {v}\n"

    raw += "\n"
    raw += request.body or ""

    return raw

def save_replay_history(
        request_id: int,
        replay_method: str,
        replay_url: str,
        status_code: int,
        response_length: int,
        reflection_detected: bool,
        diff_status_changed: bool,
        diff_body_changed: bool,
):
    db = SessionLocal()

    replay = ReplayHistoryModel(
        request_id = request_id,
        replay_method = replay_method,
        replay_url = replay_url,
        status_code = status_code,
        response_length = response_length,
        reflection_detected = reflection_detected,
        diff_status_changed = diff_status_changed,
        diff_body_changed = diff_body_changed,
    )

    db.add(replay)
    db.commit()
    db.refresh(replay)

    db.close()

    return replay

def get_replay_history(request_id: int):
    db = SessionLocal()

    history = (
        db.query(ReplayHistoryModel).filter(ReplayHistoryModel.request_id == request_id).all()
    )

    db.close()

    return history