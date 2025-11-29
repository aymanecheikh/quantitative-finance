from kfp.v2.dsl import component, Output, Dataset
from ....constants import KubeFlowConstants as kfc


@component(base_image=kfc.BASE_IMAGE)
def preprocess_data(
    data_bucket: str,
    data_folder: str,
    train_file: str,
    test_file: str,
    processed_train_data: Output[Dataset],
    processed_test_data: Output[Dataset],
    test_labels_data: Output[Dataset]
):
    from google.cloud import storage
    from pandas import DataFrame, Series
    import pandas as pd
    from sklearn.model_selection import train_test_split
    import joblib
    import io


    client = storage.Client()
    bucket = client.bucket(data_bucket)


    def read_data(bucket, data_folder, data_file) -> DataFrame:
        blob_path = f"{data_folder}/{data_file}"
        blob = bucket.blob(blob_path)
        csv_content = blob.download_as_text()
        _df = pd.read_csv(io.StringIO(csv_content))
        return _df
    
    def data_preprocessing(raw: DataFrame) -> tuple[DataFrame, Series]:
        raw.dropna(inplace=True)
        raw['SMA_20'] = raw.close.rolling(window=20).mean()
        raw['SMA_50'] = raw.close.rolling(window=20).mean()
        raw.dropna(inplace=True)
        X = raw[['open', 'high', 'low', 'volume', 'SMA_20', 'SMA_50']]
        y = raw.close
        return X, y
    
 
    data_df = read_data(bucket, data_folder, train_file)
    X, y = data_preprocessing(data_df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )


    joblib.dump(X_train, processed_train_data.path)
    joblib.dump(X_test, processed_test_data.path)
    joblib.dump(y_train, test_labels_data.path)
    joblib.dump(y_test, test_labels_data.path)
