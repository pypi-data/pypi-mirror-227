import logging
from time import sleep

import requests

from tb_vendor.tb_utils import validate_login
from tb_vendor.rest.models import RestClient

logger = logging.getLogger(__name__)


def login_wait(
    rest_client: RestClient, username: str, password: str, retry_for_timeout: int
) -> None:
    """Try to authenticate in TB Server and wait until login.

    Args:
        rest_client: RestClient instance.
        username: username for login.
        password: password for login.
        retry_for_timeout: retry timeout if something go wrong.

    Returns:
        This function is expected to return None when login was successful
    """
    # cnt_exp, max_exp = 0, 100
    while True:
        # cnt_exp += 1
        logger.info("Try to login in TB Server")
        try:
            rest_client.login(username, password)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"ConnectionError for login: {e}")
            sleep(retry_for_timeout)
        except Exception:
            logger.exception("Error for login")
            sleep(retry_for_timeout)
        else:
            validate_login(rest_client)
            logger.info("Login successful")
            break
        # if cnt_exp > max_exp:
        #     raise Exception(f"Login failed after {max_exp} attempts")
