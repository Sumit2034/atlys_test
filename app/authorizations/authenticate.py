from fastapi import HTTPException, Header, status

from app.constants.auth import Auth


def get_authenticated_user(x_token: str = Header(...)):

    if x_token == Auth.AUTH_TOKEN.value:
        return x_token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

