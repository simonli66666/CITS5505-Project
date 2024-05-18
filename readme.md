# Food Forum Web Application

## Description

This web application is a food forum where users can register, log in, and share their favorite recipes. Once logged in, users can create posts, like other users' posts, and engage with the .....

## Group Members

| UWA ID     | Name               | GitHub Username  |
|------------|--------------------|------------------|
| 22853272   | Xiheng Li          | simonli66666     |
| 87654321   | Jane Smith         | janesmith        |
| 11223344   | Alice Johnson      | alicejohnson     |

## Instructions for Launching the Application

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/simonli66666/CITS5505-Project.git
    cd CITS5505-Project
    ```

2. **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set the configuration file to initialize the Flask application with the following command:**
    ```bash
    export FLASK_APP=__init__.py
    ```

5. **Run the Application:**
    ```bash
    flask run
    ```


如何启动网页
1.配置虚拟环境
terminal输入
python3 -m venv venv
source venv/bin/activate
2.装些库
pip install -r requirements.txt
3.导入配置py
export FLASK_APP=__init__.py
4.然后通过flask run 命令来启动应用。

注意：Windows 用户请将export替换成set