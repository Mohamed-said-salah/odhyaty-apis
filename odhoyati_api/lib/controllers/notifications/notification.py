from fastapi.exceptions import HTTPException

import httpx 

import json

from google.oauth2 import service_account
from google.auth.transport.requests import Request


SERVICE_ACCOUNT_FILE = "../security/odhoyati-95978-a296af5963e4.json"

FCM_ENDPOINT = 'https://fcm.googleapis.com/v1/projects/odhoyati-95978/messages:send'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/firebase.messaging"]
)

async def get_access_token():
    request = Request()
    credentials.refresh(request)
    return credentials.token


async def send_fcm_notification(token: str, title: str, body: str):
    access_token = await get_access_token()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            FCM_ENDPOINT,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()