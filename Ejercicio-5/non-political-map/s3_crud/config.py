from dotenv import load_dotenv
import os

load_dotenv()


def get_creds():
    return {
        "aws_key": os.getenv('AWS_ACCESS_KEY_ID'),
        "aws_secret": os.getenv('AWS_SECRET_ACCESS_KEY')
    }
