from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import (
                                TrainingPipelineConfig,
                                DataTransformationConfig,
                                DataValidationConfig,
                                DataIngestionConfig
                                )
from src.components.data_transformation import DataTransformation
from src.exception.exception import CustomeException
import sys
if __name__ == "__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()

        #Data ingestion
        dataIngestionConfig = DataIngestionConfig()
        obj = DataIngestion(dataIngestionConfig)
        df = obj.initiate_data_ingestion()

        #Data validation
        dataValidationConfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        obj = DataValidation(data_validation_config=dataValidationConfig)
        data_validation_artifacts = obj.initiate_data_validation()

        #Data Transformation
        dataTransformationConfig = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        dataTransformationobj = DataTransformation(data_validation_artifacts,dataTransformationConfig)
        dataTransformationobj.initiate_data_transformation()
        
    except Exception as e:
        raise CustomeException(e,sys)