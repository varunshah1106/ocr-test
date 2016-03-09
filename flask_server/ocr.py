from __future__ import print_function
import httplib2
import os
import base64
from PIL import Image
from pytesseract import image_to_string
from apiclient.http import MediaFileUpload
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


class VisionApi:
    def __init__(self):
        self.credentials = self.get_credentials()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def ocr(self, image):
        """Shows basic usage of the Google Drive API.

        Creates a Google Drive API service object and outputs the names and IDs
        for up to 10 files.
        """
        print(image_to_string(Image.open('temp.jpg'), lang='sa'))
        credentials = self.credentials
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('drive', 'v3', http=http)
        im = Image.open('temp.jpg')
        im.save('temp.pdf', "PDF", resolution=100.0)
        media_body = MediaFileUpload('temp.jpg', resumable=True)
        print(dir(service))
        body = {
            'title': 'temp.jpg',
            'ocr': True
        }
        results = service.files().create(
            body=body, media_body=media_body).execute()
        file_id = results['id']
        file = service.files().get(fileId=file_id).execute()
        print(dir(service.files().create()))
        print(file)
