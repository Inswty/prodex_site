[![Main TNGT workflow](https://github.com/Inswty/tngt_site/actions/workflows/main.yml/badge.svg)](https://github.com/Inswty/tngt_site/actions/workflows/main.yml)
# TNGT Site
Сайт компании TNGT – производитель оборудования для добычи нефти и газа. 
Предназначен для презентации продукции, контактов и корпоративной информации.


Админка

Сайт имеет административную панель для управления контентом:
```
- URL: `/admin`  
- Доступ: через учетную запись администратора (логин + пароль)  
- Возможности:
  - Управление продукцией (добавление, редактирование, удаление)
  - Категории продукции
  - Настройка главной страницы (текст, изображения, контакты)
  - Работа с пользователями

Важно:
При деплое в продакшен создается пользователь:
'admin' пароль 'secret123'. Не забудьте сменить пароль в админке после первого входа!
```

Как запустить
```
Локально:
1. Клонируйте репозиторий:

    ```bash
git clone git@github.com:Inswty/tngt_site.git
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3. Запустите приложение:
    ``` 
  flask run
    ``` 
Приложение доступно по адресу:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

В продакшен:

  -Создать и заполнить .env файл, скопировать на сервер в директорию проекта:
  Пример содержимого:
      FLASK_APP=app
      FLASK_ENV=production
      FLASK_DEBUG=0
      DATABASE_URI=sqlite:///db.sqlite3
      SECRET_KEY=<YOUR_SECRET_KEY>
  -Создать SECRETS в GitHub Actions:
      DOCKER_PASSWORD
      DOCKER_USERNAME
      HOST
      SSH_KEY
      USER
      SSH_PASSPHRASE
      TELEGRAM_TO
      TELEGRAM_TOKEN
  -Выполнить пуш в GitHub (bash): git push
  При успешном диплое будет отправлено сообщение в мессенджер telegram
```

```
Технологический стек:
- Python 3.12
- Flask
- SQLAlchemy
- SQLite
- Gunicorn
- Docker / Docker Compose
- GitHub Actions (CI/CD)
```

Автор:
Проект разработан 
[Павел Куличенко](https://github.com/Inswty)