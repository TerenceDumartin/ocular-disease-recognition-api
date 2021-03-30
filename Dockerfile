FROM python:3.8-slim-buster

COPY lwg-ocular-disease-recognition-18a8987ca398.json /credentials.json
COPY model0_classif_eye.h5 /model0_classif_eye.h5
COPY model1_models_model_inception2_v0_N_70.h5 /model1_models_model_inception2_v0_N_70.h5
COPY model2_models_model_vlundi_v1_GCAHMO_58.h5 /model2_models_model_vlundi_v1_GCAHMO_58.h5
COPY api /api
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port 8000
