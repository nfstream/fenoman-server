import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle

data_set = "./X_scaled.csv"

def split_dataset():
    df = pd.read_csv(data_set)
    df.sample(frac=1).reset_index(drop=True)

    df = shuffle(df)

    label_encoder = LabelEncoder()
    list_of_names = df['application_name'].unique().tolist()
    list_of_labels = label_encoder.fit_transform(df['application_name'].unique()).tolist()
    name_and_id = []
    for i in range(len(list_of_names)):
        temp_tuple = (list_of_names[i], list_of_labels[i])
        name_and_id.append(temp_tuple)

    df['application_name'] = label_encoder.fit_transform(df['application_name'])  # LabelEncode text data

    """Set to a lower number, since X_scaled has less rows"""
    number_of_rows = 6505
    number_of_rows = 11709
    sub_dfs = [df[i:i + number_of_rows] for i in range(0, df.shape[0], number_of_rows)]

    for idx, sub_dfs in enumerate(sub_dfs):
        sub_dfs.to_csv(f'{data_set}-part-{idx}.csv', index=False)

    print(df['application_name'].max())


def join_dataset():
    # TODO: ez azért kellett mert béna voltam meg kell csinálni, hogy mentse ki a teljes data setet a application category labellel
    df_names = []
    for i in range(1, 16, 1):
        df_names.append(f'{data_set}-part-{i}.csv')
    df = pd.read_csv(df_names[0])
    for i in range(1, 15, 1):
        df2 = pd.read_csv(df_names[i])
        df = df.append(df2)
    df.to_csv(f'{data_set.replace(".csv", "")}-labeled.csv')


if __name__ == '__main__':
    #split_dataset()
    join_dataset()
