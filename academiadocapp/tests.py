from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Requests

class RequestsModelTestOne(TestCase):

    """
    This test suite checks the verbose name of the delivery_email field, 
    the max length of the reference field, 
    the default value of the purpose and status fields, 
    and the __str__ method of the Requests model class.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        Requests.objects.create(
            creator= self.user,
            delivery_email='user@example.com', 
            agreement=True, 
            pdf_file=None
        )

    def test_email_label(self):
        request = Requests.objects.get(id=1)
        field_label = request._meta.get_field('delivery_email').verbose_name
        self.assertEqual(field_label, 'delivery email')

    def test_reference_max_length(self):
        request = Requests.objects.get(id=1)
        max_length = request._meta.get_field('reference').max_length
        self.assertEqual(max_length, 10)

    def test_purpose_default(self):
        request = Requests.objects.get(id=1)
        purpose_default = request._meta.get_field('purpose').default
        self.assertEqual(purpose_default, 'OF')

    def test_status_default(self):
        request = Requests.objects.get(id=1)
        status_default = request._meta.get_field('status').default
        self.assertEqual(status_default, 'SU')

    def test_str_method(self):
        request = Requests.objects.get(id=1)
        expected_str = request.reference
        self.assertEqual(str(request), expected_str)



class RequestsModelTestTwo(TestCase):

    """
    These tests cover some basic functionality of the Requests model such as generating a new reference number, 
    serializing the model instance and returning its reference number as a string.

    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='secret'
        )
        self.request = Requests.objects.create(
            creator=self.user,
            delivery_email='test@example.com',
            purpose='PE',
            agreement=True
        )

    def test_create_new_ref_no(self):
        ref_no = Requests.create_new_ref_no()
        self.assertEqual(len(str(ref_no)), 10)

    def test_serialize(self):
        expected_serialized_data = {
            'reference': self.request.reference,
            'creator': self.user.username,
            'status': self.request.status,
            'date': self.request.date.strftime('%b %d %Y, %I:%M %p'),
        }
        self.assertEqual(self.request.serialize(), expected_serialized_data)

    def test_str(self):
        self.assertEqual(str(self.request), self.request.reference)



class RequestsModelTestThree(TestCase):

    """
    These tests check that the create_new_ref_no() method returns a 10-character string, 
    that the model fields are set and retrieved correctly, 
    that the default values are set correctly, 
    and that the serialize() method returns a dictionary with the correct keys and values.

    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.request = Requests.objects.create(
            creator=self.user,
            delivery_email='test@example.com',
            purpose='OF',
            agreement=True,
            status='SU',
            pdf_file=None
        )

    def test_create_new_ref_no(self):
        ref_no = Requests.create_new_ref_no()
        self.assertIsInstance(ref_no, str)
        self.assertEqual(len(ref_no), 10)

    def test_model_fields(self):
        self.assertEqual(str(self.request), self.request.reference)
        self.assertEqual(self.request.creator, self.user)
        self.assertEqual(self.request.delivery_email, 'test@example.com')
        self.assertEqual(self.request.purpose, 'OF')
        self.assertEqual(self.request.agreement, True)
        self.assertEqual(self.request.status, 'SU')
        self.assertEqual(self.request.pdf_file, None)

    def test_model_defaults(self):
        self.assertEqual(self.request.status, 'SU')
        self.assertEqual(self.request.purpose, 'OF')

    def test_model_methods(self):
        serialized_request = self.request.serialize()
        self.assertIsInstance(serialized_request, dict)
        self.assertEqual(serialized_request['reference'], self.request.reference)
        self.assertEqual(serialized_request['creator'], self.user.username)
        self.assertEqual(serialized_request['status'], self.request.status)
        self.assertEqual(serialized_request['date'], self.request.date.strftime("%b %d %Y, %I:%M %p"))
