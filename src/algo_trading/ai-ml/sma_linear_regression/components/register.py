from kfp.v2.dsl import component, Input, Model, Artifact
from constants import MLModels as mlm


@component(base_image=mlm.BASE_IMAGE)
def register_model(
    project: str,
    location: str,
    model: Input[Model],
    metrics: Input[Artifact],
):
    import os
    import json
    from google.cloud import aiplatform

    aiplatform.init(project=project, location=location)

    metrics_path = os.path.join(metrics.path, "metrics.json")
    if not os.path.exists(metrics_path):
        raise FileNotFoundError(f"No metrics.json found at {metrics_path}")

    with open(metrics_path, "r") as f:
        evaluation_metrics = json.load(f)

    model_file = os.path.join(model.path, "model")
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"No model file found at {model_file}")

    labels = {
        "model_type": "linear_regression",
    }
    print(f"Labels: {labels}")

    model_display_name = "sma-linear-regression"

    models = aiplatform.Model.list(
        filter=f'display_name="{model_display_name}"'
    )

    parent_model = models[0].resource_name if models else None
    if parent_model:
        print(f"Parent Model Resource Name: {parent_model}")
    else:
        print("No existing model found with the specified display name")

    uploaded_model: aiplatform.Model = aiplatform.Model.upload(
        artifact_uri=model.uri,
        display_name=model_display_name,
        parent_model=parent_model,
        serving_container_image_uri="europe-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-6:latest",
        labels=labels,
    )

    print("Model uploaded successfully")

    beautified_json = json.dumps(evaluation_metrics, indent=4)
    print(beautified_json)

    uploaded_model.update(
        description=f"SMA Linear Regression: Evaluation Metrics:\n{beautified_json}"
    )

    print(f"Model registered with display name '{model_display_name}'")
    print(f"Model registered with ID: {uploaded_model.resource_name}")
    print(f"Evaluation metrics: {evaluation_metrics}")
