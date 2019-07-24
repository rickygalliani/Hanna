from flask import Flask

app = Flask(__name__)

from server.app import routes  # noqa: E731

routes.index()
