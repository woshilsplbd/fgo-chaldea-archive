# 迦勒底档案馆 — FGO 同人资料站

## 项目简介

"迦勒底档案馆"是一个基于 Django 框架构建的 Fate/Grand Order（FGO）同人资料网站。项目以 FGO 游戏世界观为背景，将原企业门户网站（恒达科技）全面改造为具有紫色 FGO 风格的主题站，涵盖英灵数据库、活动情报、攻略资料、灵基研究室和御主留言等功能模块。

项目部署于 Railway 云平台，适配移动端与桌面端，并集成了 Atlas Academy API 实现英灵数据的实时查询。

## 功能模块介绍

| 模块 | 对应 App | 功能说明 |
|------|----------|----------|
| 首页 | homeApp | 站点入口，展示导航入口卡片与最新动态 |
| 关于迦勒底 | aboutApp | FGO 世界观介绍、迦勒底机构与人员介绍 |
| 活动情报 | newsApp | 三类活动信息展示——主线剧情、限时活动、召唤公告，支持分页、搜索与详情查看 |
| 英灵资料 | productsApp | 通过 Atlas Academy API 获取真实英灵数据，支持职阶筛选、名称搜索、详情查看（大立绘、宝具、技能） |
| 攻略资料 | serviceApp | 新手入门指南、配队与周回攻略 |
| 灵基研究室 | scienceApp | FGO 战斗系统科普——常规/特殊职阶体系、宝具类型、指令卡系统等 |
| 御主留言 | contactApp | 留言板（提交后保存到数据库，Django admin 可查看）、档案整理加入申请 |
| 英灵 API | productsApp | `/api/servants/` JSON 接口，支持分页、职阶筛选与名称搜索，供前端 Ajax 异步加载 |

## 技术栈

- **后端框架**：Django 2.2.4（Python）
- **数据库**：SQLite
- **前端**：Bootstrap 3 + jQuery
- **Web 服务器**：Gunicorn
- **静态文件服务**：WhiteNoise
- **部署平台**：Railway（`web-production-63d3d.up.railway.app`）
- **外部 API**：Atlas Academy API（FGO 英灵数据）
- **第三方依赖**：
  - `requests` — 调用 Atlas Academy API
  - `pyquery` — 解析新闻内容的 HTML 段落
  - `django-haystack` + `Whoosh` + `jieba` — 全文搜索与中文分词
  - `django-widget-tweaks` — 表单样式扩展
  - `docxtpl` + `python-docx` — 简历审核通过时自动生成 Word 文档
  - `whitenoise` — 生产环境静态文件托管

## 项目结构说明

```
hengDaProject-08/
│
├── manage.py                   # Django 管理脚本
├── requirements.txt            # Python 依赖清单
├── runtime.txt                 # Python 版本（3.8.16）
├── Procfile                    # Railway 部署启动命令
├── db.sqlite3                  # 本地开发数据库文件，已通过 .gitignore 忽略，不上传仓库
│
├── hengDaProject/              # 项目配置目录
│   ├── settings.py             # 全局配置（数据库、中间件、应用注册、静态文件等）
│   ├── urls.py                 # 根路由配置
│   └── wsgi.py                 # WSGI 入口
│
├── homeApp/                    # 首页应用
│   ├── views.py                # home()：渲染首页
│   └── templates/home.html     # 首页模板
│
├── aboutApp/                   # 关于迦勒底应用
│   ├── models.py               # Award 模型（荣誉记录）
│   ├── views.py                # survey()、honor()
│   ├── urls.py                 # /survey/、/honor/
│   └── templates/              # survey.html、honor.html
│
├── newsApp/                    # 活动情报应用
│   ├── models.py               # MyNew 模型（标题、内容、类型、发布时间、浏览量）
│   ├── views.py                # news()、newDetail()、search()
│   ├── urls.py                 # /news/<type>/、/newDetail/<id>/、/search/
│   ├── admin.py                # MyNew 后台注册
│   ├── search_indexes.py       # Haystack 搜索索引配置
│   ├── whoosh_backend.py       # 自定义 Whoosh 中文分词后端
│   └── templates/              # newList.html、newDetail.html、searchList.html
│
├── productsApp/                # 英灵资料应用（核心功能）
│   ├── models.py               # Product、ProductImg 模型
│   ├── views.py                # Atlas Academy API 调用、缓存、数据规范化
│   │                           # products()、servant_detail()、servants_api() 等
│   ├── urls.py                 # /products/<name>/、/productDetail/<id>/
│   ├── admin.py                # Product 后台管理（含图片内联）
│   └── templates/              # productList.html、productDetail.html
│
├── serviceApp/                 # 攻略资料应用
│   ├── views.py                # download()、platform()
│   ├── urls.py                 # /download/、/platform/
│   └── templates/              # download.html、platform.html
│
├── scienceApp/                 # 灵基研究室应用
│   ├── views.py                # science()
│   ├── urls.py                 # /science/
│   └── templates/science.html  # 职阶体系科普页面
│
├── contactApp/                 # 御主留言应用
│   ├── models.py               # Ad（留言）、Resume（简历申请）
│   ├── views.py                # contact()（带 POST 保存逻辑）、recruit()
│   ├── urls.py                 # /contact/、/recruit/
│   ├── admin.py                # Ad / Resume 后台注册
│   ├── forms.py                # Resume ModelForm
│   └── templates/              # contact.html、recruit.html、success.html
│
├── templates/                  # 项目级模板
│   ├── base.html               # 全局布局（导航栏、页脚、BB 迪拜语音向导组件）
│   └── search/                 # Haystack 搜索页面与索引模板
│
├── static/                     # 静态资源
│   ├── css/                    # Bootstrap、style.css、app 专用样式
│   ├── js/                     # jQuery、Bootstrap、日期选择器
│   └── fonts/                  # Glyphicons 字体
│
└── DjangoUeditor/              # 第三方富文本编辑器（UEditor）
```

