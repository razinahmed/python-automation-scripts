import os
import shutil
import tarfile
import datetime
import argparse
import boto3
from botocore.exceptions import NoCredentialsError

def compress_directory(source_dir: str, output_filepath: str):
    """Compresses the source directory into a tar.gz file."""
    print(f"Compressing {source_dir} to {output_filepath}...")
    try:
        with tarfile.open(output_filepath, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return True
    except Exception as e:
        print(f"Compression failed: {e}")
        return False

def upload_to_s3(file_path: str, bucket_name: str, object_name: str):
    """Uploads a file to an S3 bucket."""
    print(f"Uploading {file_path} to s3://{bucket_name}/{object_name}...")
    s3 = boto3.client('s3')
    
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print("Upload Successful!")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available. Ensure your AWS environment variables are set.")
        return False
    except Exception as e:
        print(f"Upload failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Automated AWS S3 Backup Script")
    parser.add_argument("--source", "-s", type=str, required=True, help="Directory to backup")
    parser.add_argument("--bucket", "-b", type=str, required=True, help="Destination S3 bucket name")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source directory {args.source} does not exist.")
        return
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.basename(os.path.normpath(args.source))
    archive_name = f"{folder_name}_backup_{date_str}.tar.gz"
    temp_archive_path = os.path.join(os.environ.get("TEMP", "/tmp"), archive_name)
    
    # 1. Compress
    if compress_directory(args.source, temp_archive_path):
        # 2. Upload
        upload_to_s3(temp_archive_path, args.bucket, archive_name)
        
        # 3. Cleanup local temp file
        os.remove(temp_archive_path)
        print("Cleanup complete.")

if __name__ == "__main__":
    main()
