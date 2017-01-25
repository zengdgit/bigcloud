#How To Run

1. 新建virtualenv（建议新建在项目目录下，名称为`.venv`），安装requirements.txt的依赖。(Python版本是3.5.2）
2. 新建mySQL数据库（用户名为root，密码为admin123），名称为bigcloud。
3. 在src/web文件夹下运行`python manage.py db init`来创建迁移仓库。
4. 接着运行`python manage.py db migrate`来创建迁移脚本。
5. 接着运行`python manage.py db upgrade`来更新数据库。
6. 接着运行`python manage.py deploy`来插入原始数据。
7. 最后运行`python manage.py runserver`来运行项目。
8. 打开127.0.0.1:5354登录，初始用户名和密码均为admin123。
