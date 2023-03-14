from page_analyzer.app import app
from page_analyzer.db import DB

DB().connect()


__all__ = ('app', )
