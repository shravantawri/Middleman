from random import randint
from google.cloud import storage
import os


def generate_sku_id(category, design_code):
    s = design_code + category[0]
    for _ in range(5):
        s = s + str(randint(0, 9))
    return s


def upload_image_to_bucket(image_file):
    # Create a Cloud Storage client.
    gcs = storage.Client.from_service_account_json(
        '/Users/kritika/my_projects/middleman2/application/middleman-sa.json')

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket("middleman_data")

    # Create a new blob and upload the file's content.
    blob = bucket.blob(image_file.filename)

    blob.upload_from_string(
        image_file.read(),
        content_type=image_file.content_type
    )

    # Make the blob public. This is not necessary if the
    # entire bucket is public.
    # See https://cloud.google.com/storage/docs/access-control/making-data-public.
    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url
