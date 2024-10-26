from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import (
                                TrainingPipelineConfig,
                                DataTransformationConfig,
                                DataValidationConfig,
                                DataIngestionConfig,
                                ModelTrainerConfig
                                )
from src.components.data_transformation import DataTransformation
from src.exception.exception import CustomeException
from src.components.model_trainer import ModelTrainer
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
        data_transformaiton_artifacts = dataTransformationobj.initiate_data_transformation()

        #model Training
        modelTrainerConfig = ModelTrainerConfig(trainingpipelineconfig)
        modelTrainerobj = ModelTrainer(model_trainer_config=modelTrainerConfig,data_transformation_artifact=data_transformaiton_artifacts)
        modelTrainerobj.initiate_model_trainer()
    
    
    except Exception as e:
        raise CustomeException(e,sys)