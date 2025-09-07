from django.test import TestCase, Client

# Create your tests here.

from django.urls import reverse
from django.template.loader import render_to_string

class HomeViewTests(TestCase):
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.client = Client()
        self.url = reverse('home') # Припускаючи, що name='index' в urls.py
    
    def test_home_view_returns_correct_template(self):
        """Тест, що view повертає правильний шаблон"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
    
