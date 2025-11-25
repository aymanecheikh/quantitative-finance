from enum import Enum
from typing import Final
import logging, logger

logging.info('Initializing constants')

TOP_N_SCANNER_RESULTS: Final = 20

HOST: Final = "127.0.0.1"
PORT: Final = 4002
CLIENT_ID: Final = 1


class Fundamentals(Enum):
    FINANCIAL_SUMMARY = "ReportsFinSummary"
    COMPANY_OWNERSHIP = "ReportsOwnership"
    COMPANY_FINANCIAL_OVERVIEW = "ReportSnapshot"
    FINANCIAL_STATEMENTS = "ReportsFinStatements"
    ANALYST_ESTIMATES = "RESC"
    COMPANY_CALENDAR = "CalendarReport"
