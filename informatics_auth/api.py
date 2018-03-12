import requests
import json

LOGIN_URL = "https://rmatics.info/api_v2/auth/login"


class InformaticsApiException(Exception):
    pass


class InformaticsApiInvalidPassword(InformaticsApiException):
    pass


def login(username, password):
    try:
        ret = requests.post(
            LOGIN_URL,
            data=json.dumps({
                'username': username,
                'password': password,
            }
        )).json()
    except requests.RequestException as e:
        raise InformaticsApiException from e
    if "code" in ret:
        if ret["code"] == 403:
            raise InformaticsApiInvalidPassword(ret["message"])
        else:
            raise InformaticsApiException(ret.get("message", "No message"))
    return ret