import click
import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


class GoogleDriveService():

    def __init__(self, service_account_file_path):
        credentials = service_account.Credentials.from_service_account_file(service_account_file_path, scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.readonly'
        ])
        self._service = build('drive', 'v3', credentials=credentials)

    def download(self, file_id, file_path):
        if os.path.exists(file_path):
            raise Exception(f"File {file_path} already exists.")

        request = self._service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloaded {int(status.progress() * 100)}%...")

    def upload(self, source, target, mime):
        # Upload to the shared folder in chunks of 100 MB
        file_metadata = {'name': target, 'parents': ['1m80U0-iI372eMDzoEofNNjjRO2cPmCxV']}
        media = MediaFileUpload(source, mimetype=mime, chunksize=1024 * 1024 * 100, resumable=True)
        request = self._service.files().create(body=file_metadata, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}% ...")

        return response.get('id')

    def ls(self, root=None):
        pass


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file_id')
@click.argument('download_path', type=click.Path(exists=False))
def download(file_id, download_path):
    service = GoogleDriveService("./creds.json")
    service.download(file_id, download_path)


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target')
@click.argument('mime')
def upload(source, target, mime):
    service = GoogleDriveService("./creds.json")
    file_id = service.upload(source, target, mime)
    print(f"Uploaded file (file_id = {file_id})")


@cli.command()
def ls():
    click.echo('Not implemented')


if __name__ == "__main__":
    cli()
