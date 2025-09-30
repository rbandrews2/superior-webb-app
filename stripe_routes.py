import json
import asyncio
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
import os


from report_pipeline import build_and_send_report


router = APIRouter()


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, background: BackgroundTasks):
# For production, verify signature using STRIPE_WEBHOOK_SECRET
payload = await request.body()
try:
event = json.loads(payload)
except Exception:
raise HTTPException(400, "Invalid payload")


etype = event.get("type")
data = event.get("data", {}).get("object", {})


if etype == "checkout.session.completed":
session = data
email = (session.get("customer_details") or {}).get("email")
metadata = session.get("metadata") or {}
address = metadata.get("address", "Unknown address")
report_id = metadata.get("report_id", session.get("id"))
if not email:
raise HTTPException(400, "Missing customer email in session")


# Kick off background task to generate & send report
background.add_task(lambda: asyncio.run(build_and_send_report(address, email, report_id)))


return {"received": True}