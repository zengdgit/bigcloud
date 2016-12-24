#How To Run

1. 新建virtualenv（建议新建在项目目录下，名称为`.venv`），安装requirements.txt的依赖。(Python版本是3.5.2）
2. 新建mySQL数据库，名称是bigcloud，用户名是root，密码是admin123。
3. 在src/web文件夹下先运行`python manage.py db migrate -m "init"`，再运行`python manage.py db upgrade`，来新建数据表。
4. 在src/web文件夹下运行`python manage.py runserver`来运行项目。


P.S. 没有初始数据啦，所以要调用API`auth/add/<name>/<password>`来新建用户啦。