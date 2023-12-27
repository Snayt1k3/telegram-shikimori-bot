from pydantic import BaseModel


class Response(BaseModel):
    status: int
    text: dict | list
    additionalInfo: dict | None = None


class Headers(BaseModel):
    ContentType: str = "application/json"


class ShikiHeaders(Headers):
    user_agent: str

    def to_dict(self):
        return {
            "Content-Type": self.ContentType,
            "User-Agent": self.user_agent,
        }


class ShikiAuthHeaders(ShikiHeaders):
    authorization: str

    def to_dict(self):
        return {
            "Authorization": f"Bearer {self.authorization}",
            "Content-Type": self.ContentType,
            "User-Agent": self.user_agent,
        }


class ShikiRefreshHeaders(Headers):
    refresh_token: str
    access_token: str
    grant_type: str = "refresh_token"
    client_id: str
    client_secret: str

    def to_dict(self):
        return {
            "Content-Type": self.ContentType,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
