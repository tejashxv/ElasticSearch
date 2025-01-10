from django.shortcuts import render

# Create your views here.
def shop(request):
    print("home page")
    return render(request, 'home.html')