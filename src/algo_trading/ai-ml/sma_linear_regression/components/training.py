from kfp.v2.dsl import component, Input, Output, Dataset, Model
from constants import MLModels as mlm


@component(base_image=mlm.BASE_IMAGE)
def train_model(
    preprocessed_train_data: Input[Dataset],
    train_labels_data: Input[Dataset],
    model: Output[Model]
):
    import pandas as pd
    import joblib
    from sklearn.linear_model import LinearRegression
    import os
    
    
    X_train = joblib.load(preprocessed_train_data.path)
    y_train = joblib.load(train_labels_data.path)

    
    def define_model():
        _model = LinearRegression()
        return _model
    
    def train_model(_model, X_train, y_train):
        history = _model.fit(X_train, y_train)
        return _model, history
    
    
    _model = define_model()
    _model, history = train_model(_model, X_train, y_train)


    os.makedirs(model.path, exist_ok=True)    
    save_model_path = os.path.join(model.path, "model")
    joblib.dump(_model, save_model_path)
    print(f"Model saved to: {save_model_path}")