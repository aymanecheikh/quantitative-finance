from kfp.v2.dsl import pipeline
from components.preprocessing import preprocess_data
from components.training import train_model
from components.evaluation import evaluate_model
from ...constants import MLModels as mlm


@pipeline(
    name=mlm.SMA_LINEAR_REGRESSION_MODEL.value,
    
)