import json
import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

REFRESH_TOKEN_URL = "https://bitbucket.org/site/oauth2/access_token"
TOKEN_FILE = "token.json"
CLIENT_ID = os.getenv("BITBUCKET_CLIENT_ID")
CLIENT_SECRET = os.getenv("BITBUCKET_CLIENT_SECRET")


class TokenManager:
    """Manage Bitbucket OAuth2 access tokens: load, validate, refresh, and persist."""

    def __init__(self, workspace: str = None, token_file=TOKEN_FILE):
        """Initialize with workspace and token file."""
        self.token_file = token_file
        self.api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
        self.token = None
        self.workspace = workspace

    def _load_token(self):
        """Load access token from file."""
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                data = json.load(f)
                return data.get("access_token")
        return None

    def _load_refresh_token(self):
        """Load refresh token from file."""
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                data = json.load(f)
                return data.get("refresh_token")
        return None

    def _is_token_valid(self):
        """Check if the token is still valid."""
        if not self.token:
            return False
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        try:
            response = requests.get(self.api_url, headers=headers)
            if response.status_code == 200:
                logger.info("Token is valid.")
                return True
            elif response.status_code == 401:
                logger.info("Token expired or invalid.")
                return False
            else:
                logger.error(f"Unexpected error validating token: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Exception during token validation: {str(e)}")
            return False

    def _save_token(self, token_data: dict):
        """Save the full token data to file."""
        with open(self.token_file, "w") as f:
            json.dump(token_data, f, indent=2)
        logger.info("New token data saved.")

    def _refresh_token(self) -> dict:
        """Send request to refresh the token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._load_refresh_token()
        }
        response = requests.post(
            REFRESH_TOKEN_URL,
            data=data,
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        )
        if response.status_code == 200:
            logger.info("Token refreshed successfully.")
            return response.json()
        else:
            logger.error(f"Failed to refresh token: {response.status_code} {response.text}")
            raise Exception(f"Failed to refresh token: {response.status_code} {response.text}")

    def get_or_refresh_token(self):
        """Load existing token or refresh it if expired/missing."""
        self.token = self._load_token()
        if self.token is None or not self._is_token_valid():
            logger.info("Refreshing token...")
            new_data = self._refresh_token()
            self._save_token(new_data)
            self.token = self._load_token()
        return self.token