## 核心功能实现思路

### 1. 英灵资料 — 调用外部 API 获取数据

通过 Atlas Academy API 实时获取 FGO 英灵数据，不使用本地数据库存储英灵信息。`productsApp/views.py` 中的实现：

```
products(request, 'saber')
    → _requested_classes('saber')        # 解析职阶别名
    → _fetch_atlas_servants_by_class()   # 带 600 秒内存缓存
        → _request_atlas()               # GET https://api.atlasacademy.io/nice/JP/servant/search
    → _normalize_servant()               # 提取 id、名称、职阶、星级、小头像
    → template: productList.html

servant_detail(request, 1)
    → _fetch_atlas_servant_detail(1)     # 带缓存
        → _request_atlas_detail()        # GET https://api.atlasacademy.io/nice/JP/servant/1
    → _normalize_servant_detail()        # 提取大立绘、宝具、技能、简介
    → template: productDetail.html

servants_api(request)                    # JSON 接口
    → 支持 className、search、page、limit 参数
    → 前端通过 Ajax 实现异步筛选与分页
```

通过内存字典 `_servant_cache` 实现 API 响应缓存，缓存有效期 600 秒，避免频繁请求导致限流。

### 2. 英灵列表页面 — 异步加载与筛选

`productList.html` 使用前端 JavaScript 实现：
- 页面加载时调用 `/api/servants/?className=all` 获取全部英灵
- 点击职阶按钮（Saber / Archer / Extra 等）重新请求对应类别的数据
- 搜索框输入时实时过滤（`keyup` 事件 + debounce）
- 分页控件切换页码
- 所有数据渲染通过 DOM 操作完成，不刷新页面

### 3. 留言板 — 表单提交与数据库保存

`contactApp/views.py` 中的 `contact()` 视图：
- GET 请求：渲染留言表单
- POST 请求：读取 `nickname` 和 `message` 字段，调用 `Ad.objects.create()` 保存到数据库
- 保存成功后通过 HTTP 重定向（PRG 模式）跳转到 `?saved=1`，展示成功提示
- 异常时返回 500 并显示错误信息

Django admin (`contactApp/admin.py`) 注册了 `Ad` 模型，管理员可在 `/admin/contactApp/ad/` 查看所有留言。

### 4. 活动情报 — 分页列表与搜索

`newsApp/views.py`：
- `news()` 根据 URL 参数 `newName`（company / industry / notice）映射到中文分类名（主线剧情 / 限时活动 / 召唤公告）
- 使用 `MyNew.objects.filter(newType=...)` 从数据库获取记录
- 自定义分页逻辑（显示前 2 页和后 2 页页码）
- `newDetail()` 记录浏览量自增
- `search()` 通过 `title__icontains` 实现模糊搜索

同时配置了 Haystack + Whoosh + jieba 中文分词，支持更精准的全文搜索（路由 `/search/`）。

### 5. BB 迪拜语音向导（前端交互）

`templates/base.html` 中的独立前端组件：
- 固定定位在页面右下角，CSS `position: fixed`，拖拽时更新 `right` / `bottom` 定位
- 鼠标 / 触屏拖拽：`mousedown` → `mousemove` → `mouseup`
- 点击切换"语音朗读模式"：使用 Web Speech API（`SpeechSynthesisUtterance`）朗读页面上的文本
- 拖拽与点击通过 `isDragging` 标志区分

### 6. 简历审核与文档生成

`contactApp/models.py` 中的 `Resume` 模型注册了 Django Signal：
- `post_save` 监听状态变化
- 当状态从"未审"变为"通过"时，使用 `docxtpl` 从 `.docx` 模板文件生成录用 Word 文档
- 当状态变为"未通过"时，调用 QQ 邮箱 SMTP 发送拒绝邮件（邮箱凭据已配置但功能因网络限制未启用）

