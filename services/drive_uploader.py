import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

def upload_to_drive(filepath, folder_id):
    drive = authenticate_drive()

    file_name = os.path.basename(filepath)
    file_drive = drive.CreateFile({
        "title": file_name,
        "parents": [{"id": folder_id}]
    })
    file_drive.SetContentFile(filepath)
    file_drive.Upload()

    print(f"Uploaded {file_name} to Google Drive (folder: {folder_id})")
