# -*- coding: utf-8 -*-

# __all__ = ['send']

import io
from typing import Any, Mapping

import requests
import torch


def push(host: str, name: str, model: Mapping[str, Any] = None, **kwargs):
    buffer = io.BytesIO()
    torch.save(model, buffer)
    url = f'{host}/public/ai'
    r = requests.post(url, data={'name': name, 'model': buffer.getvalue()},
                      **kwargs)
    if r.status_code != 200:
        return {'code': r.status_code, 'msg': r.text}

    return r.json()
