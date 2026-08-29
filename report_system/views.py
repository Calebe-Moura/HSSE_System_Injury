from django.shortcuts import render, redirect


def start(request):
    if request.user.is_authenticated:
        return render(request, 'start/index.html')
    else:
        return redirect('login')

def hub(request):
    if request.user.is_authenticated:
        return render(request, 'injury/hub.html')
    else:
        return redirect('login')