from __future__ import unicode_literals

import json
import logging
from concurrent.futures import Future
from pathlib import Path
from typing import Optional

from mopidy import backend
from pykka import ThreadingActor
from tidalapi import Config, Quality, Session
from tidalapi.session import LinkLogin

from mopidy_tidal import Extension, context, library, playback, playlists

logger = logging.getLogger(__name__)


def _connecting_log(msg: str, level="info"):
    getattr(logger, level)("Connecting to TIDAL... " + msg)


class TidalBackend(ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super().__init__()
        self._active_session: Optional[Session] = None
        self._logged_in = False
        self._config = config
        context.set_config(self._config)
        self.playback = playback.TidalPlaybackProvider(audio=audio, backend=self)
        self.library = library.TidalLibraryProvider(backend=self)
        self.playlists = playlists.TidalPlaylistsProvider(backend=self)
        self.uri_schemes = ["tidal"]
        self._login_future: Optional[Future] = None
        self._login_url: Optional[str] = None
        self.login_method = "BLOCK"
        self.data_dir = Path(Extension.get_data_dir(self._config))
        self.oauth_file = self.data_dir / "tidal-oauth.json"
        self.lazy_connect = False

    @property
    def session(self):
        if not self.logged_in:
            self._login()
        return self._active_session

    @property
    def logged_in(self):
        if not self._logged_in:
            self._load_oauth_session()
        return self._logged_in

    def _save_oauth_session(self):
        # create a new session
        if self._active_session.check_login():
            # store current OAuth session
            data = {}
            data["token_type"] = {"data": self._active_session.token_type}
            data["session_id"] = {"data": self._active_session.session_id}
            data["access_token"] = {"data": self._active_session.access_token}
            data["refresh_token"] = {"data": self._active_session.refresh_token}
            logger.debug("Saving OAuth session to %s" % self.oauth_file)
            with self.oauth_file.open("w") as outfile:
                json.dump(data, outfile)
            self._logged_in = True
            logger.info("TIDAL Login OK")

    def on_start(self):
        user_config = self._config["tidal"]
        quality = user_config["quality"]
        _connecting_log("Quality = %s" % quality)
        config = Config(quality=Quality(quality))
        client_id = user_config["client_id"]
        client_secret = user_config["client_secret"]
        self.login_method = user_config["login_method"]
        self.lazy_connect = user_config["lazy"]
        if self.login_method == "HACK" and not user_config["lazy"]:
            _connecting_log(
                "HACK login implies lazy connection, setting lazy=True.",
                level="warning",
            )
            self.lazy_connect = True
        _connecting_log(f"login method {self.login_method}.")
        if (client_id and not client_secret) or (client_secret and not client_id):
            _connecting_log(
                "always provide client_id and client_secret together", "warning"
            )
            _connecting_log("using default client id & client secret from python-tidal")

        if client_id and client_secret:
            _connecting_log("client id & client secret from config section are used")
            config.client_id = client_id
            config.api_token = client_id
            config.client_secret = client_secret

        if not client_id and not client_secret:
            _connecting_log("using default client id & client secret from python-tidal")

        self._active_session = Session(config)
        if not self.lazy_connect:
            self._login()

    def _login(self):
        self._load_oauth_session()
        if not self._active_session.check_login():
            logger.info("Creating new OAuth session...")
            self._active_session.login_oauth_simple(function=logger.info)
            self._save_oauth_session()

        if not self._active_session.check_login():
            logger.info("TIDAL Login KO")
            raise ConnectionError("Failed to log in.")

    @property
    def logging_in(self) -> bool:
        """Are we currently waiting for user confirmation to log in?"""
        return bool(self._login_future and self._login_future.running())

    @property
    def login_url(self) -> Optional[str]:
        if not self._logged_in and not self.logging_in:
            login_url, self._login_future = self._active_session.login_oauth()
            self._login_future.add_done_callback(lambda *_: self._save_oauth_session())
            # self._login_future.add_done_callback(lambda: self.logged_in=True)
            self._login_url = login_url.verification_uri_complete
        return f"https://{self._login_url}" if self._login_url else None

    def _load_oauth_session(self):
        try:
            oauth_file = self.oauth_file
            with open(oauth_file) as f:
                logger.info("Loading OAuth session from %s...", oauth_file)
                data = json.load(f)

            assert self._active_session, "No session loaded"
            args = {
                "token_type": data.get("token_type", {}).get("data"),
                "access_token": data.get("access_token", {}).get("data"),
                "refresh_token": data.get("refresh_token", {}).get("data"),
            }

            self._active_session.load_oauth_session(**args)
        except Exception as e:
            logger.info("Could not load OAuth session from %s: %s", oauth_file, e)

        if self._active_session.check_login():
            logger.info("TIDAL Login OK")
            self._logged_in = True
