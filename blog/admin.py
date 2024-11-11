from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


# 装饰器的方式更加简洁，并且将注册和配置逻辑放在了一起，admin.site.register也可以
# 将Post模型注册到 Django 的管理界面，并自定义它在管理面板中的显示和管理方式 
@admin.register(Post)
# 创建 PostAdmin 类，继承 SummernoteModelAdmin，允许使用 Summernote 富文本编辑器来编辑 Post 模型的 content 字段
class PostAdmin(SummernoteModelAdmin):
    # 指定在管理列表视图中显示的字段
    list_display = ('title', 'slug', 'status', 'created_on','get_author_fullname')
    # 在管理界面的侧边栏提供 status 字段的过滤选项
    list_filter = ('status',)
    # 启用搜索框，允许管理员按 title, content, first_name, last_name字段内容搜索帖子
    # 由于 author 字段是一个外键，需使用双下划线 __ 访问相关字段
    search_fields = ['title', 'content', 'author__first_name', 'author__last_name']
    # 自动填充 slug 字段的值为 title 字段的内容，生成更加规范的 URL 片段
    prepopulated_fields = {'slug': ('title',)}
    # 使用 Summernote 富文本编辑器编辑 content 字段
    summernote_fields = ('content',)

    # 自定义方法，用于获取作者的全名。如果作者只有用户名且无 first_name 和 last_name，则显示用户名
    def get_author_fullname(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}" if obj.author.first_name or obj.author.last_name else obj.author.username
    get_author_fullname.short_description = 'Author Fullname'

# 将 Comment 模型注册到 Django 管理界面
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_preview', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body', 'post__title')
    # 在管理界面的评论列表中提供自定义操作 approve_comments，可以批量审批评论
    actions = ['approve_comments']
    # 设置管理界面每页显示的评论数量为 20 条
    list_per_page = 20

    # 用于给自定义的管理操作 (admin action) 添加描述，使其在 Django 管理界面的操作下拉菜单中显示为更具可读性的文字
    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        # 批量更新查询集 (queryset) 的方法，将 queryset 中的所有对象的 active 字段设置为 True，并将修改直接保存到数据库中，无需逐个调用 save() 方法
        queryset.update(active=True)

    # 用于在 Django 管理界面的 CommentAdmin 列表视图中显示评论内容的简短预览
    # obj: 是 Comment 模型的一个实例，传入的具体对象为某条评论
    def body_preview(self, obj):
        # 三元表达式，用于检查 obj.body 的长度
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    # 用于设置 body_preview 方法在管理界面中显示的列标题
    body_preview.short_description = 'Body Preview'


