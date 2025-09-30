import os
import base64
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.async_api import async_playwright
from supabase import create_client
import httpx


RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "Customer Support <customerservice@superiorllc.org>")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET = os.getenv("REPORTS_BUCKET", "reports")
RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")


# -----------------
# Jinja environment + helpful filters
# -----------------
env = Environment(
loader=FileSystemLoader("templates"),
autoescape=select_autoescape(["html", "xml"])
)


def usd(value):
try:
if value is None: return "-"
return f"${float(value):,.0f}"
except Exception:
return "-"


def shortdate(value):
if not value:
return "-"
# Expecting ISO like '2023-08-12T...' or '2023-08-12'
return str(value)[:10]


def yesno(value, yes="Yes", no="No", null="-"):
if value is True: return yes
if value is False: return no
return null


env.filters["usd"] = usd
env.filters["shortdate"] = shortdate
env.filters["yesno"] = yesno


# -----------------
# PDF rendering
# -----------------
async def html_to_pdf(html: str) -> bytes:
async with async_playwright() as p:
browser = await p.chromium.launch()
page = await browser.new_page()
await page.set_content(html, wait_until="networkidle")
pdf = await page.pdf(
format="Letter",
print_background=True,
margin={"top":"0.5in","bottom":"0.5in","left":"0.5in","right":"0.5in"}
)
await browser.close()
return pdf


# -----------------
# Data gathering (REAL RentCast call)
# -----------------
async def fetch_data(address: str, report_id: str) -> dict:
headers = {"X-Api-Key": RENTCAST_API_KEY} if RENTCAST_API_KEY else {}
out = {"address": address}


prop = {}
async with httpx.AsyncClient(timeout=60) as client:
try:
r = await client.get(
"https://api.rentcast.io/v1/properties",
params={"address": address},
send_email(email, "Your Property Report is Ready", body, "report.pdf", pdf_bytes)
