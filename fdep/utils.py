"""Misc. utilties. e.g. urlparse, etc."""

try:
    from urlparse import urlparse
except ImportError:  # pragma: no cover
    from urllib.parse import urlparse
