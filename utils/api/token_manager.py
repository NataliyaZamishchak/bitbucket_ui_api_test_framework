import json
import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

REFRESH_TOKEN_URL = "https://bitbucket.org/site/oauth2/access_token"
TOKEN_FILE = "token.json"
CLIENT_ID=os.getenv("BITBUCKET_CLIENT_ID")
CLIENT_SECRET=os.getenv("BITBUCKET_CLIENT_SECRET")


class TokenManager:
    def __init__(self, workspace: str = None, token_file=TOKEN_FILE):
        self.token_file = token_file
        self.api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
        self.token = None
        self.workspace = workspace

    def _load_token(self):
        """Load token from file."""
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                data = json.load(f)
                if "access_token" in data:
                    return data["access_token"]
        return None

    def _load_refresh_token(self):
        """Load refresh token from file."""
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                data = json.load(f)
                if "refresh_token" in data:
                    return data["refresh_token"]
        return None

    def _is_token_valid(self):
        """Check if the token is valid by making a simple API request."""
        if not self.token:
            return False
        headers = {"Authorization": f"Bearer {self.token}"}
        headers.update({"Accept": "application/json"})
        try:
            response = requests.get(self.api_url, headers=headers)
            if response.status_code == 200:
                print("Token is valid.")
                return True
            elif response.status_code == 401:
                print("Token expired or invalid.")
                return False
            else:
                print(f"Unexpected error: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error validating token: {str(e)}")
            return False

    def _save_token(self, token_data: dict):
        """Save full token data to a file."""
        with open(self.token_file, "w") as f:
            json.dump(token_data, f, indent=2)
        print("New token data saved.")

    def _refresh_token(self) -> dict:

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
            return response.json()
        else:
            raise Exception(f"Failed to refresh token: {response.status_code} {response.text}")

    def get_or_refresh_token(self):
        """Get the token, refresh it if expired or missing."""
        self.token = self._load_token()

        # If token is missing or expired, refresh it
        if self.token is None or not self._is_token_valid():
            print("Refreshing token...")
            new_data = self._refresh_token()
            self._save_token(new_data)
            print("Token refreshed...")
            self.token = self._load_token()

        return self.token
