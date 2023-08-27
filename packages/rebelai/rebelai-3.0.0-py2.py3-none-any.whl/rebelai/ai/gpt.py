#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gpt models"""

import typing
from re import Pattern
from uuid import uuid4

import aiohttp
import tls_client  # type: ignore

from .. import const


async def gpt3(
    prompt: str,
    api: str = const.DEFAULT_GPT3_API,
    profile: str = "",
    request_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
    session_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Optional[str]:
    """access to the gpt3 generation model ( proxies suggested )

    *prompt(str): the prompt passed to the ai
    role(str): role of the prompt ( usually system or user )
    profile(str): system profile
    request_args(dict[str, Any] | None): arguments passed to `session.post()`
    session_args(dict[str, Any] | None): arguments passed to `aiohttp.ClientSession()`

    return(str | None): the ai output as a string or nothing if no output was
                        generated"""

    async with aiohttp.ClientSession(**(session_args or {})) as session:
        async with session.post(
            url=api,
            headers={
                "origin": "https://chat9.yqcloud.top",
            },
            json={
                "prompt": f"Always respond in the language of the given prompt, \
default to English. Prompt: {prompt}",
                "network": True,
                "system": profile,
                "withoutContext": False,
                "stream": False,
            },
            **(request_args or {}),
        ) as response:
            return (await response.text()) or None


async def gpt4(
    prompt: str,
    pattern: Pattern[str] = const.GPT4_PATTERN,
    you_params: typing.Optional[typing.Dict[str, typing.Any]] = None,
    tls_client_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
    client_headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
    client_proxies: typing.Optional[typing.Dict[str, typing.Any]] = None,
    api: str = const.DEFAULT_GPT4_API,
    request_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Optional[str]:
    """access to the gpt4 generation model

    *prompt(str): the prompt passed to the ai
    pattern(Pattern[str]): pattern to find all output pieces
    you_params(dict[str, Any] | None): params passed to you.com api
    tls_client_args(dict[str, Any] | None): args passed to `tls_client.Session()`
    client_headers(dict[str, Any] | None): tls client headers in requests
    client_proxies(dict[str, Any] | None): tls client proxies in requests
    api(str): api url for the alpaca model
    request_args(dict[str, Any] | None): arguments passed to `session.post()`
                                         and `session.get()`

    return(str | None): the ai output as a string or nothing if no output was
                        generated"""

    client: tls_client.Session = tls_client.Session(
        client_identifier="chrome112", **(tls_client_args or {})
    )

    client.headers = tls_client.sessions.CaseInsensitiveDict(
        {
            "referer": "https://you.com/search?q=youchat&tbm=youchat",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            **(client_headers or {}),
        }
    )

    client.proxies = client_proxies or {}

    return (
        (
            "".join(
                pattern.findall(
                    client.get(
                        url=api,
                        params={
                            "q": prompt,
                            "page": 1,
                            "count": 10,
                            "safeSearch": "Off",
                            "onShoppingPage": False,
                            "mkt": "",
                            "responseFilter": "WebPages,Translations,TimeZone,\
Computation,RelatedSearches",
                            "domain": "youchat",
                            "queryTraceId": str(uuid4()),
                            "chat": [],
                            **(you_params or {}),
                        },
                        **(request_args or {}),
                    ).text
                    or ""
                )
            )
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )
        or None
    )
