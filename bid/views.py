from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from models import BidItem, Member
import json

current_member = u'admin'

# Create your views here.
def index(request):
    return HttpResponse('Hello World!')

def bidindex(request):
    biditems = BidItem.objects.filter(member=current_member)
    return render(request, 'index.html', {'biditems':biditems})

def bidindexid(request, bid):
    biditems = BidItem.objects.filter(member=current_member)
    try:
        item = BidItem.objects.get(id=bid)
    except Exception:
        return redirect('/bid')
    print item.data
    print json.dumps(item.data)
    return render(request, 'index.html', {'biditems':biditems, 'bid':item})

def bidadd(request):
    actual_member = Member.objects.get(id=current_member)
    
    bid = request.POST['bid']
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
    print checks
    data = {'prices':prices, 'base':base, 'rate':rate, 'checks':checks}
    print data
    
    BidItem.objects.create(name=bid, data=data, member=actual_member)
    return redirect('/bid/'+bid)

def biddel(request, bid):
    actual_member = Member.objects.get(id=current_member)
    try:
        item = BidItem.objects.get(id=bid)
    except Exception:
        return redirect('/bid')
    if actual_member == item.member:
        item.delete()
    return redirect('/bid')