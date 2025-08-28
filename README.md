[![Main TNGT workflow](https://github.com/Inswty/tngt_site/actions/workflows/main.yml/badge.svg)](https://github.com/Inswty/tngt_site/actions/workflows/main.yml)
# TNGT Site
Сайт компании TNGT – производитель оборудования для добычи нефти и газа. 
Предназначен для презентации продукции, контактов и корпоративной информации.


```
Админка

Сайт имеет административную панель для управления контентом:

- URL: `/admin`  
- Доступ: через учетную запись администратора (email + пароль)  
- Возможности:
  - Управление продукцией (добавление, редактирование, удаление)
  - Категории продукции
  - Настройка главной страницы (текст, изображения)
  - Контакты компании

После первого запуска сайта можно создать администратора через консоль:
```bash
flask shell
>>> from app.models import User
>>> User.create_admin(email='admin@tngt.ru', password='your_password')
```
flask shell

from app import db
from app.models import User

admin = User(username="admin", is_admin=True)
admin.set_password("secret123")
db.session.add(admin)
db.session.commit()

```
Технологический стек:
- Python 3.12
- Flask
- Flask-Babel
- SQLAlchemy
- SQLite/PostgreSQL
- Docker
```

Автор:
Проект разработан 
[Павел Куличенко](https://github.com/Inswty)