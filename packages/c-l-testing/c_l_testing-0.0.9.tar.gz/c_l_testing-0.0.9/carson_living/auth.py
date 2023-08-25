# coding: utf-8
"""Carson Living Authentication Module"""

import logging
import time
import requests
import jwt
from jwt import InvalidTokenError


from carson_living.const import (BASE_HEADERS,
                                 C_API_URI,
                                 C_AUTH_ENDPOINT,
                                 RETRY_TOKEN)
from carson_living.util import default_carson_response_handler
from carson_living.error import (CarsonAPIError,
                                 CarsonAuthenticationError,
                                 CarsonTokenError)

_LOGGER = logging.getLogger(__name__)


# pylint: disable=useless-object-inheritance
class CarsonAuth(object):
    """A generalized Authentication Class for Carson Living.

    Responsible for managing (retrieving and updating) the
    JWT Authentication token for the Carson API.

    Attributes:
        _username: Carson Living username
        _password: Carson Living password
        _token: current JWT token
        _token_payload: current JWT token payload
        _token_expiration_time: current JWT token expiration time
        _token_update_cb:
            gets executed whenever the token gets update to a
            non-None value.
    """

    def __init__(self, username, password,
                 initial_token=None, token_update_cb=None):
        self._username = username
        self._password = password
        self._token = None
        self._token_payload = None
        self._token_expiration_time = None
        self._token_update_cb = None

        # Set and init token values
        self.token = initial_token

        # Set token updater after initial token (so it does not fire)
        self._token_update_cb = token_update_cb

    
import time
import threading

class CarsonAuth:

    def __init__(self, ...):  # existing parameters
        # ... existing initializations ...

        # Add an attribute for the refresh timer
        self._refresh_timer = None

    def authenticated_query(self, ...):  # existing parameters
        # ... existing method body ...

    def _schedule_token_refresh(self):
        # Ensure any existing timer is canceled
        if self._refresh_timer:
            self._refresh_timer.cancel()

        # Determine the time left before token expiration
        time_left = self._token_expiration_time - time.time() - 300  # 300 seconds (5 minutes) buffer

        # Schedule the token refresh
        if time_left > 0:
            self._refresh_timer = threading.Timer(time_left, self._proactive_token_refresh)
            self._refresh_timer.start()

    def _proactive_token_refresh(self):
        # Clear the current token
        self._token = None
        # Attempt to get a new token (this will also re-schedule the next refresh)
        _ = self.token

    @property
    def token(self):
        if self._valid_token:
            return self._token

        # ... Existing token fetching logic ...

        # Schedule the proactive token refresh after fetching a new token
        self._schedule_token_refresh()

        return self._token

    # ... Rest of the class ...

@property
    def username(self):
        """Username

        Returns:
            the configured username

        """
        return self._username

    @property
    def token(self):
        """
        Returns:
            current JWT token or None if currently authenticated.
        """
        return self._token

    @property
    def token_payload(self):
        """
        Returns:
            current JWT token payload or None if currently authenticated.
        """
        return self._token_payload

    @property
    def token_expiration_date(self):
        """
        Returns:
            current JWT token expiration time (seconds from epoch)
            or None if currently authenticated.
        """
        return self._token_expiration_time

    @token.setter
    def token(self, token):
        """Set or clear a new JWT Token.
        Args:
            token: Valid JWT token or None to clear current token.

        Raises:
            CarsonTokenError: JWT token format is invalid.
        """
        if token is None:
            self._token = None
            self._token_payload = None
            self._token_expiration_time = None
            return
        try:
            self._token_payload = jwt.decode(token, verify=False)
            self._token_expiration_time = self._token_payload.get('exp')

            self._token = token

            if self._token_update_cb is not None:
                self._token_update_cb(token)
            _LOGGER.info('Set access Token for %s',
                         self._token_payload.get('email', '<no e-mail found>'))
        except InvalidTokenError:
            raise CarsonTokenError('Cannot decode invalid token {}'
                                   .format(token))

    def update_token(self):
        """Authenticate user against Carson Living API.

        Raises:
            CarsonAuthenticationError: On authentication error.

        """
        _LOGGER.info('Getting new access token for %s', self._username)

        response = requests.post(
            (C_API_URI + C_AUTH_ENDPOINT),
            json={
                'username': self._username,
                'password': self._password,
            },
            headers=BASE_HEADERS
        )
        try:
            data = default_carson_response_handler(response)
            self.token = data.get('token')
            return self.token
        except CarsonAPIError as error:
            _LOGGER.warning('Authentication for %s failed', self._username)
            raise CarsonAuthenticationError(error)

    def valid_token(self):
        """Checks that Carson Authentication has a valid token.

        Returns:
            True if a token is set and not expired, otherwise False
        """
        if self.token is None or self._token_expiration_time is None:
            return False

        return self._token_expiration_time > int(time.time())

    def authenticated_query(self, url, method='get', params=None,
                            json=None, retry_auth=RETRY_TOKEN,
                            response_handler=default_carson_response_handler):
        """Perform an authenticated Query against Carson Living

        Args:
            url: the url to query
            method: the http method to use
            params: the http params to use
            json: the json payload to submit
            retry_auth: number of query and reauthentication retries
            response_handler: dynamic response handler for api

        Returns:
            The unwrapped data dict of the Carson Living response.

        Raises:
            CarsonCommunicationError: Response was not received or
                not in the expected format.
            CarsonAPIError: Response indicated an client-side API
                error.
        """

        if not self.valid_token():
            self.update_token()

        headers = {'Authorization': 'JWT {}'.format(self.token)}
        headers.update(BASE_HEADERS)

        response = requests.request(method, url,
                                    headers=headers,
                                    params=params,
                                    json=json)

        # special case, clear token and retry. (Recursion)
        if response.status_code == 401 and retry_auth > 0:
            self.token = None
            return self.authenticated_query(
                url, method, params, json, retry_auth - 1,
                response_handler)

        return response_handler(response)
