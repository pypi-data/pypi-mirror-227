import uuid
from mimetypes import guess_extension
from urllib.parse import urljoin

import requests
from flask import g
from qcos import Client


class COS(Client):
    def __init__(self, bucket=None, app=None):
        self.bucket = bucket
        if app:
            self.init_app(app)

    def init_app(self, app):
        secret_id = app.config["COS_SECRET_ID"]
        secret_key = app.config["COS_SECRET_KEY"]
        region = app.config["COS_REGION"]
        bucket = self.bucket or app.config["COS_BUCKET"]
        scheme = app.config.get("COS_SCHEME", "https")
        self.host = app.config.get("COS_HOST")

        super().__init__(secret_id, secret_key, region, bucket, scheme)
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        requests_session = g.pop("requests_session", None)
        if requests_session is not None:
            requests_session.close()

    @property
    def session(self):
        requests_session = g.get("requests_session")
        if requests_session is None:
            g.requests_session = requests.Session()
        return g.requests_session

    @session.setter
    def session(self, value):
        pass

    def get_url(self, key):
        if self.host:
            return urljoin(self.host, key)
        else:
            return super().get_object_url(key)


def gen_filename(mimetype=""):
    """使用uuid生成随机文件名
    :params mimetype: 用于生成文件扩展名
    """
    ext = guess_extension(mimetype)
    if ext == ".jpe":
        ext = ".jpg"
    elif ext is None:
        ext = ""

    return uuid.uuid4().hex + ext
