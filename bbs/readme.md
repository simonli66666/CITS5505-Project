如何启动网页
1.配置虚拟环境
terminal输入
python3 -m venv venv
source venv/bin/activate  venv\Scripts\activate
2.装些库
pip install -r requirements.txt
3.导入配置py
export FLASK_APP=__init__.py
4.然后通过flask run 命令来启动应用。

注意：Windows 用户请将export替换成set