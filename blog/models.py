from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
  # 定义status字段的选项元组，这些选择将在status字段中使用来表示帖子可见性
  STATUS = (
    (0, "Draft"),
    (1, "Publish"),
  )

  # 一个可选的图片字段，允许上传与帖子相关的图片。upload_to='posts/' 指定了图片的上传目录
  image = models.ImageField(upload_to='posts/', blank=True, null=True)
  # enforces that each post must have a unique title
  title = models.CharField(max_length=100, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  # 如果删除用户，则与该用户关联的所有帖子也将被删除
  # 允许使用user.blog_posts.all()从User模型进行反向查找以获取用户的所有帖子
  # 例如，如果我们有一个用户对象 user，可以通过 user.blog_posts.all() 来获取该用户创建的所有帖子
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
  # 每当帖子更新时，都会自动将此字段更新为当前时间戳
  updated_on = models.DateTimeField(auto_now=True)
  content = models.TextField()
  # 自动将此字段设置为首次创建帖子时的时间戳，之后不会更改
  created_on = models.DateTimeField(auto_now_add=True)
  # 选择仅限于上面定义的STATUS元组
  status = models.IntegerField(
    choices=STATUS, 
    default=0, 
    verbose_name="Post Status", 
    help_text="Set the status of the post to draft or publish."
    )

# Meta 类用于在 Django 模型中定义一些元数据，控制模型在数据库中的表现方式，但不直接创建数据库字段
  class Meta:
    # 按created_on降序排列查询结果（最新的帖子首先出现）。
    ordering = ['-created_on']

  def __str__(self):
    # 当打印或显示 Post 对象时，__str__ 方法会返回该对象的 title 属性
    # print(post) 会输出 post.title 的值
    return self.title
  
  # def get_absolute_url(self):
  #   # 使用 reverse 函数生成 post_detail 视图的 URL，并将 self.slug 作为参数传入
  #   # reverse 函数是 Django 中的一个工具函数，用于根据视图的名称（URL 的名称）生成 URL。它接收视图的名称及其对应的参数，然后返回该视图的完整 URL
  #   # 当在模板中调用 {{ post.get_absolute_url }} 时，Django 会生成基于 post_detail 视图的完整 URL，而无需手动拼接字符串
  #    return reverse('post_detail', args=[self.slug])
  
class Comment(models.Model):
  # 与 Post 模型建立了多对一的关系
  # related_name 属性允许我们将用于相关对象与此对象的关系的属性命名，并使用 post.comments.all（） 检索帖子的所有评论
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  name = models.CharField(max_length=80)
  email = models.EmailField()
  body = models.TextField()
  created_on = models.DateTimeField(auto_now_add=True)
  # 该字段设置为 False 以防止垃圾评论，手动允许发布的所有评论
  active = models.BooleanField(default=False)

  # 管理数据在页面上的呈现方式
  class Meta:
    ordering = ['created_on']
  
  def __str__(self):
    return f'Comment {self.body[:30]} by {self.name}'