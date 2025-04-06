from django.shortcuts import render, get_object_or_404, redirect, redirect
from .models import Wish
from .forms import WishForm, CommentForm
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, "app1/home.html")


def add_wish(request):
    if request.method == "POST":
        form = WishForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.owner = request.user
            wish.save()
            messages.success(request, "Your wish has been added!")
            return redirect("add_wish")
    else:
        form = WishForm()
    
    return render(request, "app1/add_wish.html", {"form": form})

from django.contrib.contenttypes.models import ContentType

def wish_list(request):
    wishes = Wish.objects.filter(owner=request.user)
    comments = {wish.id: wish.comments.all() for wish in wishes}  # Fetch comments for each wish

    if request.method == 'POST':
        wish_id = request.POST.get('wish_id')
        wish = Wish.objects.get(id=wish_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.wish = wish  # Associate the comment with the specific wish

            # Set the GenericForeignKey fields
            comment.content_type = ContentType.objects.get_for_model(Wish)
            comment.object_id = wish.id

            comment.user = request.user
            
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('wish_list')
    else:
        form = CommentForm()

    return render(request, 'app1/wish_list.html', {'wishes': wishes, 'form': form, 'comments': comments})


# views.py
def public_wishes(request):
    # Fetch only public wishes
    wishes = Wish.objects.filter(is_public=True)

    # Fetch comments for each wish
    comments = {wish.id: wish.comments.all() for wish in wishes}  

    if request.method == 'POST':
        wish_id = request.POST.get('wish_id')
        wish = Wish.objects.get(id=wish_id)

        # Initialize form with POST data
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.wish = wish  # Associate the comment with the specific wish

            # Set the GenericForeignKey fields
            comment.content_type = ContentType.objects.get_for_model(Wish)
            comment.object_id = wish.id

            # Assign the logged-in user to the comment
            comment.user = request.user
            
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('public_wish_list')  # Redirect to the same page after adding the comment

    else:
        form = CommentForm()  # Initialize an empty form when not posting

    return render(request, 'app1/public_wish.html', {'wishes': wishes, 'form': form, 'comments': comments})


def edit_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    
    if wish.owner != request.user:
        messages.error(request, "You can only edit your own wishes.")
        return redirect('wish_list')

    if request.method == 'POST':
        form = WishForm(request.POST, instance=wish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wish updated successfully!')
            return redirect('wish_list')
    else:
        form = WishForm(instance=wish)

    return render(request, 'app1/edit_wish.html', {'form': form, 'wish': wish})

# Delete a wish
def delete_wish(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)

    if wish.owner != request.user:
        messages.error(request, "You can only delete your own wishes.")
        return redirect('wish_list')

    if request.method == 'POST':
        wish.delete()
        messages.success(request, 'Wish deleted successfully!')
        return redirect('wish_list')

    return render(request, 'app1/delete_wish.html', {'wish': wish})

def add_comment(request, wish_id):
    wish = get_object_or_404(Wish, id=wish_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, wish=wish)
        if form.is_valid():
            form.save()
            messages.success(request, "Your comment has been added successfully!")
            return redirect('wish_detail', wish_id=wish.id)  
    else:
        form = CommentForm(wish=wish)
    
    return render(request, 'add_comment.html', {'form': form, 'wish': wish})