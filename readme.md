## 介绍
项目整体架构图如下：
![](https://gitee.com/halfcoke/blog_img/raw/master/20210302094748.svg)
1. 项目使用`docker-compose.yml`进行部署，用到了4个镜像：
   - `ElasticSearch`：`registry.cn-beijing.aliyuncs.com/env_halfcoke/elasticsearch:7.11.1`   该镜像与官方镜像相同，此地址仅用来加速
   - `dblp_data_process`：`registry.cn-beijing.aliyuncs.com/env_halfcoke/dblp-data-process:1.0.0`  该镜像为数据解析及更新模块
   - `dblp_web_backend`：`registry.cn-beijing.aliyuncs.com/env_halfcoke/dblp-web-backend:2.0.0`   该镜像为使用Flask开发的WEB后端
   - `webserver`：`nginx:1.19.7-alpine`   该镜像为官方nginx镜像
2. 使用`docker-compose.yml`进行部署时，`volumes`说明如下：
   - `dblpweblog`：该volumes用来指定了镜像`dblp_data_process`、`dblp_web_backend`的日志存放地址，该路径下会有三个日志文件：
     - `dblpDataProcess.log`：镜像`dblp_data_process`日志
     - `dblpWebBackend.log` ：镜像`dblp_web_backend`主程序日志
     - `dblpweb.log`：镜像`dblp_web_backend`的`uwsgi`服务日志
   - `dblpwebconf`：该volumes当前仅有`__init.py__`文件，用来进行镜像`dblp_data_process`、`dblp_web_backend`的配置
   - `dblpdata`：该volumes为镜像`dblp_data_process`的`dblpDataProcess/resources`路径，用来存放需要解析的数据文件，后续增加功能后可能会用到。
   - `nginx_conf`：该volumes用来进行nginx的配置，当前项目路径`nginx_conf`即为nginx配置文件
   - `html`：该volumes用来存放前端代码
   - `es_data`：该volumes用来存放ElasticSearch的数据
   - `es_conf`：该volumes用来进行ElasticSearch的配置

## 注意事项

1. 使用`docker-compose.yml`部署时，需要提前将volumes中指定的主机路径创建好，已知的配置文件可以直接放到路径里。或者保持路径为空，文件内容容器会直接复制进去，再进行修改以及重启容器即可。
