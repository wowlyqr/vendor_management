
from datetime import datetime
import random
import string
from werkzeug.utils import secure_filename
import boto3

S3_BUCKET_NAME = "vendor-management-images"
# AWS S3 Configuration
s3 = boto3.client(
    's3',
    aws_access_key_id="AKIAVX3YTTSGO4R66C36",
    aws_secret_access_key="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"
)

def serialize_data(user):
    user_dict = user.to_mongo().to_dict()  # Convert to dict
    user_dict["_id"] = str(user_dict["_id"])  # Convert ObjectId to string
    return user_dict


def create_response(success, message, data=None, error=None, status_code=200):
    return {
        "success": success,
        "message": message,
        "data": data if data else {},
        "error": error if error else None
    }, status_code


def generate_uniform_unique_id(prefix = None):
    # prefix = "pl"
    constant = "VM"
    
    # Generate two 4-digit random segments
    random_segment1 = ''.join(random.choices(string.ascii_uppercase, k=4))
    random_segment2 = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    # Combine to form the ID
    formatted_id = f"{prefix}-{random_segment1}-{constant}-{random_segment2}"
    return formatted_id


def upload_file_to_s3(file,folder=""):
    try:
        # Secure the original filename
        filename = secure_filename(file.filename)

        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Set folder path like 'post/images' or 'post/documents'
        folder = folder.strip("/")  # Remove leading/trailing slashes just in case

        # Build the full S3 key path
        s3_key = f"{folder}/{timestamp}_{filename}"

        # Upload the file to S3
        s3.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        # Return the public S3 URL
        s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return s3_url

    except Exception as e:
        raise Exception(f"Failed to upload to S3: {str(e)}")