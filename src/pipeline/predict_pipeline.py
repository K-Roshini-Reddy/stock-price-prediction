import os
import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
from src.logger import logging
import numpy as np

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            logging.info("Starting prediction pipeline")

            model_path = os.path.join('artifacts', 'model.pkl')
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')

            model = load_object(model_path)
            preprocessor = load_object(preprocessor_path)

            logging.info(f"Model and Preprocessor loaded from {model_path} and {preprocessor_path}")

            features_scaled = preprocessor.transform(features)
            hmm_model, reg_model = model

            hidden_states = hmm_model.predict(features_scaled)
            features_with_states = np.column_stack([features_scaled, hidden_states])

            predictions = reg_model.predict(features_with_states)

            logging.info("Predictions made successfully")
            return predictions
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            raise CustomException(e, sys)
