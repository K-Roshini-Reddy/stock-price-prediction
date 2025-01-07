import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion process")
        try:
            df = pd.read_csv('Z:\\Data Science\\stock price prediction\\notebook\\data\\nifty 50.csv')
            logging.info('Dataset loaded into a DataFrame')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            train_set, test_set = train_test_split(df, test_size=0.2, shuffle=False)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed")
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_array, test_array, preprocessor_path = data_transformation.initiate_data_transformation(
        'Z:\\Data Science\\stock price prediction\\artifacts\\train.csv', 
        'Z:\\Data Science\\stock price prediction\\artifacts\\test.csv'
    )

    try:
        # Initialize the ModelTrainer
        model_trainer = ModelTrainer()

        # Pass the train_array and test_array to the model trainer
        best_rmse = model_trainer.initiate_model_trainer(train_array, test_array)

        # Log the best RMSE achieved
        logging.info(f"Best RMSE achieved: {best_rmse}")

    except Exception as e:
        # Log any exceptions that occur during execution
        logging.error(f"Error occurred in the model training process: {str(e)}")
