# pylint: disable=raise-missing-from

from http import HTTPStatus
from typing import Annotated

from fastapi import Header
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from cumplo_common.database.firestore import firestore_client


async def authenticate(request: Request, x_api_key: Annotated[str | None, Header()] = None) -> None:
    """
    Authenticates a request using the X-API-KEY header

    Args:
        request (Request): The request to authenticate
        x_api_key (Annotated[str  |  None, Header], optional): API key header. Defaults to None.

    Raises:
        HTTPException: When the API key is not present or invalid
    """
    if not x_api_key:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    try:
        user = firestore_client.get_user(x_api_key)
    except (KeyError, ValueError):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    request.state.user = user
