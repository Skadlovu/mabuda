from django.shortcuts import render

def assist(request):
    template='assist.html'
    return render(request,template)


