## 介绍
项目整体架构图如下：
![](https://gitee.com/halfcoke/blog_img/raw/master/20210302094748.svg)
1. 论文检索使用 `SQLite + FTS5` 实现，单文件存储，无需额外部署检索服务
2. 项目使用`docker-compose.yml`进行部署，用到了4个镜像：
   - `dblp_data_process`：`registry.cn-beijing.aliyuncs.com/env_halfcoke/dblp-data-process:1.2.0`  该镜像为数据解析及更新模块，负责将DBLP数据写入SQLite检索库
   - `dblp_web_backend`：`registry.cn-beijing.aliyuncs.com/env_halfcoke/dblp-web-backend:2.4.0`   该镜像为使用Flask开发的WEB后端
   - `webserver`：`nginx:1.19.7-alpine`   该镜像为官方nginx镜像
   - `search_data_storage`：`redis:6-alpine`   该镜像用来统计搜索热词
3. 使用`docker-compose.yml`进行部署时，`volumes`说明如下：
   - `dblpweblog`：该volumes用来指定了镜像`dblp_data_process`、`dblp_web_backend`的日志存放地址，该路径下会有三个日志文件：
     - `dblpDataProcess.log`：镜像`dblp_data_process`日志
     - `dblpWebBackend.log` ：镜像`dblp_web_backend`主程序日志
     - `dblpweb.log`：镜像`dblp_web_backend`的`uwsgi`服务日志
   - `dblpwebconf`：该volumes当前仅有`__init.py__`文件，用来进行镜像`dblp_data_process`、`dblp_web_backend`的配置
   - `dblpdata`：该volumes为镜像`dblp_data_process`的`dblpDataProcess/resources`路径，用来存放需要解析的数据文件
   - `dblpdb`：该volumes用来存放SQLite检索库`dblp.sqlite`，同时挂载给数据进程（读写）和WEB后端（只读查询）
   - `nginx_conf`：该volumes用来进行nginx的配置，当前项目路径`nginx_conf`即为nginx配置文件
   - `html`：该volumes用来存放前端代码
   - `redis_data`：该volumes用来存放Redis数据

## 检索接口
`POST /api/v1/search`，请求体：

| 参数 | 说明 |
| --- | --- |
| `keys` | 检索关键词，多个关键词用空格分隔，需同时命中（AND） |
| `category` | 类别数组，如 `["A","B","C"]` |
| `yf` / `yt` | 年份范围，闭区间 |
| `sort` | `time` 按发表年份倒序（默认），`relevance` 按 BM25 相关度 |
| `page` | 页码，从 1 开始，默认 1 |
| `page_size` | 每页条数，默认 20，最大 100 |

响应包含 `papers`（当前页论文）、`total`（命中总数）、`page`、`page_size`、`sort`。

## 注意事项

1. 使用`docker-compose.yml`部署时，需要提前将volumes中指定的主机路径创建好，已知的配置文件可以直接放到路径里。或者保持路径为空，文件内容容器会直接复制进去，再进行修改以及重启容器即可。
