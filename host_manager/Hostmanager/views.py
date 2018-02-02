from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


def login(request):
    pass


host_list = [{
    'id': 1,
    'hostname': 'nginx',
    'port': 22,
    'ip': '192.168.1.1'
},
    {
        'id': 2,
        'hostname': 'python',
        'port': 22,
        'ip': '192.168.1.2'
    }, ]


def hosts(request):
    return render(request, 'hosts.html', {'host_list': host_list})


def index(request):
    return render(request, 'index.html', {'host_list': '11111'})


def addhost(request):
    if request.method == "POST":
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        tmp = {
            'id': 3,
            'hostname': hostname,
            'port': port,
            'ip': ip
        }
        host_list.append(tmp)
        print(ip, hostname, port)

    return render(request, 'hosts.html', {'host_list': host_list})


def delhost(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        # host_list.append(tmp)
        print(ip, hostname, port,nid)

    return redirect('/hosts/')


def modhost(request):
    if request.method == "POST":
        nid = request.POST.get('nid')
        ip = request.POST.get('ip')
        hostname = request.POST.get('hostname')
        port = request.POST.get('port')
        # host_list.append(tmp)
        print(ip, hostname, port,nid)


    return redirect('/hosts/')
