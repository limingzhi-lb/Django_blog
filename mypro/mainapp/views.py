from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Tag, Category, Me, Message
from .forms import CommentForm
from markdown import markdown
from django.db.models import Q

# def index(request):
#     return render(request, 'mainapp/index.html')


class IndexView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'mainapp/index.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num = {"num": 0, }
        context.update(num)
        print(context.get('num'))
        return context


class PostDetailView(DetailView):
    template_name = 'mainapp/single.html'
    model = Post
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        post.body = markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_list = self.object.comment_set.all()
        form = CommentForm()
        context.update({'comment_list': comment_list, 'form': form, })
        return context


def comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect(post)


class TagPosts(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


class CategoryPosts(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)
    # pass


def about(request):
    me = Me.objects.all()
    if me:
        me = me[0].text
    else:
        me = False
    return render(request, 'mainapp/about.html', {'me': me})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        msg = Message()
        msg.name = name
        msg.email = email
        msg.text = message
        msg.save()
        request.session['send_email'] = True
        return redirect("mainapp:contact")
    else:
        flag = request.session.get('send_email')
        request.session['send_email'] = False
        return render(request, 'mainapp/contact.html', {'flag': flag})


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'mainapp/index.html',
                      {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) |
                                    Q(body__icontains=q))
    return render(request, 'mainapp/index.html',
                  {'error_msg': error_msg,
                  'post_list': post_list})
