import csv
import json
import random
import string
from os.path import join
from unittest.mock import patch

import vcr
from django.http import StreamingHttpResponse
from django.test import TestCase
from django.urls import reverse
from request_broker import settings
from rest_framework.test import APIRequestFactory

from .models import MachineUser, User
from .routines import ProcessRequest
from .views import (DeliverEmailView, DownloadCSVView, ProcessEmailRequestView,
                    ProcessRequestView)

transformer_vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir=join(settings.BASE_DIR, 'fixtures/cassettes'),
    record_mode='once',
    match_on=['path', 'method'],
    filter_query_parameters=['username', 'password'],
    filter_headers=['Authorization', 'X-ArchivesSpace-Session'],
)

FIXTURES_DIR = join(settings.BASE_DIR, "fixtures")

ROUTINES = (
    ('process_request.json', ProcessRequest),
)

VIEWS = (
    ('process_request.json', ProcessRequestView),
)


def random_list():
    return random.sample(string.ascii_lowercase, random.randint(2, 10))


def json_from_fixture(filename):
    with open(join(FIXTURES_DIR, filename), "r") as df:
        return json.load(df)


class TestUsers(TestCase):

    def test_user(self):
        user = User(
            first_name="Patrick",
            last_name="Galligan",
            email="pgalligan@rockarch.org")
        self.assertEqual(user.full_name, "Patrick Galligan")
        self.assertEqual(str(user), "Patrick Galligan <pgalligan@rockarch.org>")

    def test_machineuser(self):
        system = 'Zodiac'
        user = MachineUser(system_name="Zodiac")
        self.assertEqual(str(user), system)


class TestRoutines(TestCase):

    def test_routines(self):
        for cassette, routine in ROUTINES:
            with transformer_vcr.use_cassette(cassette):
                routines = ProcessRequest().process_readingroom_request(['/repositories/2/archival_objects/8457'])
                self.assertEqual(routines, 'test')

    @patch("process_request.routines.ProcessRequest.get_data")
    def test_process_email_request(self, mock_get_data):
        mock_get_data.return_value = json_from_fixture("as_data.json")
        to_process = random_list()
        processed = ProcessRequest().process_email_request(to_process)
        self.assertEqual(len(to_process), len(processed))
        self.assertTrue([isinstance(item, dict) for item in processed])


class TestViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_processrequestview(self):
        for v in VIEWS:
            with transformer_vcr.use_cassette(v[0]):
                request = self.factory.post(reverse('process-request'), {"items": ["/repositories/2/archival_objects/8457"]}, format='json')
                response = v[1].as_view()(request)
                self.assertEqual(response.status_code, 200)

    def exception_handling(self, patched_fn, exception_text, view_str, view):
        patched_fn.side_effect = Exception(exception_text)
        request = self.factory.post(
            reverse(view_str), {"items": random_list()}, format="json")
        response = view.as_view()(request)
        self.assertEqual(
            response.status_code, 500, "Request did not return a 500 response")
        self.assertEqual(
            response.data["detail"], exception_text, "Exception string not in response")

    @patch("process_request.routines.ProcessRequest.get_data")
    def test_downloadcsvview(self, mock_get_data):
        mock_get_data.return_value = json_from_fixture("as_data.json")
        to_process = random_list()
        request = self.factory.post(
            reverse("download-csv"), {"items": to_process}, format="json")
        response = DownloadCSVView.as_view()(request)
        self.assertTrue(isinstance(response, StreamingHttpResponse))
        self.assertEqual(response.get('Content-Type'), "text/csv")
        self.assertIn("attachment;", response.get('Content-Disposition'))
        f = response.getvalue().decode("utf-8")
        reader = csv.reader(f.splitlines())
        self.assertEqual(
            sum(1 for row in reader), len(to_process) + 1,
            "Incorrect number of rows in CSV file")

        self.exception_handling(mock_get_data, "foobar", "download-csv", DownloadCSVView)

    @patch("process_request.routines.ProcessRequest.process_email_request")
    def test_process_email_request_view(self, mock_processed):
        mock_processed.return_value = [json_from_fixture("as_data.json")]
        to_process = random_list()
        request = self.factory.post(
            reverse("process-email"), {"items": to_process}, format="json")
        response = ProcessEmailRequestView.as_view()(request)
        self.assertEqual(response.status_code, 200, "Response error: {}".format(response.data))
        self.assertEqual(len(response.data), 1)

        self.exception_handling(mock_processed, "foobar", "process-email", ProcessEmailRequestView)

    @patch("process_request.routines.DeliverEmail.send_message")
    def test_send_email_request_view(self, mock_sent):
        mock_sent.return_value = "email sent"
        to_process = random_list()
        request = self.factory.post(
            reverse("deliver-email"),
            {"items": to_process, "to_address": "test@example.com", "subject": "DIMES list"},
            format="json")
        response = DeliverEmailView.as_view()(request)
        self.assertEqual(response.status_code, 200, "Response error: {}".format(response.data))
        self.assertEqual(len(response.data), 1)

        self.exception_handling(mock_sent, "foobar", "process-email", DeliverEmailView)
