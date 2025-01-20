from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from gigachat.api.utils import build_headers
from gigachat.exceptions import AuthenticationError, ResponseError
from gigachat.models.threads import Threads


def _get_kwargs(
    *,
    assistants_ids: Optional[List[str]] = None,
    limit: Optional[int] = None,
    before: Optional[int] = None,
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    headers = build_headers(access_token)
    params: Dict[str, Any] = {}
    if assistants_ids:
        params["assistants_ids"] = assistants_ids
    if limit:
        params["limit"] = limit
    if before:
        params["before"] = before
    params = {
        "method": "GET",
        "url": "/threads",
        "headers": headers,
        "params": params,
    }
    return params


def _build_response(response: httpx.Response) -> Threads:
    if response.status_code == HTTPStatus.OK:
        return Threads(**response.json())
    elif response.status_code == HTTPStatus.UNAUTHORIZED:
        raise AuthenticationError(response.url, response.status_code, response.content, response.headers)
    else:
        raise ResponseError(response.url, response.status_code, response.content, response.headers)


def sync(
    client: httpx.Client,
    *,
    assistants_ids: Optional[List[str]] = None,
    limit: Optional[int] = None,
    before: Optional[int] = None,
    access_token: Optional[str] = None,
) -> Threads:
    """Получение перечня тредов"""
    kwargs = _get_kwargs(
        assistants_ids=assistants_ids,
        limit=limit,
        before=before,
        access_token=access_token,
    )
    response = client.request(**kwargs)
    return _build_response(response)


async def asyncio(
    client: httpx.AsyncClient,
    *,
    assistants_ids: Optional[List[str]] = None,
    limit: Optional[int] = None,
    before: Optional[int] = None,
    access_token: Optional[str] = None,
) -> Threads:
    """Получение перечня тредов"""
    kwargs = _get_kwargs(
        assistants_ids=assistants_ids,
        limit=limit,
        before=before,
        access_token=access_token,
    )
    response = await client.request(**kwargs)
    return _build_response(response)
