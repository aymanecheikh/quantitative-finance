from kfp.v2.dsl import pipeline
from .components.preprocessing import preprocess_data
from .components.training import train_model
from .components.evaluation import evaluate_model
from .components.register import register_model
from constants import SMALinearRegression as sma_lr


@pipeline(
    name=sma_lr.SMA_LINEAR_REGRESSION_MODEL,
    pipeline_root=sma_lr.BUCKET_ROOT
)
def sma_market_data_pipeline(
    project: str,
    location: str,
    data_bucket: str,
    data_folder: str,
    train_file: str,
):
    preprocess_task = preprocess_data(
        data_bucket=data_bucket,
        data_folder=data_folder,
        train_file=train_file,
    )

    train_task = train_model(
        preprocessed_train_data=preprocess_task.outputs['processed_train_data'],
        train_labels_data=preprocess_task.outputs['train_labels_data'],
    )

    evaluation_task = evaluate_model(
        processed_test_data=preprocess_task.outputs['processed_test_data'],
        test_labels_data=preprocess_task.outputs['test_labels_data'],
        model=train_task.outputs['model']
    )

    register_model(
        project=project,
        location=location,
        model=train_task.outputs['model'],
        metrics=evaluation_task.outputs['evaluation_metrics']
    )