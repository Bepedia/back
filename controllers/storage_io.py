from google.cloud import storage
import os
import uuid


class StorageIO:

    def __init__(self):
        self.client = storage.Client.from_service_account_json(os.getcwd() + '/config/gae-service-account.json')

    def post_img(self, file, file_extension, collection):
        bucket = self.client.bucket('bepedia-media')
        blob = bucket.blob(f"{collection}/{str(uuid.uuid4())}.{file_extension}")
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()
        return blob.public_url
