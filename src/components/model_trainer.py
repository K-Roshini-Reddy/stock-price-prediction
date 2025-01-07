import os
import sys
from dataclasses import dataclass
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.linear_model import LinearRegression
from hmmlearn.hmm import GaussianHMM
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import numpy as np

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            best_rmse = float("inf")
            best_model = None

            param_grid = {
                "n_components": [2, 3, 4],
                "covariance_type": ['diag', 'full'],
                "n_iter": [500],
                "tol": [1e-3]
            }

            for n_components in param_grid["n_components"]:
                for covariance_type in param_grid["covariance_type"]:
                    try:
                        hmm_model = GaussianHMM(
                            n_components=n_components,
                            covariance_type=covariance_type,
                            n_iter=param_grid["n_iter"][0],
                            tol=param_grid["tol"][0],
                            random_state=42
                        )
                        hmm_model.fit(X_train)

                        hidden_states = hmm_model.predict(X_train)
                        X_train_with_states = np.column_stack([X_train, hidden_states])

                        reg_model = LinearRegression()
                        reg_model.fit(X_train_with_states, y_train)

                        X_test_with_states = np.column_stack([X_test, hmm_model.predict(X_test)])
                        predicted = reg_model.predict(X_test_with_states)

                        rmse = sqrt(mean_squared_error(y_test, predicted))

                        if rmse < best_rmse:
                            best_rmse = rmse
                            best_model = (hmm_model, reg_model)
                    except Exception as e:
                        logging.info(f"Error in model training: {e}")

            if best_model is None:
                raise CustomException("No suitable model found")

            save_object(self.model_trainer_config.trained_model_file_path, best_model)

            return best_rmse
        except Exception as e:
            raise CustomException(e, sys)
