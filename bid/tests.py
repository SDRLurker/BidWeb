# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from bid.models import Member, BidItem
# Test모듈에서 SQL 로그 출력 위해 필요한 모듈들
# https://docs.djangoproject.com/en/1.9/faq/models/
# http://stackoverflow.com/questions/7447134/how-do-you-set-debug-to-true-when-running-a-django-test
from django.db import connection, reset_queries
from django.test.utils import override_settings
from django.conf import settings

# Create your tests here.
class IndexTestPage(TestCase):        
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
        
    # 다대일 관계 given의 중복제거를 위해 추가한 함수
    # 'admin' member 하나에 2개의 biditem을 추가한다.
    def makeTestBidItem(self):
        member = Member.objects.create(id=u'admin', created_date=timezone.now())
        bid_data = {'prices':[294084627,301735938,292385989,298335686,294935434,302583770,291535182,300034325,303434577,300885132,297484880,299183518,293233821,296634073,295786241], 
                'base':297484880, 'rate':87.995, 'checks':[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
        biditem = BidItem.objects.create(name=u'test1', data=bid_data, member=member)
        BidItem.objects.create(name=u'test2', data=bid_data, member=member)
        
        return member, bid_data, biditem
    
    # 다대일 관계 저장 하기
    @override_settings(DEBUG=True) 
    def testAddBidItem(self):
        reset_queries()
        # given, when
        member, bid_data, biditem = self.makeTestBidItem()
        # then
        self.assertEqual(Member.objects.count(),1)
        self.assertEqual(BidItem.objects.count(),2)
        actual_biditem = BidItem.objects.get(id=biditem.id)
        self.assertEqual(actual_biditem, biditem)
        self.assertEqual(actual_biditem.member, member)
        
        self.print_queries('AddBidItem')
    
    #다대일 관계 삭제하기
    @override_settings(DEBUG=True) 
    def testDelMember(self):
        reset_queries()
        # given
        member, bid_data, biditem = self.makeTestBidItem()
        # when
        member.delete()
        #then
        self.assertEqual(Member.objects.count(), 0)
        self.assertEqual(BidItem.objects.count(), 0)
        
        self.print_queries('DelMember')
    
    #다대일 관계 조회하기
    @override_settings(DEBUG=True) 
    def testSelectFromMember(self):
        reset_queries()
        # given
        member, bid_data, biditem = self.makeTestBidItem()
        # when
        actual_member = Member.objects.get(id=member.id)
        actual_biditem = actual_member.biditem_set.get(id=biditem.id)
        # then
        self.assertEqual(biditem, actual_biditem)
        
        self.print_queries('SelectFromMember')
    @override_settings(DEBUG=True) 
    def testSelectFromBidItem(self):
        reset_queries()
        # given
        member, bid_data, biditem = self.makeTestBidItem()
        # when
        actual_biditem = BidItem.objects.get(id=biditem.id)
        actual_member = actual_biditem.member
        # then
        self.assertEqual(member, actual_member)
        
        self.print_queries('SelectFromBidItem')
        
        
        
        
        
    