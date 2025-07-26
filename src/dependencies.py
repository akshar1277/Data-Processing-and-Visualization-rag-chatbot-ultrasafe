from fastapi import Request, HTTPException


def get_current_user(request: Request):
    if not request.state.user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return request.state.user
