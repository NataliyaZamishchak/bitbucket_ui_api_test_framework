import json
import os
import requests
from dotenv import load_dotenv

from utils.auth.token_retriver import TokenRetriever

load_dotenv()

BITBUCKET_API_URL = f"https://api.bitbucket.org/2.0/repositories/{os.getenv("BITBUCKET_ORGANIZATION_NAME")}"
TOKEN_FILE = "token.json"


class TokenManager:
    def __init__(self, token_file=TOKEN_FILE, api_url=BITBUCKET_API_URL):
        self.token_file = token_file
        self.api_url = api_url
        self.token = None

    def _load_token(self):
        """Load token from file if it exists and is not expired."""
        if os.path.exists(self.token_file):
            with open(self.token_file) as f:
                data = json.load(f)
                if "access_token" in data:
                    return data["access_token"]
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

    def _save_token(self):
        """Save new token to a file."""
        with open(self.token_file, "w") as f:
            json.dump({"access_token": self.token}, f, indent=2)
        print("New token saved.")

    def _retrieve_token(self):
        """Retrieve new token."""
        print("Retrieving new token...")
        self.token = self._get_bearer_token()
        print("Saving new token...")
        self._save_token()

    def _get_bearer_token(self):
        """Get token from token retriever."""
        retriever = TokenRetriever()
        token = retriever.get_bearer_token()
        print("Bearer token:", token[:15] + "...")
        return token

    def get_or_refresh_token(self):
        """Get the token, refresh it if expired or missing."""
        self.token = self._load_token()

        # If token is missing or expired, refresh it
        if self.token is None or not self._is_token_valid():
            print("Refreshing token...")
            self._retrieve_token()

        return self.token


# # Example usage
# token_manager = TokenManager()
# token = token_manager.get_or_refresh_token()
# print("Bearer token:", token[:15] + "...")
