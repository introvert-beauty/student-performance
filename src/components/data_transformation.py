import sys
import os
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str=os.path.join("artifacts/preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.transformation_config=DataTransformationConfig()

    def get_data_transformation(self):
        numerical_cols=["Age",	"Gender",	"Ethnicity",	"ParentalEducation",	"StudyTimeWeekly",	"Absences",	"Tutoring",	"ParentalSupport"	,"Extracurricular",	"Sports",	"Music",	"Volunteering","GradeClass"]
        categorical_cols=[]


        num_pipeline=Pipeline(
            steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ]
        )

        cat_pipeline=Pipeline(
            steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("onehotencoder",OneHotEncoder()),
                ("scaler",StandardScaler())
            ]
        )

        preprocessor=ColumnTransformer(
            [
                ("num_pipeline",num_pipeline,numerical_cols),
                ("cat_pipeline",cat_pipeline,categorical_cols)
            ]
        )


        return preprocessor
    
    def intiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            target_column_name="GPA"

            preprocessor_obj=self.get_data_transformation()

            input_train_data_path=train_df.drop(columns=[target_column_name],axis=1)
            input_test_data_path=test_df.drop(columns=[target_column_name],axis=1)

            preprocessor_obj_train_path=preprocessor_obj.fit_transform(input_train_data_path)
            preprocessor_obj_test_path=preprocessor_obj.transform(input_test_data_path)

            train_array=np.c_[
                preprocessor_obj_train_path,np.array(input_train_data_path),
                
            ]
            test_array=[
                preprocessor_obj_test_path,np.array(input_test_data_path)
            ]

            save_object(
                file_path=self.transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return(
                train_array,
                test_array,
                self.transformation_config.preprocessor_obj_file_path,
                
            )
        except Exception as e:
            raise CustomException(e,sys)
