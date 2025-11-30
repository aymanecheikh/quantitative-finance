from kfp.v2.dsl import component, Input, Output, Dataset, Model, Artifact
from constants import MLModels as mlm


@component(base_image=mlm.BASE_IMAGE)
def evaluate_model(
    processed_test_data: Input[Dataset],
    test_labels_data: Input[Dataset],
    model: Input[Model],
    evaluation_metrics: Output[Artifact],
):
    import joblib
    from sklearn.metrics import mean_squared_error, r2_score
    import json
    import os


    X_test = joblib.load(processed_test_data.path)
    y_test = joblib.load(test_labels_data.path)


    model_path = os.path.join(model.path, "model")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No model found at {model_path}")

    _model = joblib.load(model_path)


    y_pred = _model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)


    os.makedirs(evaluation_metrics.path, exist_ok=True)
    metrics_path = os.path.join(evaluation_metrics.path, "metrics.json")

    metrics = {"mse": mse, "r2": r2}

    with open(metrics_path, "w") as f:
        json.dump(metrics, f)

    print(f"Saved evaluation metrics to: {metrics_path}")
