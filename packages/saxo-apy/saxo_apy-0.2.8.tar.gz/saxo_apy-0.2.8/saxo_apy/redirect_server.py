"""Redirect server class used by SaxoOpenAPIClient."""

import logging
import threading
from typing import Optional
from urllib.parse import parse_qs

from flask import Flask, request
from loguru import logger
from pydantic import AnyHttpUrl, parse_obj_as
from werkzeug.serving import make_server

response_html = """
<head>
<title>
SAXO-APY Client
</title>
<style>
body {background-color: black;}
h2 {color: white;}
</style>
</head>
<body>
<center><h2 style='font-family: sans-serif;'>
{display_text}
</h2></center>
</body>
"""


class RedirectServer(threading.Thread):
    """Simple redirect server to catch callback from Saxo SSO."""

    def __init__(
        self,
        redirect_url: AnyHttpUrl,
        state: str,
        port: Optional[int] = None,
    ):
        """Create new redirect server."""
        app = Flask(__name__)
        self.auth_code = None

        @app.route(str(redirect_url.path))
        def handle_redirect() -> str:
            logger.debug(f"redirect server received callback: {request.url}")

            redirect_location = parse_obj_as(AnyHttpUrl, request.url)
            parsed_qs = parse_qs(redirect_location.query)

            if (
                not parsed_qs.get("state") or parsed_qs.get("state")[0] != state  # type:ignore[index]
            ):
                logger.warning(f"received request state: {parsed_qs.get('state')} but expected {state}")
                display_text = "↪️ This is a redirect server for <code>saxo-apy</code>."
            elif "code" in parsed_qs:
                logger.success("redirect URL auth code found")
                self.auth_code = parsed_qs["code"][0]
                display_text = "✅ Login succeeded! Please return to the application."
            else:
                logger.error(f"no auth code found in redirect - authentication error occurred {request.url=}")
                display_text = f"🚫 It looks like an error occurred - {request.url=}"
            return response_html.replace("{display_text}", display_text)

        threading.Thread.__init__(self, daemon=True)
        host = "0.0.0.0"
        _port = port or redirect_url.port

        logger.debug(f"initializing redirect server: {host}:{_port}{redirect_url.path}")

        assert _port
        self.server = make_server(host, int(_port), app)
        self.ctx = app.app_context()
        self.ctx.push()
        logging.getLogger("werkzeug").disabled = True  # disable default logging

    def run(self) -> None:
        """Start server."""
        logger.debug("starting redirect server")
        self.server.serve_forever()

    def shutdown(self) -> None:
        """Stop server."""
        logger.debug("terminating redirect server")
        self.server.shutdown()
