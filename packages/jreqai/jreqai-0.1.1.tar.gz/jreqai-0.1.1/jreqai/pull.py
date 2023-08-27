# -*- coding: utf-8 -*-

import io

import requests
import torch


def pull(host: str, name: str, version: str = "latest", **kwargs):
    url = f'{host}/public/ai'
    r = requests.get(url, params={'name': name, 'version': version}, **kwargs)
    if r.status_code != 200:
        return None
    buffer = io.BytesIO(r.content)

    return torch.load(buffer, map_location=torch.device('mps'))
