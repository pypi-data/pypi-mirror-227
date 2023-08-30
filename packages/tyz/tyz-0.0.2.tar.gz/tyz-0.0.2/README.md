#库文件的打包与分发
1.安装依赖
```shell
pip setuptools wheel twine 
```
setuptools用于将库文件打包为可分发的包
wheel生成.whl格式的预编译二进制包
twine将包上传到PyPI（需PyPI账号）供他人下载
2.创建工程结构
```
python_test_package
├─ LICENSE #许可证 *必须写
├─ pyproject.toml #包配置文件 *必须写
├─MANIFEST.in #用于指定哪些额外的文件和目录应包含在分发包中
├─ README.md 
├─ src
│  ├─ example01 #每个文件算一个包可以有多个
│  │  ├─ example.py
│  │  └─ __init__.py #这个文件文件用于标识一个目录为包，并可以包含一些初始化代码，以及在导入时需要执行的逻辑。
│  └─ __init__.py
└─ test #测试程序
```
3.


```
python库文件打包与分发
├─ python_test_package
│  ├─ LICENSE
│  ├─ MANIFEST.in
│  ├─ pyproject.toml
│  ├─ README.md
│  ├─ src
│  │  ├─ example01
│  │  │  ├─ example.py
│  │  │  └─ __init__.py
│  │  └─ __init__.py
│  └─ test
├─ README.md
└─ setup.py

```