# evan-Nester

``* 这是一个用来测试构建函数，然后将函数打包成模块的例子代码。
代码nester.py里面的print_lol函数可以实现递归打印数据的功能。``

## 关键代码说明
* evannester.py - 用于编写python语言代码的文件，里面包含print_lol函数。
* setup.py - 用于存放打包相关配置的代码。
* READEME.md - 用于存放说明的文档。
* Makefile - 存放各种快捷命令，通过makefile指令方式执行。
  * 执行命令：
    * `make packages`
    * `make install`
    * `make upload`
  * 代码内容片段：
    * `python setup.py sdist bdist_wheel`
    * `python setup.py install`
    * `twine upload -r evannester dist/*`
  
## 安装依赖
* pip install twine
* python -m pip install --user --upgrade setuptools wheel


    
