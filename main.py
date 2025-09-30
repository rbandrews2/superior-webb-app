import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()


CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]


app = FastAPI(title="superior-report-api")


app.add_middleware(
CORSMiddleware,
allow_origins=CORS_ORIGINS,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.get("/")
def root():
return {"message": "Report API is running"}


# Mount Stripe webhook routes
from stripe_routes import router as stripe_router
app.include_router(stripe_router)