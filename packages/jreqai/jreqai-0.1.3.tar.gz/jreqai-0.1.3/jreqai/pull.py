# -*- coding: utf-8 -*-

import io

import requests
from .utils import device


def pull(host: str, name: str, version: str = "latest", **kwargs):
    import torch
    url = f'{host}/public/ai/' + name + ".pth"
    r = requests.get(url, params={'version': version}, **kwargs)
    if r.status_code != 200:
        return None

    buffer = io.BytesIO(r.content)

    return torch.load(buffer, map_location=device())


def versions(host: str, name: str, **kwargs):
    url = f'{host}/public/ai/' + name
    r = requests.get(url, None, **kwargs)

    if r.status_code != 200:
        return {'code': r.status_code, 'msg': r.text}

    return r.json()["data"]
