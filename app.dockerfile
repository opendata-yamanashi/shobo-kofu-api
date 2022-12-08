FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

RUN cp /start.sh /start.production.sh && \
    cp /start-reload.sh /start.development.sh

ENV PYTHON_ENV="production"

CMD "/start.${PYTHON_ENV}.sh"