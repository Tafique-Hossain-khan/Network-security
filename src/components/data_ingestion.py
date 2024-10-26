from src.exception.exception import CustomeException
from src.logging.logger import logging
from dataclasses import dataclass
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
@dataclass
class DataIngestionConfig:
    
    raw_data_path:str = os.path.join("Data/ingested_data","raw_data.csv")
    train_data_path:str = os.path.join("Data/ingested_data","train_data.csv")
    test_data_path:str = os.path.join("Data/ingested_data","test_data.csv")

    
class DataIngestion:
    def __init__(self):
        pass

    def get_data_from_db(self,db_name,collection_name):
        try:
            MONGO_DB_URL = os.getenv("MONGO_DB_URL")
            client = pymongo.MongoClient(MONGO_DB_URL)
            data = client[db_name][collection_name]

            df=pd.DataFrame(list(data.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            os.makedirs(os.path.dirname(DataIngestionConfig.raw_data_path),exist_ok=True)
            df.to_csv(DataIngestionConfig.raw_data_path)
            return df
        except Exception as e:
            raise CustomeException(e,sys)
        
    def split_data_into_train_test(self,raw_data,test_size):
        try:
            logging.info("spliting the data into train and test")
            X = raw_data.drop(columns=['Result'])
            y = raw_data['Result']
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=test_size,random_state=42)
            logging.info(X_train.shape)
            logging.info(X_test.shape)

            os.makedirs(os.path.dirname(DataIngestionConfig.train_data_path),exist_ok=True)
            X_train.to_csv(DataIngestionConfig.train_data_path)

            os.makedirs(os.path.dirname(DataIngestionConfig.test_data_path),exist_ok=True)
            X_test.to_csv(DataIngestionConfig.test_data_path)

            logging.info("Data spliting complited and saved to the respective location")

            return X_train,X_test,y_train,y_test
        except Exception as e:
            raise CustomeException(e,sys)


    