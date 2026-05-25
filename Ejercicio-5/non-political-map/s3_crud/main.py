from utils.parquet_service import ParquetService
from utils.s3_service import S3Service

def create_bucket(bucket_name: str):
    s3_service = S3Service()
    s3_service.create_bucket(bucket_name)

def upload_file(bucket_name: str, file_path: str, object_key: str):
    s3_service = S3Service()
    s3_service.upload_file(file_path, bucket_name=bucket_name, object_key=object_key)
    

def main():
    parquet_service = ParquetService()
    print(parquet_service.read_file("kpi.parquet"))
    print("Uploading file...")
    bucket_name = "lemoncode-non-political-map-1"
    upload_file(bucket_name, "./kpi.parquet", "kpi.parquet")

if __name__ == "__main__":
    main()
