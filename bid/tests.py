# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from bid.models import Member, BidItem
from django.db import connection, reset_queries
#from django.test.utils import override_settings
from django.conf import settings

# Create your tests here.
class IndexTestPage(TestCase):
    def testIndexPage(self):
        # when
        response = self.client.get('/')
        # then
        self.assertEqual(response.status_code,200)
        self.assertIn(response.content, "Hello World!")
        
    def print_queries(self, name):
        print 
        print name
        for query in connection.queries:
            print query['sql']
    
    @override_settings(DEBUG=True)
    def testAddMember(self):
        reset_queries()
        # when
        member = Member.objects.create(id=u'admin', created_date=timezone.now())
        
        # then
        self.assertEqual(Member.objects.count(), 1)
        actual = Member.objects.first()
        self.assertEqual(member, actual)
        
        self.print_queries('AddMember')
        
    @override_settings(DEBUG=True) 
    def testAddBidItem(self):
        reset_queries()
        # given, when
        member = Member.objects.create(id=u'admin', created_date=timezone.now())
        bid_data = {'prices':[294084627,301735938,292385989,298335686,294935434,302583770,291535182,300034325,303434577,300885132,297484880,299183518,293233821,296634073,295786241], 
                'base':297484880, 'rate':87.995, 'checks':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
        biditem = BidItem.objects.create(name=u'쉰들러', data=bid_data, member=member)
        
        # then
        self.assertEqual(Member.objects.count(),1)
        self.assertEqual(BidItem.objects.count(),1)
        
        actual_biditem = BidItem.objects.get(id=biditem.id)
        self.assertEqual(actual_biditem, biditem)
        self.assertEqual(actual_biditem.member, member)
        
        self.print_queries('AddBidItem')    

        
    