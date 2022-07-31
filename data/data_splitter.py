import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle


def split_dataset():
    df = pd.read_csv('./comnet14-flows.csv')
    df.sample(frac=1).reset_index(drop=True)

    df = shuffle(df)

    label_encoder = LabelEncoder()
    df['application_name'] = label_encoder.fit_transform(df['application_name'])  # LabelEncode text data

    number_of_rows = 151145
    sub_dfs = [df[i:i + number_of_rows] for i in range(0, df.shape[0], number_of_rows)]

    for idx, sub_dfs in enumerate(sub_dfs):
        sub_dfs.to_csv(f'./comnet14-flows-part-{idx}.csv', index=False)

    print(df['application_name'].max())


def join_dataset():
    # TODO: ez azért kellett mert béna voltam meg kell csinálni, hogy mentse ki a teljes data setet a application category labellel
    df_names = []
    for i in range(1, 6, 1):
        df_names.append(f'comnet14-flows-part-{i}.csv')
    df = pd.read_csv(df_names[0])
    for i in range(1, 5, 1):
        df2 = pd.read_csv(df_names[i])
        df = df.append(df2)
    df.to_csv('./comnet14-flows-labeled.csv')


if __name__ == '__main__':
    join_dataset()
    #split_dataset()
