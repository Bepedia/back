from google.cloud import storage
import os


class StorageIO:

    def __init__(self):
        self.client = storage.Client.from_service_account_json(os.getcwd() + '/config/gae-service-account.json')

    def post_img(self, file, file_name):
        bucket = self.client.bucket('bepedia-media')
        blob = bucket.blob(file_name)
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()
        return 'https://storage.cloud.google.com/bepedia-media/' + file_name
