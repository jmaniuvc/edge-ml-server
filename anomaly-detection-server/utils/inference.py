import os
import json
from joblib import load
import pandas as pd

from utils.mqtt_publish import public_message


SAVE_DIR = os.getenv('RESOURCE_PATH')


def detect_anomaly_data(df):
    "inference anomaly data"
    model = load(f'{SAVE_DIR}/dbscan.pkl')
    scaler = load(f'{SAVE_DIR}/scaler.joblib')
    onehot = load(f'{SAVE_DIR}/onehot_encoder.joblib')
    dim_reduction = load(f'{SAVE_DIR}/dime_reduction.joblib')
    with open(f'{SAVE_DIR}/meta_info.json', 'r', encoding='UTF-8') as f:
        meta = json.load(f)
    ###
    category_data_encoded = onehot.fit_transform(df[meta['categorical']])
    category_df = pd.DataFrame(
        category_data_encoded,
        columns=onehot.get_feature_names_out(meta['categorical']))
    df = pd.concat([df[meta['numeric']], category_df], axis=1)
    print(df)
    df = scaler.transform(df)
    df = dim_reduction.transform(df)

    predicted_label = model.predict(df).tolist()
    print(predicted_label)
    print("predicted_label")
    # result = {i+1: value for i, value in enumerate(predicted_label)}
    if -1 in predicted_label:
        public_message('anomaly')
