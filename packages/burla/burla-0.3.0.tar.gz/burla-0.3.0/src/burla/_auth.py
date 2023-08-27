import json
import webbrowser
import requests
from time import sleep
from uuid import uuid4
from pathlib import Path
from typing import Tuple

from appdirs import user_config_dir

from burla import _BURLA_SERVICE_URL

AUTH_TIMEOUT_SECONDS = 180
CONFIG_PATH = Path(user_config_dir(appname="burla", appauthor="burla")) / Path("burla_config.json")


class AuthTimeoutException(Exception):
    def __init__(self):
        super().__init__("Timed out waiting for authentication flow to complete.")


class AuthException(Exception):
    def __init__(self):
        super().__init__("Unauthenticated. Please run `burla login` to create an account or login.")


def auth_headers_from_local_config() -> Tuple[str, str]:
    if not CONFIG_PATH.exists():
        raise AuthException()
    else:
        auth_info = json.loads(CONFIG_PATH.read_text())
        return {"email": auth_info["email"], "Authorization": f"Bearer {auth_info['api_key']}"}


def _get_auth_creds(client_id, attempt=0):
    if attempt == AUTH_TIMEOUT_SECONDS / 2:
        raise AuthTimeoutException()

    sleep(2)
    response = requests.get(f"{_BURLA_SERVICE_URL}/v1/keys/{client_id}")

    if response.status_code == 404:
        return _get_auth_creds(client_id, attempt=attempt + 1)
    else:
        response.raise_for_status()
        return response.json()["api_key"], response.json()["email"]


def login():
    client_id = uuid4().hex
    webbrowser.open(f"{_BURLA_SERVICE_URL}/v1/login/{client_id}")
    api_key, email = _get_auth_creds(client_id)

    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.touch()
    CONFIG_PATH.write_text(json.dumps({"api_key": api_key, "email": email}))
