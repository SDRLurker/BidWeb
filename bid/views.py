# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import BidItem, Member
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
    # print("item.data", item.data)
    # print("json.dumps(item.data)", json.dumps(item.data))
    return render(request, 'index.html', {'biditems':biditems, 'item':item})

def get_post_data(request):
    prices = [ int(x) for x in request.POST.getlist('prices') ]
    base = int(request.POST['base'])
    rate = float(request.POST['rate'])
    checks = []
    for i in range(1,15+1):
        cstr = u"c" + str(i)
        if cstr in request.POST.getlist('checks'):
            checks.append(1)
        else:
            checks.append(0)
    # print("checks", checks)
    data = {'prices':prices, 'base':base, 'rate':rate, 'checks':checks}
    # print("data", data)
    return data

def bidadd(request):
    actual_member = Member.objects.get(id=current_member)
    bid_name = request.POST['bid_name']
    data = get_post_data(request)
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
    return redirect('/'+str(item.id))

import xlwt
def write_row(ws, row_num, row, font_style):
    for col_num in range(len(row)):
        ws.write(row_num, col_num, row[col_num], font_style)

from itertools import combinations
from urllib import parse
def bidexcel(request):
    bid_name = request.POST['bid_name']
    data = get_post_data(request)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s.xls"' % parse.quote(bid_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(bid_name)
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    write_row(ws, row_num, ['번호', '예비가격', '사정율', ], font_style)
    #for col_num in range(len(columns)):
    #    ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for i, price in enumerate(data['prices']):
        row_num += 1
        write_row(ws, row_num, [i+1, price, "%.3f%%" % (price / data['base'] * 100.0)], font_style)
        #for col_num in range(len(row)):
        #    ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    write_row(ws, row_num, ['기초금액', data['base']], font_style)
    row_num += 1
    write_row(ws, row_num, ['투찰율', "%.3f%%" % data['rate']], font_style)

    row_num += 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    write_row(ws, row_num, ['조합번호', '사정율', '투찰금액', ], font_style)

    checks = [i+1 for i, v in enumerate(data['checks']) if v == 1]
    if sum(data['checks']) <= 4:
        comb = []
        for element in list(combinations(list(range(1,15+1)), 4)):
            if set(checks) < set(element):
                comb.append(element)
    else:
        comb = list(combinations(checks, 4))
    font_style = xlwt.XFStyle()
    for element in comb:
        row_num += 1
        price = 0
        for i in element:
            price += int(data['prices'][i-1])
        price /= 4.0
        rate = price / float(data['base']) * 100.0
        rate = "%.3f" % rate
        price *= (float(data['rate']) / 100.0)
        price = "%.0f" % price
        write_row(ws, row_num, [str(element), rate, price], font_style)

    wb.save(response)
    return response


def biddel(request, bid):
    actual_member = Member.objects.get(id=current_member)
    try:
        item = BidItem.objects.get(id=bid)
    except Exception:
        return redirect('/')
    if actual_member == item.member:
        item.delete()
    return redirect('/')
