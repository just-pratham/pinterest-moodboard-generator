from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Moodboard, MoodboardImage
from .forms import MoodboardForm, MoodboardImageForm
from .services import (
    get_recommended_images,
    track_unsplash_download,
)

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
    
def edit_moodboard(request, board_id):
    moodboard = get_object_or_404(Moodboard, id=board_id) 
    
    if request.method=='POST':
        form=MoodboardForm(
            request.POST,
            instance=moodboard
        )   
        
    if form.is_valid():
        form.save()
        
        messages.success(
            request,
            "Moodboard updated successfully."
        )  
        
        return redirect(
            'moodboard_detail',
            board_id=moodboard.id
        )  
        
    else:
        form=MoodboardForm(instance=moodboard)
        
    return render(request, 'boards/edit_moodboard.html', {
        'form': form,
        'moodboard': moodboard,
    })        


def my_boards(request):
    moodboards = Moodboard.objects.all().order_by('-updated_at')

    return render(request, 'boards/my_boards.html', {
        'moodboards': moodboards
    })


def moodboard_detail(request, board_id):
    moodboard = get_object_or_404(
        Moodboard,
        id=board_id
    )

    images = moodboard.images.all().order_by('-created_at')

    # -------------------------------
    # BUILD RECOMMENDATION QUERY
    # -------------------------------

    query_parts = [moodboard.title]

    if moodboard.description:
        query_parts.append(moodboard.description)

    captions = (
        images
        .exclude(caption='')
        .values_list('caption', flat=True)[:5]
    )

    for caption in captions:
        if caption:
            query_parts.append(caption)

    search_query = " ".join(query_parts)


    # -------------------------------
    # REFRESH RECOMMENDATIONS
    # -------------------------------

    try:
        refresh_number = int(
            request.GET.get('refresh', 0)
        )
    except ValueError:
        refresh_number = 0

    # Prevent negative page numbers
    refresh_number = max(refresh_number, 0)

    unsplash_page = refresh_number + 1


    # -------------------------------
    # FETCH RECOMMENDATIONS
    # -------------------------------

    recommendations = get_recommended_images(
        search_query,
        per_page=20,
        page=unsplash_page
    )


    # -------------------------------
    # REMOVE ALREADY-ADDED IMAGES
    # -------------------------------

    existing_unsplash_ids = set(
        images
        .exclude(unsplash_id__isnull=True)
        .exclude(unsplash_id='')
        .values_list('unsplash_id', flat=True)
    )

    recommendations = [
        photo
        for photo in recommendations
        if photo['id'] not in existing_unsplash_ids
    ]


    # Display maximum 12 recommendations
    recommendations = recommendations[:12]


    # Used by the Refresh button
    next_refresh = refresh_number + 1


    return render(request, 'boards/moodboard_detail.html', {
        'moodboard': moodboard,
        'images': images,
        'recommendations': recommendations,
        'next_refresh': next_refresh,
    })

def add_image(request, board_id):
    moodboard = get_object_or_404(Moodboard, id=board_id)

    if request.method == 'POST':
        form = MoodboardImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.moodboard = moodboard
            image.save()

            return redirect(
                'moodboard_detail',
                board_id=moodboard.id
            )

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
    
def add_recommended_image(request, board_id):
    moodboard = get_object_or_404(Moodboard, id=board_id)

    if request.method == 'POST':
        unsplash_id = request.POST.get('unsplash_id')
        image_url = request.POST.get('image_url')
        caption = request.POST.get('caption', '')
        download_location = request.POST.get('download_location')

        if image_url and unsplash_id:

            already_exists = MoodboardImage.objects.filter(
                moodboard=moodboard,
                unsplash_id=unsplash_id
            ).exists()

            if not already_exists:
                MoodboardImage.objects.create(
                    moodboard=moodboard,
                    image_url=image_url,
                    caption=caption,
                    unsplash_id=unsplash_id
                )
                
                messages.success(
                    request,
                    "Image added to your moodboard."
            )

                track_unsplash_download(download_location)

    return redirect(
        'moodboard_detail',
        board_id=moodboard.id
    )