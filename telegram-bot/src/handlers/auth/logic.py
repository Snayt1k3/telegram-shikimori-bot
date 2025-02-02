from src.adapters.http import BaseHttpAdapter
from src.config.http import http_settings
from src.handlers.auth.dto import UserResponse


async def get_uri(http: BaseHttpAdapter) -> str:
    response = await http.get(http_settings.AUTH_URL + "/uri")
    return response["data"].get("uri", "")


async def check_user(http: BaseHttpAdapter, id_telegram: int) -> UserResponse | None:
    response = await http.post(
        http_settings.AUTH_URL + "/check", json={"user_id": id_telegram}
    )

    if not response["data"]:
        return None

    return response["data"]


async def auth_user(
    http: BaseHttpAdapter, id_telegram: int, code: str
) -> UserResponse | None:
    response = await http.post(
        http_settings.AUTH_URL, json={"user_id": id_telegram, "token": code}
    )

    if not response["data"]:
        return None

    return response["data"]
