import os


class Config(object):
    SECRET_KEY = os.environ.get('SECERT_KEY') or "secret_string"
