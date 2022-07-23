import os

import requests

BASE_URL = "https://api.doppler.com/v3/configs/config/secret"


def _get_secret(name: str):
    def _get() -> str:
        with requests.get(
            BASE_URL,
            params={
                "project": "eaglytics",
                "config": "prd",
                "name": name,
            },
            auth=(os.getenv("DOPPLER_TOKEN"), ""),
        ) as r:
            res = r.json()
        return res["value"]["raw"]

    return _get


get_access_token = _get_secret("FACEBOOK_ACCESS_TOKEN")
