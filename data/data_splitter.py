import pandas as pd
from sklearn.preprocessing import LabelEncoder


def split_dataset():
    df = pd.read_csv('./comnet14-flows.csv')
    df.sample(frac=1).reset_index(drop=True)

    label_encoder = LabelEncoder()
    df['application_name'] = label_encoder.fit_transform(df['application_name'])  # LabelEncode text data

    number_of_rows = 151145
    sub_dfs = [df[i:i + number_of_rows] for i in range(0, df.shape[0], number_of_rows)]

    for idx, sub_dfs in enumerate(sub_dfs):
        sub_dfs.to_csv(f'./comnet14-flows-part-{idx}.csv', index=False)

    print(df['application_name'].max())


if __name__ == '__main__':
    split_dataset()
