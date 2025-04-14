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


def upload_folder_to_drive(folder_path, folder_id):
    drive = authenticate_drive()

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        print(f"No files found in {folder_path}")
        return

    for file_name in files:
        full_path = os.path.join(folder_path, file_name)
        file_drive = drive.CreateFile({
            "title": file_name,
            "parents": [{"id": folder_id}]
        })
        file_drive.SetContentFile(full_path)
        file_drive.Upload()

        print(f"Uploaded {file_name} to Google Drive (folder: {folder_id})")
