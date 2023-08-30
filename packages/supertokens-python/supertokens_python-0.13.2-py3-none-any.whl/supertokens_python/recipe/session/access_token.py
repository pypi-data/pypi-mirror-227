# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import jwt
from jwt.exceptions import DecodeError, PyJWKClientError

from supertokens_python.logger import log_debug_message
from supertokens_python.utils import get_timestamp_ms

from .exceptions import raise_try_refresh_token_exception
from .jwks import JWKClient, JWKSRequestError, PyJWK
from .jwt import ParsedJWTInfo


def sanitize_string(s: Any) -> Union[str, None]:
    if s == "":
        return s

    if not isinstance(s, str):
        return None

    return s.strip()


def sanitize_number(n: Any) -> Union[Union[int, float], None]:
    if isinstance(n, (int, float)):
        return n

    return None


def get_info_from_access_token(
    jwt_info: ParsedJWTInfo,
    jwk_clients: List[JWKClient],
    do_anti_csrf_check: bool,
):
    try:
        payload: Optional[Dict[str, Any]] = None
        client: Optional[JWKClient] = None
        keys: Optional[List[PyJWK]] = None

        # Get the keys from the first available client
        for c in jwk_clients:
            try:
                client = c
                keys = c.get_latest_keys()
                break
            except JWKSRequestError:
                continue

        if keys is None or client is None:
            raise PyJWKClientError("No key found")

        if jwt_info.version < 3:
            # It won't have kid. So we'll have to try the token against all the keys from all the jwk_clients
            # If any of them work, we'll use that payload
            for k in keys:
                try:
                    payload = jwt.decode(jwt_info.raw_token_string, k.key, algorithms=["RS256"])  # type: ignore
                    break
                except DecodeError:
                    pass

        elif jwt_info.version >= 3:
            matching_key = client.get_matching_key_from_jwt(jwt_info.raw_token_string)
            payload = jwt.decode(  # type: ignore
                jwt_info.raw_token_string,
                matching_key.key,  # type: ignore
                algorithms=["RS256"],
                options={"verify_signature": True, "verify_exp": True},
            )

        if payload is None:
            raise DecodeError("Could not decode the token")

        validate_access_token_structure(payload, jwt_info.version)

        if jwt_info.version == 2:
            user_id = sanitize_string(payload.get("userId"))
            expiry_time = sanitize_number(payload.get("expiryTime"))
            time_created = sanitize_number(payload.get("timeCreated"))
            user_data = payload.get("userData")
        else:
            user_id = sanitize_string(payload.get("sub"))
            expiry_time = sanitize_number(payload.get("exp", 0) * 1000)
            time_created = sanitize_number(payload.get("iat", 0) * 1000)
            user_data = payload

        session_handle = sanitize_string(payload.get("sessionHandle"))
        refresh_token_hash_1 = sanitize_string(payload.get("refreshTokenHash1"))
        parent_refresh_token_hash_1 = sanitize_string(
            payload.get("parentRefreshTokenHash1")
        )
        anti_csrf_token = sanitize_string(payload.get("antiCsrfToken"))

        if anti_csrf_token is None and do_anti_csrf_check:
            raise Exception("Access token does not contain the anti-csrf token")

        assert isinstance(expiry_time, int)

        if expiry_time < get_timestamp_ms():
            raise Exception("Access token expired")

        return {
            "sessionHandle": session_handle,
            "userId": user_id,
            "refreshTokenHash1": refresh_token_hash_1,
            "parentRefreshTokenHash1": parent_refresh_token_hash_1,
            "userData": user_data,
            "antiCsrfToken": anti_csrf_token,
            "expiryTime": expiry_time,
            "timeCreated": time_created,
        }
    except Exception as e:
        log_debug_message(
            "getSession: Returning TRY_REFRESH_TOKEN because failed to decode access token"
        )
        raise_try_refresh_token_exception(e)


def validate_access_token_structure(payload: Dict[str, Any], version: int) -> None:
    if version >= 3:
        if (
            not isinstance(payload.get("sub"), str)
            or not isinstance(payload.get("exp"), int)
            or not isinstance(payload.get("iat"), int)
            or not isinstance(payload.get("sessionHandle"), str)
            or not isinstance(payload.get("refreshTokenHash1"), str)
        ):
            raise Exception(
                "Access token does not contain all the information. Maybe the structure has changed?"
            )
    elif (
        not isinstance(payload.get("sessionHandle"), str)
        or payload.get("userData") is None
        or not isinstance(payload.get("refreshTokenHash1"), str)
        or not isinstance(payload.get("expiryTime"), int)
        or not isinstance(payload.get("timeCreated"), int)
    ):
        raise Exception(
            "Access token does not contain all the information. Maybe the structure has changed?"
        )
