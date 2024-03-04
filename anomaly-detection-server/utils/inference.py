#!/usr/bin/env python3

"""
This is a module that publishes messages to the broker.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2024, NT Team"

import os
import json
import warnings
from joblib import load
import pandas as pd

from utils.mqtt_publish import public_message
import config


warnings.filterwarnings("ignore")
SAVE_DIR = os.getenv('RESOURCE_PATH')


def detect_anomaly_data(df, dt):
    "inference anomaly data"
    try:
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
        df = scaler.transform(df)
        df = dim_reduction.transform(df)
        predicted_label = model.predict(df).tolist()
        # TODO : Fix
        topic = f'{config.BASE_TOPIC}/Abnormal'
        result = {
                "ALARM_TYPE": "ALARM",
                "DEVICE_ID": "DEV01",
                "VALUE": 0,
                "DATE_TIME": dt
            }
        if -1 in predicted_label:
            public_message(topic, json.dumps(result))
        return None

    except Exception:  # pylint: disable=broad-except
        return None
