#pip install google-api-python-client
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

load_dotenv()
SCOPES = [os.getenv('GOOGLE_SCOPE')]
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
PARENT_FOLDER_ID = os.getenv('PARENT_FOLDER_ID')

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

#https://drive.google.com/file/d/1o7kbL39Hy6u_c9KTxSGQDJN-hY_e8pV2/view?usp=sharing
def upload_photo(file_path:str):
    """Upload File to Parent Folder and prints the folder ID
    Returns : Folder Id
    NOTE: upload speed may vary depend on Internet Speed"""
    creds = authenticate()
    try:
        service = build('drive','v3',credentials=creds)
        file_metadata = {
          'name': file_path.replace(".jpg",""), 
          # I hope the .jpg string only shows up in the end of very and of the filename
          'parents':[PARENT_FOLDER_ID],
          "role": "reader",
          "type": "anyone",
          'allowFileDiscovery': True
        }
        file = service.files().create(
            body=file_metadata,
            media_body=file_path,
            fields="id"
        ).execute()
        print(f'File ID: "{file.get("id")}".')
        return file.get("id")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def create_folder(fileName):
  """Create a folder and prints the folder ID
  Returns : Folder Id
  """
  creds = authenticate()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": fileName,
        "mimeType": "application/vnd.google-apps.folder" ,
        'parents':[PARENT_FOLDER_ID],
        "role": "reader",
        "type": "anyone",
        'allowFileDiscovery': True
    }
    # pylint: disable=maybe-no-member
    file = service.files().create(body=file_metadata, fields="id").execute()
    newFolderURL = f'Folder URL: https://drive.google.com/drive/u/0/folders/"{file.get("id")}".'
    print(newFolderURL)
    return file.get("id")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def upload_to_folder(folder_id, file_path):
  """Upload a file to the specified folder and prints file ID, folder ID
  Args: Id of the folder
  Returns: ID of the file uploaded
  NOTE: upload speed may vary depend on Internet Speed"""
  creds = authenticate()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file_metadata = {
        "name": file_path.replace(".jpeg",""), 
        # I hope the .jpg string only shows up in teh very and of the filename
        "parents": [folder_id],
        "role": "reader",
        "type": "anyone",
        'allowFileDiscovery': True
        }
    media = MediaFileUpload(
        file_path, mimetype="image/jpeg", resumable=True
    )
    # pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File ID: "{file.get("id")}".')
    return file.get("id")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return None
  
def trashFileOrFolder(id):
  """Move a folder/file to Trash"""
  creds = authenticate()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    body_value = {'trashed': True}
    # pylint: disable=maybe-no-member
    file = (
        service.files().update(fileId=id,body=body_value).execute()
    )
    print(f'File deleted: "{file}".')
  except HttpError as error:
    print(f"An error occurred: {error}")

def deleteFileOrFolder(id):
  """Delete a folder/file"""
  creds = authenticate()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    file = (
        service.files().delete(fileId=id).execute()
    )
    print(f'File deleted: "{file}".')
  except HttpError as error:
    print(f"An error occurred: {error}")    

def emptyTrash():
  """Empty Trash"""
  creds = authenticate()
  try:
    service = build("drive", "v3", credentials=creds)
    response = service.files().emptyTrash().execute()
    return response
  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def search_drive(name):
  """Search files in drive location containing a certain string"""
  creds = authenticate()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)
    files = []
    page_token = None
    while True:
      # pylint: disable=maybe-no-member
      response = (
          service.files()
          .list(
              q=f"name contains '{name}'",
              spaces="drive",
              fields="nextPageToken, files(id, name)",
              pageToken=page_token
          )
          .execute()
      )
      for file in response.get("files", []):
        # Process change
        print(f'Found file: {file.get("name")}, {file.get("id")}')
      files.extend(response.get("files", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break
  except HttpError as error:
    print(f"An error occurred: {error}")
    files = None
  return files
