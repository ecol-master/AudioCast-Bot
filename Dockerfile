FROM python:3.10-slim-bullseye

ENV PATH="venv/bin:$PATH"
COPY requirements.txt . 
RUN pip install --no-cache-dir  --upgrade pip \
  && pip install --no-cache-dir  -r requirements.txt

WORKDIR /app
COPY bot /app/bot
RUN mkdir -p app/data
RUN mkdir -p app/db
CMD ["python", "-m", "bot"]
