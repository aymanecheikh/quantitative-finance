from kfp.v2.dsl import component, Input, Output, Dataset, Model, Artifact
from ....constants import KubeFlowConstants as kfc


@component(base_image=kfc.BASE_IMAGE)
def evaluate_model(
    processed_test_data: Input[Dataset],
    test_labels_data: Input[Dataset],
    model: Input[Model],
    evaluation_metrics: Output[Artifact]
):
    import pandas as pd
    import joblib
    from sklearn.metrics import mean_squared_error, r2_score
    import json
    import os


    X_test = joblib.load(processed_test_data.path)
    y_test = joblib.load(test_labels_data.path)


    model_path = os.path.join(model.path, 'model')
    if os.path.exists(model_path):
        _model = joblib.load(model_path)
        print(f'Loaded model from: {model_path}')
    else:
        raise FileNotFoundError(f"No mode found in {model.path}")
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')
    linear_regression_report = {
        "Mean Squared Error": mse,
        "R-Squared": r2
    }

    with open(evaluation_metrics.path, "w") as f:
        json.dump(linear_regression_report)