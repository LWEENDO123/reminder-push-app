# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pywebpush import webpush, WebPushException
import json

app = FastAPI()
subscriptions = []

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/save-subscription")
async def save_subscription(request: Request):
    sub = await request.json()
    subscriptions.append(sub)
    return {"message": "Subscription saved"}

@app.post("/send-reminder")
async def send_reminder():
    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps({
                    "title": "Class Reminder",
                    "body": "Your class at UNZA starts now!"
                }),
                vapid_private_key="YOUR_PRIVATE_KEY",
                vapid_claims={"sub": "mailto:you@example.com"}
            )
        except WebPushException as e:
            print("Push failed:", e)
    return {"message": "Notifications sent"}
