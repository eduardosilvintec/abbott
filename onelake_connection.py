# cd "C:\Users\eduar\source\repos\Abbott-New"
#.\.venv\Scripts\Activate.ps1
# deactivate

from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import AzureCliCredential
import os

# Ensure Azure CLI path is accessible
os.environ["PATH"] += r";C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin"

# Parameters
ACCOUNT_NAME   = "onelake"
WORKSPACE_NAME = "Abbott"
LAKEHOUSE_NAME = "Abbott"
LOCAL_FILE_PATH = r"C:\Users\eduar\Downloads\ABT_daily.csv"
DEST_DIR_PATH  = f"{LAKEHOUSE_NAME}.Lakehouse/Files"
DEST_FILE_NAME = os.path.basename(LOCAL_FILE_PATH)
ONELAKE_FILE_PATH = f"{DEST_DIR_PATH}/{DEST_FILE_NAME}"

def upload_csv_to_onelake():
    account_url = f"https://{ACCOUNT_NAME}.dfs.fabric.microsoft.com"
    credential = AzureCliCredential()
    service_client = DataLakeServiceClient(account_url=account_url, credential=credential)
    file_system = service_client.get_file_system_client(file_system=WORKSPACE_NAME)
    directory_client = file_system.get_directory_client(DEST_DIR_PATH)

    file_client = directory_client.get_file_client(DEST_FILE_NAME)
    with open(LOCAL_FILE_PATH, "rb") as data:
        file_client.upload_data(data, overwrite=True)

    print(f"File successfully uploaded to OneLake at: {ONELAKE_FILE_PATH}")

if __name__ == "__main__":
    upload_csv_to_onelake()