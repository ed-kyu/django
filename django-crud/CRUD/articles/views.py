from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')


def new(request):
    pass


def create(request):
    pass


def detail(request, pk):
    pass


def edit(request, pk):
    pass


def update(request, pk):
    pass


def delete(request, pk):
    pass