FROM arm64v8/python:3.13.7-slim

COPY Pipfile Pipfile.lock ./

RUN pip install hidapi pipenv && \
    apt-get update && \
    apt-get install --yes --no-install-recommends gcc python3-dev libssl-dev libusb-1.0-0-dev libudev-dev && \
    pipenv install --deploy --system && \
    apt-get remove --yes gcc python3-dev libssl-dev && \
    apt-get autoremove --yes && \
    pip uninstall pipenv --yes

COPY main.py ./

EXPOSE 9800

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "9800", "main:app"]
