# FGO Chaldea Archive

## Legacy Django Web Project

这是一个 FGO 主题的传统 Django Web 项目，包含内容展示、SQLite 数据、Django Admin、站内搜索和外部从者数据接入。它构成了原始的 Web / data foundation，后来进一步演进为独立的 [fgo-chaldea-agent](https://github.com/woshilsplbd/fgo-chaldea-agent) 项目。

## 核心功能

- FGO 内容、新闻与资料页面展示。
- 产品与档案式结构化内容管理。
- 访客留言通过 Django ORM 持久化到 SQLite。
- 基于 Django Admin 的内容管理：新闻、产品、奖项、留言与简历数据。
- Django Haystack + custom Whoosh backend 站内搜索。
- 通过 Atlas Academy API 获取从者数据。
- 使用 Django Media 管理奖项、简历和产品图片。

## 技术栈

| 方向 | 技术 |
| --- | --- |
| Backend | Python / Django 2.2 |
| Database | SQLite / Django ORM |
| Search | Django Haystack / Whoosh |
| External data | Atlas Academy API |
| Frontend | HTML / CSS / JavaScript |
| Engineering / deployment | Git / Render / Gunicorn / WhiteNoise |

## 系统结构

```text
Browser
  │
  ▼
Django Views / Templates
  ├─ Django ORM ─────→ SQLite
  ├─ Django Admin
  ├─ Haystack ───────→ Whoosh Index
  ├─ Media Files
  └─ Atlas Academy API
```

页面请求由 Django Views 和 Templates 负责，站点内容由 ORM 读写 SQLite；Admin 提供后台管理入口，Haystack 将新闻内容连接到 Whoosh 索引，媒体文件则通过 Django 的 media 配置提供服务。

## 数据库设计

| Model | 用途 | Relationship / role |
| --- | --- | --- |
| `Award` | 公司奖项与荣誉 | 包含可选照片 |
| `Ad` | 访客留言 | 留言标题、内容、联系方式与发布时间 |
| `Resume` | 简历 / 应聘数据 | 包含申请信息、状态与个人照片 |
| `MyNew` | 新闻内容 | 新闻类型、正文、发布时间与浏览量 |
| `Product` | 产品 / 结构化档案 | 通过一对多关系关联产品图片 |
| `ProductImg` | 产品图片 | `ForeignKey` → `Product` |

当前本地 SQLite 是开发 / 演示数据集，而不是规模或性能指标。已审计的当前行数为：`Award` 6、`Ad` 7、`Resume` 1、`MyNew` 11、`Product` 28、`ProductImg` 47；数据库完整性检查通过。

## 留言系统

```text
Browser form
      ↓
contactApp:contact
      ↓
contactApp.views.contact
      ↓
Ad.objects.create(...)
      ↓
SQLite: contactApp_ad
      ↓
Django Admin review
```

有效的访客留言会通过 Django ORM 写入 SQLite，CSRF protection 已启用，管理员可以在 Django Admin 中查看后续留言记录。表单处理保持在传统 Django View / Form / Model 边界内，不将其描述为独立的生产级消息平台。

## Django Admin

项目使用基本的 Django Admin-backed content management：

- News：管理新闻内容；
- Products：管理产品及产品图片 inline；
- Awards：管理奖项与荣誉照片；
- Visitor messages：查看访客留言；
- Resume / application data：查看简历与申请状态。

Admin 配置以 Django 原生能力和少量 `ModelAdmin` 定制为主，不将其包装为 fully customized CMS 或高级后台产品。

## 搜索架构

新闻搜索同时体现了索引搜索与 ORM 查询两种路径：

```text
Database news content
        ↓
newsApp.MyNewIndex
        ↓
Django Haystack
        ↓
custom Whoosh backend
        ↓
whoosh_index/
        ↓
Search results
```

根路径 `/search/` 使用 Haystack + Whoosh；`newsApp` 下的独立搜索路径则直接对 `MyNew.title` 执行 Django ORM 的 `icontains` 过滤。Whoosh 索引由数据库新闻记录派生。

## Atlas Academy API

从者数据通过 Atlas Academy API 获取，而不是复制为本地 SQLite business models。`productsApp` 对 Atlas Academy 的搜索和详情请求进行了规范化，并使用进程内约 600 秒的 bounded cache，减少短时间内的重复请求。

这形成了清晰的数据边界：本地新闻、产品、留言等站点内容使用 Django ORM；外部 FGO servant data 则由 Atlas Academy 作为数据源。

## Media / content

Django Media 主要用于：

- `Award.photo`：奖项与荣誉照片；
- `Resume.photo`：简历个人照片；
- `ProductImg.photo`：产品图片。

当前数据库中引用的媒体文件已完成存在性核对，未发现缺失引用文件。

## 项目结构

```text
hengDaProject/       Django settings、URL routing 与 WSGI
aboutApp/            关于、奖项与荣誉
contactApp/          留言与简历
homeApp/             首页
newsApp/             新闻、搜索索引与 Whoosh backend
productsApp/         产品、产品图片与 Atlas servant data
scienceApp/          科研 / 静态内容页面
serviceApp/          服务 / 静态内容页面
agentApp/            原始站点中的兼容性路由模块
templates/           共享模板
static/              CSS、JavaScript、字体与站点图片
media/               上传与内容媒体文件
whoosh_index/        新闻搜索索引文件
manage.py            Django 管理入口
requirements.txt     Python 依赖
```

## 本地运行

项目根目录就是 Django app root，`manage.py` 使用 `hengDaProject.settings`：

```powershell
$env:DJANGO_SECRET_KEY = "development-only-secret"
$env:DJANGO_DEBUG = "True"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

运行前请提供开发环境专用的 `DJANGO_SECRET_KEY`；不要把真实 secret 写入 README、shell profile 或 Git。项目的默认数据库是根目录下的 `db.sqlite3`，本地生产 / 部署数据策略应另行规划。

## 项目演进

```text
FGO Chaldea Archive
        ↓
Django Web / SQLite / Admin / Search
        ↓
Chaldea Agent
        ↓
Dify / RAG / Tool Calling / Memory
```

这个 legacy 项目建立了 Web 页面、数据模型、后台管理、搜索和外部 API 的基础；后续的 [fgo-chaldea-agent](https://github.com/woshilsplbd/fgo-chaldea-agent) 将这套基础继续延伸到 AI application engineering。两个项目分别体现传统 Django Web 工程与 Agent 应用工程，职责互补。

<!-- Add legacy website screenshots before final GitHub portfolio release -->

## 项目定位

本仓库保留原始 Django Web implementation，适合展示数据库建模、ORM 持久化、Admin、搜索索引、媒体管理和外部 API integration。活跃的 AI Agent development 已迁移到独立的 [fgo-chaldea-agent](https://github.com/woshilsplbd/fgo-chaldea-agent) repository；本仓库不将自己描述为当前 Agent implementation。
