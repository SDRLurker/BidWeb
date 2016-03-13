# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from models import BidItem, Member
import json

current_member = u'admin'

def bidindex(request):
    biditems = BidItem.objects.filter(member=current_member)
    return render(request, 'index.html', {'biditems':biditems})

def bidindexid(request, bid):
    biditems = BidItem.objects.filter(member=current_member)
    try:
        item = BidItem.objects.get(id=bid, member=current_member)
    except Exception:
        return redirect('/bid')
    print item.data
    print json.dumps(item.data)
    return render(request, 'index.html', {'biditems':biditems, 'item':item})

def bidadd(request):
    actual_member = Member.objects.get(id=current_member)
    
    bid_name = request.POST['bid_name']
    prices = [ int(x) for x in request.POST.getlist('prices') ]
    base = int(request.POST['base'])
    rate = float(request.POST['rate'])
    checks = []
    for i in range(1,16):
        cstr = u"c" + str(i)
        if cstr in request.POST.getlist('checks'):
            checks.append(1)
        else:
            checks.append(0)
    #print checks
    data = {'prices':prices, 'base':base, 'rate':rate, 'checks':checks}
    #print data
    
    try:
        # #1 2단계 POST 변수에서 bid에 값이 존재하는 지 확인. #}
        bid = request.POST['bid']
        # #1 3-1단계 bid 값이 존재하면 BidItem의 해당 id 값으로 update(갱신) 처리. #}
        item = BidItem.objects.get(id=bid, member=actual_member)
        item.name = bid_name
        item.data = json.dumps(data)
        item.save()
    except Exception:
        # #1 3-2단계 bid 값이 존재하지 않으면 insert(Create, 추가) 처리. #}
        item = BidItem.objects.create(name=bid_name, data=json.dumps(data), member=actual_member)
    return redirect('/bid/'+str(item.id))

def biddel(request, bid):
    actual_member = Member.objects.get(id=current_member)
    try:
        item = BidItem.objects.get(id=bid)
    except Exception:
        return redirect('/bid')
    if actual_member == item.member:
        item.delete()
    return redirect('/bid')