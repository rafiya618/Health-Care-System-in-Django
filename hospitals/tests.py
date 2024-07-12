from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import *


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_post_success(self):
        response = self.client.post(reverse('contact'), {'name': 'John', 'contact': '123', 'email': 'john@example.com', 'subject': 'Test', 'message': 'Test Message'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_admin_home_view(self):
        # Assuming user is authenticated as staff
        user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.client.force_login(user)
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_home.html')

    def test_doctor_page_view(self):
        # Assuming user is authenticated as staff
        user = User.objects.create_user(username='doctor', password='doctorpassword', is_staff=True)
        self.client.force_login(user)
        response = self.client.get(reverse('doctor_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prescription_test_report.html')

    def test_buy_drug_view(self):
        response = self.client.get(reverse('buy_drug_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buy_page.html')



    def test_successMsg_view(self):
        response = self.client.get(reverse('success', args=[100]))  # Assuming the argument 100 for amount
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')