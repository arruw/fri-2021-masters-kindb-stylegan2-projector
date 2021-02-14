import click
import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class GoogleDriveService():

    def __init__(self, service_account_file_path):
        credentials = service_account.Credentials.from_service_account_file(service_account_file_path, scopes=[
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

    def upload(self, blob):
        pass

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
def upload():
    click.echo('Not implemented')


@cli.command()
def ls():
    click.echo('Not implemented')


if __name__ == "__main__":
    cli()
