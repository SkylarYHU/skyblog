from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PostList(generic.ListView):
    # 使用查询集从 Post 模型中过滤出已发布的文章（status=1），按 created_on 时间降序排序，并限制为最新的7篇文章
    # queryset 和 model 是 Django 类视图中用于定义数据源的两种方式，但通常只需要选择其中一种
    queryset = Post.objects.filter(status=1).order_by('-created_on')[:7] 
    # 指定渲染的模板为 index.html
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    # 数据来源：指定视图使用 Post model来查询特定文章的数据
    model = Post
    template_name = "post_detail.html"
    
    # 重写此方法以传递评论和评论表单到模板中
    # 接受 **kwargs 参数，以便在调用父类的 get_context_data 方法时传递额外的数据
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前视图的帖子对象，即将展示的文章的实例
        post = self.get_object()
        # 向 context 字典中添加 comments 键，以便在模板中访问评论数据
        # 通过 related_name="comments" 反向访问该帖子的所有评论
        context['comments'] = post.comments.filter(active=True)
        # 向 context 字典中添加 comment_form 键，值为一个新的 CommentForm 表单实例
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # 将评论与当前帖子关联
            new_comment.active = False  # 设置为等待审核
            new_comment.save()

            # 使用 Django 的 messages 提示用户评论已经提交
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')

            # 使用 PRG 模式，重定向到详情页，避免表单重复提交
            return redirect('post_detail', slug=post.slug)
        
        # 如果表单无效，则重新渲染页面，包含现有评论和表单错误信息
        comments = post.comments.filter(active=True)
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, self.template_name, context)
    

class MoreArticles(generic.ListView):
    model = Post
    template_name = 'more_articles.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(self.get_queryset(), self.paginate_by)
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            posts = paginator.page(paginator.num_pages)
        
        context['posts'] = posts
        context['page_obj'] = posts  # Ensure `page_obj` is available for pagination controls in template
        return context
    
