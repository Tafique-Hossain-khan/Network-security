from src.logging.logger import logging
from src.exception.exception import CustomeException
from src.utils.main_utlis import utils
from dataclasses import dataclass
from scipy.stats import ks_2samp # used to compare the distribution of two sampel
import os,sys
import pandas as pd


@dataclass
class DataValidationConfig: 

    drift_report_file_path = os.path.join("Data_validation/Drift_report","report.yaml")


class DataValidation:

    def __init__(self):
        self.data_validataion_config_obj = DataValidationConfig()
    
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame,yaml_file_path:str):
        """
        This fucntion aims to validate the number of columns in the dataset

        Parameters:
        dataframe: The original dataset
        yaml_file_path: File path for the schema of the dataset

        Return: 
        Boolean value 'True' if the columns are same else 'False'
        """
        try:
            schema = utils.read_yaml(yaml_file_path)
            schema = schema["columns"]
            number_of_columns=len(schema)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise CustomeException(e,sys)
        
    def validate_number_of_numerical_columsn(self,dataframe:pd.DataFrame,yaml_file_path):
        """
        This fucntion aims to validate the number of numerical columns in the dataset

        Parameters:
        dataframe: The original dataset
        yaml_file_path: File path for the schema of the dataset

        Return: 
        Boolean value 'True' if the columns are same else 'False'
        """
        pass

    

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        """
        This fucntion aims check the drift in the upcomming dataset

        Parameters:
        base_df (pd.DataFrame): Original Dataset that is being used to train the model
        current_df (pd.DataFrame): new Dtatset 

        Return: 
        Boolean value 'True' if the columns are same else 'False'
        """
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue: #if the p_value is greater than the thresold then there is no drift
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
                
                os.makedirs(os.path.dirname(self.data_validataion_config_obj.drift_report_file_path),exist_ok=True)
                utils.write_yaml_file(file_path=self.data_validataion_config_obj.drift_report_file_path,content=report)

        except Exception as e:
            raise CustomeException(e,sys)
        
    def initiate_data_validation(self):
        try:
            df = pd.read_csv("Data\phisingData.csv")
            train_dataframe = pd.read_csv("Data\ingested_data\\train_data.csv")
            test_dataframe = pd.read_csv("Data\ingested_data\\test_data.csv")
            yaml_file_path = 'Data_schema\schema.yaml'
            status=self.validate_number_of_columns(dataframe=train_dataframe,yaml_file_path=yaml_file_path)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe,yaml_file_path=yaml_file_path)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"   
            ## lets check datadrift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            #Based on the status we can save the incomming data
            
        except Exception as e:
            raise CustomeException(e,sys)


if __name__ == "__main__":
    obj = DataValidation()
    obj.initiate_data_validation()