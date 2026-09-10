from django.shortcuts import render


def download(request):
    return render(request, 'download.html', {
        'active_menu': 'service',
        'sub_menu': 'download',
    })


def platform(request):
    return render(request, 'platform.html', {
        'active_menu': 'service',
        'sub_menu': 'platform',
    })
