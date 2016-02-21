from django.test import TestCase
from django.utils import timezone
from bid.models import Member

# Create your tests here.
class IndexTestPage(TestCase):
    def testIndexPage(self):
        # when
        response = self.client.get('/')
        # then
        self.assertEqual(response.status_code,200)
        self.assertIn(response.content, "Hello World!")
    
    def testAddMember(self):
        # when
        member = Member.objects.create(id=u'admin', created_date=timezone.now())
        # then
        self.assertEqual(Member.objects.count(), 1)
        actual = Member.objects.first()
        self.assertEqual(member, actual)