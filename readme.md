## 介绍
1. 本项目包括前端页面和后端(flask)部分,通过一个RESTFUL API进行交互. 后端需要用到Elasticsearch, 配置文件在`webBackend/common/__init__.py`下.
2. 首次运行需要对ES中的数据初始化, 运行`background_program.py`程序进行初始化, 后续启动从app入口就可以.
## 注意事项
1. 由于dblp数据库过大, 为了初次运行需要手动[下载](https://dblp.org/xml/dblp.xml.gz) dblp数据库,存到`webBackend/resources/`路径下