import os
import json
from getpass import getpass
from pathlib import Path

from .apis import OpeniAPI
from .utils import logger, constants
from .utils.logger import *

log = logger.setup_logger()


def get_login_user(token: str = None, endpoint: str = None):
    try:
        api = OpeniAPI(token=token, endpoint=endpoint)
        response = api.user_my_info()
        username = response.json()["username"]
        return username, api.endpoint
    except:
        msg = f"无法获取当前用户信息"
        log.error(msg)
        raise ValueError(msg)


def login(token: str = None, endpoint: str = constants.API.DEFAULT_ENDPOINT) -> None:
    print(
        """\n
             ██████╗   ██████╗  ███████╗  ███╗   ██╗  ██████╗
            ██╔═══██╗  ██╔══██╗ ██╔════╝  ████╗  ██║    ██╔═╝
            ██║   ██║  ██████╔╝ █████╗    ██╔██╗ ██║    ██║
            ██║   ██║  ██╔═══╝  ██╔══╝    ██║╚██╗██║    ██║
            ╚██████╔╝  ██║      ███████╗  ██║ ╚████║  ██████╗
             ╚═════╝   ╚═╝      ╚══════╝  ╚═╝  ╚═══╝  ╚═════╝\n
         """
    )
    endpoint = endpoint[:-1] if endpoint[-1] == "/" else endpoint

    if token is None:
        print(f"点击链接获取令牌并复制粘贴到下列输入栏 {endpoint}/user/settings/applications \n")
        print(
            f"[WARNING] 若本机已存在登录令牌，本次输入的令牌会将其覆盖 \n"
            "          若粘贴时切换了本窗口，请先按 退格键⇦ 删除多余空格\n"
        )
        token = getpass(prompt="  🔒 token: ")

    # _login(token=token, endpoint=endpoint)

    try:
        username, api_endpoint = get_login_user(token=token, endpoint=endpoint)
        msg = (
            f"\n  Your token was saved to `{constants.PATH.TOKEN_PATH}`\n"
            f"  Successfully logged in as `{username}` @{api_endpoint}!\n"
        )
        Path(constants.PATH.TOKEN_PATH).write_text(
            json.dumps({"endpoint": endpoint, "token": token})
        )
        log.info(msg)
        print(msg)
    except:
        # os.remove(constants.PATH.TOKEN_PATH)
        msg = "\n  ❌ login failed: invalid token!\n"
        log.error(msg)
        # raise ValueError(msg)
        print(msg)


def whoami() -> None:
    try:
        username, endpoint = get_login_user()
        msg = f"\n`{username}` @{endpoint}\n"
        log.info(msg)
        print(msg)
    except:
        msg = f"\n无法获取当前用户信息, 请检查网络或 {constants.PATH.TOKEN_PATH} \n"
        log.info(msg)
        print(msg)


def logout() -> None:
    try:
        username, _ = get_login_user()
        os.remove(constants.PATH.TOKEN_PATH)
        msg = f"\n`{username}` successfully logged out.\n"
        log.info(msg)
        print(msg)
    except:
        msg = "\nCurrently not logged in.\n"
        log.info(msg)
        print(msg)
