FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY web_fetch/ web_fetch/

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r web_fetch/requirements.txt

# Make the Browserless URL configurable at runtime
ENV BROWSERLESS_API_URL=http://browserless:3000/content

EXPOSE 8000
CMD ["uvicorn", "web_fetch.app:app", "--host", "0.0.0.0", "--port", "8000"]