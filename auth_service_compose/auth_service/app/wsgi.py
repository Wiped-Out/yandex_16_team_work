from gevent import monkey

monkey.patch_all()

from app import app  # noqa: F401, E402
