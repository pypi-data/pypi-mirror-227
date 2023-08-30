"""Temporary!"""
import json
import os
from pathlib import Path
import random

from flask import request
from lexrpc.server import Server

from .mst import MST
from .repo import Repo
from .storage import MemoryStorage


# duplicates testutil
random.seed(1234567890)

# XRPC server
lexicons = []
for filename in (Path(__file__).parent / 'lexicons').glob('**/*.json'):
    with open(filename) as f:
        lexicons.append(json.load(f))

server = Server(lexicons, validate=False)

# these are initialized in app.py, testutil.XrpcTestCase.setUp
key = None
storage = None
repo = None


def auth():
    if request.headers.get('Authorization') != f'Bearer {os.environ["REPO_TOKEN"]}':
        raise ValueError('Invalid bearer token in Authorization header')
