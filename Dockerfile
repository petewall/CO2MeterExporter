FROM arm64v8/python:3.12.2-slim

COPY Pipfile Pipfile.lock ./

RUN pip install co2meter hidapi pipenv && \
    apt-get update && \
    apt-get install --yes --no-install-recommends gcc python3-dev libssl-dev libusb-1.0-0-dev libudev-dev && \
    pipenv install --deploy --system && \
    apt-get remove --yes gcc python3-dev libssl-dev && \
    apt-get autoremove --yes && \
    pip uninstall pipenv --yes

COPY main.py ./

EXPOSE 9800

CMD ["uvicorn", "--port", "9800", "main:app"]
