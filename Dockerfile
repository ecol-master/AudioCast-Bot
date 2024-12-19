FROM python:3.10-slim-bullseye as compile-image

RUN python -m venv venv
ENV PATH="venv/bin:$PATH"
COPY requirements.txt . 

RUN pip install --no-cache-dir  --upgrade pip \
  && pip install --no-cache-dir  -r requirements.txt
FROM python:3.10-slim-bullseye

COPY --from=compile-image venv/ venv/
ENV PATH="/venv/bin:$PATH"
WORKDIR /app
COPY bot /app/bot
COPY locales /app/locales
CMD ["python", "-m", "bot"]
