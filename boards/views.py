from django.shortcuts import render, redirect, get_object_or_404
from .forms import MoodboardForm, MoodboardImageForm
from .models import Moodboard, MoodboardImage


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

    return render(request, 'boards/my_boards.html', {
        'moodboards': moodboards
    })


def moodboard_detail(request, board_id):
    moodboard = get_object_or_404(Moodboard, id=board_id)

    images = moodboard.images.all().order_by('-created_at')

    return render(request, 'boards/moodboard_detail.html', {
        'moodboard': moodboard,
        'images': images,
    })


def add_image(request, board_id):
    moodboard = get_object_or_404(Moodboard, id=board_id)

    if request.method == 'POST':
        form = MoodboardImageForm(request.POST)

        if form.is_valid():
            image = form.save(commit=False)
            image.moodboard = moodboard
            image.save()

            return redirect('moodboard_detail', board_id=moodboard.id)

    else:
        form = MoodboardImageForm()

    return render(request, 'boards/add_image.html', {
        'form': form,
        'moodboard': moodboard
    })
    
def edit_image(request, board_id, image_id):

    moodboard = get_object_or_404(
        Moodboard,
        id=board_id
    )

    image = get_object_or_404(
        MoodboardImage,
        id=image_id,
        moodboard=moodboard
    )

    if request.method == 'POST':

        form = MoodboardImageForm(
            request.POST,
            instance=image
        )

        if form.is_valid():
            form.save()

            return redirect(
                'moodboard_detail',
                board_id=moodboard.id
            )

    else:
        form = MoodboardImageForm(instance=image)

    return render(request, 'boards/edit_image.html', {
        'form': form,
        'moodboard': moodboard,
        'image': image,
    })


def delete_image(request, board_id, image_id):

    moodboard = get_object_or_404(
        Moodboard,
        id=board_id
    )

    image = get_object_or_404(
        MoodboardImage,
        id=image_id,
        moodboard=moodboard
    )

    if request.method == 'POST':
        image.delete()

    return redirect(
        'moodboard_detail',
        board_id=moodboard.id
    )