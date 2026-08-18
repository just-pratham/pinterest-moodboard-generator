from django.shortcuts import render, redirect
from .forms import MoodboardForm
from .models import Moodboard


def home(request):
    return render(request, 'boards/home.html')


def create_moodboard(request):

    if request.method == 'POST':
        form = MoodboardForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = MoodboardForm()

    return render(request, 'boards/create_moodboard.html', {
        'form': form
    })
    
def my_boards(request):
    moodboards = Moodboard.objects.all().order_by('-updated_at')
    
    return render(request, 'boards/my_boards.html',{
        'moodboards': moodboards
    })
    
def moodboard_detail(request, board_id):
    moodboard = Moodboard.objects.get(id=board_id)

    return render(request, 'boards/moodboard_detail.html', {
        'moodboard': moodboard
    })
    