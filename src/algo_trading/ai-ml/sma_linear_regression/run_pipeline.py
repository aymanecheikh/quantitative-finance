from google.cloud import aiplatform
from kfp import compiler
from .pipeline import sma_market_data_pipeline

from constants import MLModels as mlm, SMALinearRegression as sma_lr


compiler.Compiler().compile(
    pipeline_func=sma_market_data_pipeline,
    package_path=sma_lr.PACKAGE_PATH
)


def main():
    aiplatform.init(
        project=mlm.PROJECT,
        location=mlm.REGION
    )

    pipeline_job = aiplatform.PipelineJob(
        display_name=sma_lr.SMA_LINEAR_REGRESSION_MODEL,
        template_path=sma_lr.PACKAGE_PATH,
        pipeline_root=mlm.BUCKET_ROOT,
        parameter_values={
            "project": mlm.PROJECT,
            "location": mlm.REGION,
            "data_bucket": mlm.BUCKET_NAME,
            "data_folder": mlm.DATA_FOLDER,
            "train_file": "SOXL.csv" # Testing, to be looped
        },
        enable_caching=True
    )

    pipeline_job.run(
        service_account=mlm.PIPELINE_SERVICE_ACCOUNT,
        sync=True
    )


if __name__ == "__main__":
    main()