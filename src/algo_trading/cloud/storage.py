import logging, logger
from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    logging.info('Connecting to GCS')
    storage_client = storage.Client()
    logging.info('Fetching bucket')
    bucket = storage_client.bucket(bucket_name)
    logging.info('Fetching bucket blob')
    blob = bucket.blob(destination_blob_name)
    logging.info(f'Uploading {source_file_name} to bucket')
    blob.upload_from_filename(source_file_name)
    logging.info(
        f'File {source_file_name} uploaded to '
        f'{destination_blob_name} in bucket'
    )