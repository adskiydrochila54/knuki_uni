# from rest_framework.test import APITestCase
# from django.urls import reverse
# from rest_framework import status
# from .models import News
# from django.utils.text import slugify
#
# def create_news(title, body):
#     obj = News.objects.create(
#         status='draft',
#         slug=slugify(title),
#         title=title,
#         body=body
#     )
#     return obj
#
# class BaseAPITest(APITestCase):
#     def setUp(self):
#         self.client.credentials(HTTP_ACCEPT_LANGUAGE='ru')
#
# class NewsListAPITest(BaseAPITest): # Наследуемся от BaseAPITest
#     def setUp(self):
#         super().setUp()
#         News.objects.all().delete() # Чистим базу перед каждым тестом
#         create_news('News One', 'Text 1') # Используй разные заголовки
#         create_news('News Two', 'Text 2')
#
#     def test_news_list(self):
#         url = reverse('news-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
# class NewsCreateAPITest(BaseAPITest):
#     def test_create_news(self):
#         url = reverse('news-create')
#         data = {
#             'title': 'New title',
#             'body': 'New body',
#             'slug': 'new-title',
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # self.assertEqual(News.objects.count(), 1)
#
# class NewsUpdateAPITest(APITestCase):
#     def setUp(self):
#         self.news = create_news('Old', 'Old text')
#
#     def test_update_news(self):
#         url = reverse('news-detail', args=[self.news.slug])
#         data = {'title': 'Updated'}
#         response = self.client.patch(url, data, format='json', HTTP_ACCEPT_LANGUAGE='ru')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.news.refresh_from_db()
#         updated_title = self.news.safe_translation_getter('title', language_code='ru')
#         self.assertEqual(updated_title, 'Updated')
#
# class NewsDeleteAPITest(APITestCase):
#     def setUp(self):
#         self.news = create_news('To delete', '...')
#
#     def test_delete_news(self):
#         url = reverse('news-detail', args=[self.news.slug])
#         response = self.client.delete(url)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(News.objects.count(), 0)
#
# class NewsDetailAPITest(APITestCase):
#     def setUp(self):
#         self.news = create_news('Заголовок новости', 'Текст новости')
#         self.url = reverse('news-detail', args=[self.news.slug])
#
#     def test_get_detail_news(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], self.news.safe_translation_getter('title'))
#         self.assertEqual(response.data['body'], self.news.safe_translation_getter('body'))
#
#     def test_get_news_detail_not_found(self):
#         invalid_url = reverse('news-detail', args=['non-existent-slug'])
#         response = self.client.get(invalid_url)
#
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
