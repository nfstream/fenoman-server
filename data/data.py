from patterns.singleton import singleton
import pandas as pd
from sklearn.model_selection import train_test_split
from configuration.data_configuration import *
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


@singleton
class Data:
    def __init__(self, df: str = TEST_DATAFRAME) -> None:
        self.__data = pd.read_csv(df)



    def load_data(self, target_field: str = TARGET_VARIABLE):
        train, validation = train_test_split(self.__data, test_size=TRAIN_VALIDATION_SPLIT)

        def __separate_target(df):
            return df.loc[:, ~train.columns.isin([target_field])], train[target_field]

        x_train, y_train = __separate_target(train)
        x_val, y_val = __separate_target(validation)

        return x_train, y_train, x_val, y_val


data = Data()
