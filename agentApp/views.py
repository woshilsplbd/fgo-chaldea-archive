from django.shortcuts import render


def chat(request):
    return render(request, 'agentApp/chat.html', {
        'active_menu': 'agent',
    })
