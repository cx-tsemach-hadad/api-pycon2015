from urllib.parse import urlsplit
from flask import has_app_context, has_request_context
from flask.globals import app_ctx, request_ctx
from werkzeug.exceptions import NotFound


def match_url(url, method=None):
    if not has_app_context():
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if has_request_context():
        url_adapter = request_ctx.url_adapter
    else:
        url_adapter = app_ctx.url_adapter
        if url_adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed_url = urlsplit(url)
    if parsed_url.netloc != '' and \
                    parsed_url.netloc != url_adapter.server_name:
        raise NotFound()
    return url_adapter.match(parsed_url.path, method)


def args_from_url(url, endpoint):
    r = match_url(url, 'GET')
    if r[0] != endpoint:
        raise NotFound()
    return r[1]
