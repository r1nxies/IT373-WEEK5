from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from pages.forms import PostForm, CommentForm
from pages.models import Post, Comment
from django.views.decorators.http import require_http_methods

# Create your views here.
def home(request):
    ctx = {"title": "Home", "features": ["Django", "Templates", "Static files"]}
    return render(request, "home.html", ctx)

def about(request):
    return render(request, "about.html", {"title": "About"})

def hello(request, name):
    return render(request, "hello.html", {"name": name})

def gallery(request):
    # Assume images placed in pages/static/img/
    images = ["img1.jpg", "img2.jpg", "img3.jpg"]
    return render(request, "gallery.html", {"images": images})

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def server_error_view(request):
    return render(request, '500.html', status=500)

def post_list(request):
    # Model.objects.all()
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'title': 'Posts',
    }
    return render(request, 'post_list.html', context)

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                post = form.save(commit=False)

                if hasattr(post, 'author') and (getattr(post, 'author', None) in (None, '') or not post.author_id if hasattr(post, 'author_id') else False):
                    try:
                        if request.user and request.user.is_authenticated:
                            post.author = request.user
                    except Exception:
                        pass

                post.save()
                form.save_m2m() if hasattr(form, 'save_m2m') else None

                messages.success(request, "Post created.")
                return redirect('post_list')
            except Exception as e:
                messages.error(request, "Server error while saving post. See console for details.")
                import traceback, sys
                print("Error saving Post in post_create:", file=sys.stderr)
                traceback.print_exc()
                return render(request, 'post_create.html', {'form': form})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PostForm()

    return render(request, 'post_create.html', {'form': form})

def post_view(request, pk):
    post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment was added.")

            return redirect('post_view', pk=post.pk)
        else:
            messages.error(request, "Please fix the comment errors below.")
    else:
        form = CommentForm()

    return render(request, 'post_view.html', {'post': post, 'comment_form': form})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            return redirect('post_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"Post `{post.title}` was deleted")
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

def csrf_failure_view(request, reason=""):
    return render(request, '403_csrf.html', {'reason': reason}, status=403)