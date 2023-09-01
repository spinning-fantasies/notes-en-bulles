import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Replace these with your actual values
instance_url = os.getenv("MASTODON_INSTANCE_URL")
access_token = os.getenv("MASTODON_ACCESS_TOKEN")
account_id = os.getenv("AUTHENTICATED_USER_ID")

# Set up headers
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Write you code below
