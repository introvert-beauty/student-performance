import sys
import os
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
import pandas as pd
from dataclasses import dataclass

# write a @dataclass without use the init for creating class variables
@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join("artifacts/train.csv")
    test_data_path:str=os.path.join("artifacts/test.csv")
    raw_dat_path:str=os.path.join("artifacts/raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    
    def intiate_data_ingestion(self):
        try:
            logging.info("read the datset")
            df=pd.read_csv(r"D:\RESUME ML PROJECTS\student_performance\notebooks\Student_performance_data _.csv")

            logging.info("create a directory")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_dat_path,index=False,header=True)

            logging.info("train and test data split is intiated")
            train_set,test_set=train_test_split(df,test_size=0.2)

            logging.info("passed the train and test data to the path")
            train_set.to_csv(self.ingestion_config.train_data_path)
            test_set.to_csv(self.ingestion_config.test_data_path)
            
            logging.info("return the train and test data for data transformation process")
            return(
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path
        )
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj=DataIngestion()
    obj.intiate_data_ingestion()

        
    