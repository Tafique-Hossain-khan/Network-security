import os
import sys
from dotenv import load_dotenv
import certifi # use to make secure http connection
import json
import pymongo
import pandas as pd
import pymongo.mongo_client
from src.exception.exception import CustomeException
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataExtraction:

    def __init__(self):
        pass

    def csv_to_json(self,df):
        try:
            json_str = df.to_json(orient='records')
            json_obj = json.loads(json_str)

            return json_obj
        
        except Exception as e:
            raise CustomeException(e,sys)
        
    def insert_data_mangodb(self,records,database,collection):

        try:

            mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            db = mongo_client[database]
            Collection = db[collection]
            if isinstance(records, list):
                Collection.insert_many(records)  
            else:
                Collection.insert_one(records)
            return len(records)
        except Exception as e:
            raise CustomeException(e,sys)
    


if __name__ == "__main__":
    obj = DataExtraction()
    df = pd.read_csv("Data\phisingData.csv")
    df.reset_index(drop=True,inplace=True)
    json_obj = obj.csv_to_json(df)

    database = "TAFIQUE"
    Collection = "NetworkData"
    no_of_records = obj.insert_data_mangodb(records=json_obj,database=database,collection=Collection)
    print(no_of_records)