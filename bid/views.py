from django.shortcuts import render
from django.http.response import HttpResponse
from models import BidItem


# Create your views here.
def index(request):
    return HttpResponse('Hello World!')

def bidindex(request):
    biditems = BidItem.objects.filter(member=u'admin')
    return render(request, 'index.html', biditems)