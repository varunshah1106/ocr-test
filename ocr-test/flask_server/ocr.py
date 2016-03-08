import argparse
import base64
import os
import re
import sys

from googleapiclient import discovery
from googleapiclient import errors
import nltk
from nltk.stem.snowball import EnglishStemmer
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
BATCH_SIZE = 10


class VisionApi:
    """Construct and use the Google Vision API service."""

    def __init__(self, api_discovery_file='vision_api.json'):
        self.credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_text(self, image, num_retries=3, max_results=6):
        """Uses the Vision API to detect text in the given file.

        images = {}
        for filename in input_filenames:
            with open(filename, 'rb') as image_file:
                images[filename] = image_file.read()
        """
        #print image_base64
        batch_request = []
        batch_request.append({
            'image': {
                'content': base64.b64encode(image)
            },
            'features': [{
                'type': 'TEXT_DETECTION',
                'maxResults': max_results,
            }]
        })

        request = self.service.images().annotate(
            body={'requests': batch_request})
        responses = request.execute(num_retries=num_retries)
        return responses['responses']
        """
        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}
            text_response = {}
            for filename, response in zip(images, responses['responses']):
                if 'error' in response:
                    print("API Error for %s: %s" % (
                            filename,
                            response['error']['message']
                            if 'message' in response['error']
                            else ''))
                    continue
                if 'textAnnotations' in response:
                    text_response[filename] = response['textAnnotations']
                else:
                    text_response[filename] = []
            return text_response
        except errors.HttpError, e:
            print("Http Error for %s: %s" % (filename, e))
        except KeyError, e2:
            print("Key error: %s" % e2)
        """
