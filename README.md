# Django_blog
Django实现blog
### 运行前的准备
在settings中更改数据库的用户名密码，建立test数据库
删除mypro/mainapp/migrations和mypro/users/migrations下的所有内容
执行
#### python manage.py makemigrations users
#### python manage.py makemigrations mainapp
#### python manage.py migrate
完成迁移
