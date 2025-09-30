# Uses Chromium + fonts + Playwright preinstalled
FROM mcr.microsoft.com/playwright/python:v1.47.2-jammy


WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN docker build --no-cache -t superior-report-api 

COPY . .


# Expose app port
ENV PORT=10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