## 开发过程中遇到的问题及解决方案

### 1. Python 版本兼容性问题

**问题**：本地系统默认 Python 3.14 与 Django 2.2.4 不兼容（`distutils` 模块在 Python 3.12+ 被移除），使用 `python manage.py` 运行项目报错。

**解决方案**：在 `runtime.txt` 中锁定 Python 3.8.16，部署时 Railway 使用指定版本运行；本地开发通过直接操作 SQLite 数据库的方式绕过了 Django 脚本执行限制。

### 2. 静态文件 404（部署环境）

**问题**：项目部署到 Railway 后，二维码等静态图片返回 404。原因是 `STATICFILES_STORAGE` 使用了 `CompressedManifestStaticFilesStorage`，对带特殊字符的文件名（如原 `https_web-production-63d3d_up_railway_app_.png`）处理异常。

**解决方案**：将图片重命名为简单文件名 `qr.png`，同时将存储后端切换为 `CompressedStaticFilesStorage`，避免 manifest 文件名的哈希映射问题。

### 3. BB 迪拜图片被父容器裁切

**问题**：大屏下 BB 迪拜角色贴纸只显示下半身，头部被父容器裁切。

**解决方案**：将图片的 `position` 从 `fixed` 改为 `absolute`，外层容器设置 `overflow: visible`，使用 `object-fit: contain` 确保图片完整显示，移动端通过媒体查询隐藏。

### 4. 企业数据替换为 FGO 内容

**问题**：原恒达科技网站的数据库中存在大量企业新闻、招聘广告等无关数据，页面显示内容不符合 FGO 主题。

**解决方案**：直接操作 SQLite 数据库——删除 `newsApp_mynew` 表中的 11 条企业新闻记录，替换为 11 条 FGO 活动数据（主线剧情 3 条、限时活动 4 条、召唤公告 4 条）；同时删除 `contactApp_ad` 表中的企业招聘广告，替换为 6 条 FGO 风格留言示例。模型字段的 `verbose_name` 也同步修改以匹配新内容（如"招聘岗位"→"用户名"）。

### 5. 留言表单提交后数据未持久化

**问题**：前台表单使用 `action="javascript:void(0)"`，JavaScript 只做了前端显示/隐藏切换，完全没有向服务器发送 POST 请求，数据从未离开浏览器。

**解决方案**：将表单 `action` 改为 Django URL 模板标签 `{% url 'contactApp:contact' %}`；在 `views.py` 中增加 POST 处理逻辑——读取表单字段、调用 `Ad.objects.create()` 保存到数据库、重定向到成功状态页面，遵循 PRG（Post-Redirect-Get）模式。

### 6. 导航栏默认竖排布局

**问题**：Bootstrap 导航栏下拉菜单显示为竖排但主菜单项布局不符合移动端适配要求。

**解决方案**：移除宽度 100% 限制，使用 Flexbox 实现横向菜单，添加 `navbar-toggle` 三横线按钮实现移动端折叠，所有导航链接替换为 FGO 主题名称。

### 7. 部署环境网络限制

**问题**：开发环境的网络连接不稳定，无法通过 `git push` 将代码推送至 GitHub，导致 Railway 无法自动部署最新代码。

**解决方案**：手动记录需要部署的变更步骤，告知用户在可访问 GitHub 的环境中执行 `git push` 触发部署。

## 项目总结与收获

通过本项目的开发，完整实践了一个 Django Web 项目的全生命周期：从项目初始化、应用拆分、模板渲染、数据库建模、第三方 API 集成，到云平台部署与线上调试。

**技术方面的收获**：

1. **Django MTV 架构**：深入理解了 Model-Template-View 的职责划分，实践了多应用项目结构设计
2. **外部 API 集成**：实现了对第三方 API（Atlas Academy）的 HTTP 调用、数据规范化、内存缓存与 JSON 接口封装
3. **前后端交互**：通过 Django JSON View + jQuery Ajax 实现了异步数据加载与前端渲染
4. **全文搜索**：在 Django 中集成了 Haystack + Whoosh + jieba 中文分词搜索框架
5. **数据库直接操作**：在无法运行 Django manage.py 的环境中，通过 SQLite 命令行直接修改数据，加深了对 ORM 底层 SQL 的理解
6. **部署运维**：使用 Gunicorn + WhiteNoise + Railway 完成生产环境部署，处理了静态文件收集、环境变量配置、Host 白名单等实际问题
7. **前端交互**：实现了可拖拽悬浮组件、Web Speech API 语音朗读、响应式布局等客户端功能

**项目管理方面的收获**：

项目从一个完整的旧企业网站出发进行主题改造，需要在不破坏已有路由结构和数据库表结构的前提下完成全部界面的替换。这对代码理解和改造规划能力提出了较高要求——必须准确识别哪些代码需要保留、哪些需要替换、哪些需要新增，同时保证导航、页脚等公共组件的一致性和可用性。
