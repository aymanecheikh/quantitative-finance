from enum import Enum
from typing import Final
import logging, logger


logging.info('Initializing constants')


class IBAPI:
    HOST: Final = "127.0.0.1"
    PORT: Final = 4002
    CLIENT_ID: Final = 1
    TOP_N_SCANNER_RESULTS: Final = 20

    
class MLModels:
    PROJECT: Final = "quantitative-finance-479721"
    REGION: Final = "europe-west2"
    SMA_LINEAR_REGRESSION_MODEL: Final = "sma-linear-regression"
    PACKAGE_PATH: Final = f"{SMA_LINEAR_REGRESSION_MODEL.replace('-', '_')}.json"
    BUCKET_NAME: Final = "historical-market-data"
    BUCKET_ROOT: Final = f"gs://{BUCKET_NAME}/sma-market-data-pipeline"
    DATA_FOLDER: Final = "raw-data"
    PIPELINE_SERVICE_ACCOUNT = (
        "vertex-pipelines-sa@quantitative-finance-479721.iam.gserviceaccount.com"
    )
    BASE_IMAGE: Final = "us-docker.pkg.dev/deeplearning-platform-release/gcr.io/sklearn-cpu"
    SERVING_CONTAINER_IMAGE: Final = "europe-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-6:latest"


class Fundamentals(Enum):
    FINANCIAL_SUMMARY = "ReportsFinSummary"
    COMPANY_OWNERSHIP = "ReportsOwnership"
    COMPANY_FINANCIAL_OVERVIEW = "ReportSnapshot"
    FINANCIAL_STATEMENTS = "ReportsFinStatements"
    ANALYST_ESTIMATES = "RESC"
    COMPANY_CALENDAR = "CalendarReport"