from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from Hostmanager.models import Hosts, UserInfo, Group
import json


def login(request):
    return render(request, 'login.html')


# host_list = [{
#     'id': 1,
#     'hostname': 'nginx',
#     'port': 22,
#     'ip': '192.168.1.1'
# },
#     {
#         'id': 2,
#         'hostname': 'python',
#         'port': 22,
#         'ip': '192.168.1.2'
#     }, ]


def hosts(request):
    host_list = Hosts.objects.all()

    return render(request, 'hosts.html', {'host_list': host_list})


def index(request):
    host_list = Hosts.objects.all()
    return render(request, 'hosts.html', {'host_list': host_list})


def addhost(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        tmp = {
            'hostname': hostname,
            'port': port,
            'ip': ip,
        }
        Hosts.objects.create(**tmp)
    return redirect('/hosts/')


def delhost(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        nid = int(json.loads(nid))
        data = Hosts.objects.filter(nid=nid).delete()
        ret = {'status': True, 'error': None, 'data': None}
        ret['status'] = True
        ret['data'] = 'OK'
        return HttpResponse(json.dumps(ret))


def modhost(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        tmp = {
            'hostname': hostname,
            'port': port,
            'ip': ip
        }
        print(ip, hostname, port, nid)
        Hosts.objects.filter(nid=nid).update(**tmp)
    return redirect('/hosts/')


def managerGroup(request):
    group = Group.objects.all()

    return render(request, 'group.html', {'host_list': group})


def addGroup(request):
    pass


def modGroup(request):
    pass


def delGroup(request):
    pass
