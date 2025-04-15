from typing import Annotated

from fastapi import Depends

from src.adapters import AbstractCache, AbstractAuthService, MessageQueueI, get_auth_client, get_cache, message_queue_client

CacheServiceDep = Annotated[AbstractCache, Depends(get_cache)]
MessageQueueDep = Annotated[MessageQueueI, Depends(message_queue_client)]
AuthServiceDep = Annotated[AbstractAuthService, Depends(get_auth_client)]
