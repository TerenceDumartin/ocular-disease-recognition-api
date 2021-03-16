FROM python:3.8-slim-buster

COPY lwg-ocular-disease-recognition-18a8987ca398.json /credentials.json
COPY baseline_model_N_C_downsample.h5 /baseline_model_N_C_downsample.h5
COPY api /api
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port 8000
