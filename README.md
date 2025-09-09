[![Prodex workflow](https://github.com/Inswty/prodex_site/actions/workflows/main.yml/badge.svg)](https://github.com/Inswty/prodex_site/actions/workflows/main.yml)
## ProdexSite
ProdexSite — это корпоративное веб-решение, предназначенное для производственных компаний с небольшим ассортиментом продукции. Проект включает публичный сайт-визитку и CMS-панель для самостоятельного управления контентом.

## Технологический стек:
- Python 3.12
- Flask
- SQLAlchemy
- SQLite
- Nginx
- Gunicorn
- Docker / Docker Compose
- GitHub Actions (CI/CD)

## Hosted Version:
[![Website](https://img.shields.io/badge/Visit-Live%20Site-brightgreen)](https://)

## Как запустить:
### Локально:
- Клонируйте репозиторий, установите зависимости, запустите приложение:
```bash
git clone git@github.com:Inswty/prodex_site.git
pip install -r requirements.txt
flask run
``` 
Приложение доступно по адресу:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Докер:
Если в вашей системе установлен Docker, в корневом каталоге выполните:
```bash
docker-compose up -d --build
```
Приложение будет запущено по адресу [http://localhost:5000](http://localhost:5000)

### Деплой в продакшен:
- Создать и заполнить .env файл, скопировать на сервер в директорию проекта:
  Пример содержимого:
```env
  FLASK_APP=app
  FLASK_ENV=production
  FLASK_DEBUG=0
  DATABASE_URI=sqlite:///db.sqlite3
  SECRET_KEY=<YOUR_SECRET_KEY>
```
- Создать SECRETS в GitHub Actions:
```
  DOCKER_PASSWORD
  DOCKER_USERNAME
  HOST
  SSH_KEY
  USER
  SSH_PASSPHRASE
  TELEGRAM_TO
  TELEGRAM_TOKEN
```
- Выполнить пуш GitHub в ветку main:
```bash
git push origin main
```
- При успешном диплое будет отправлено сообщение в мессенджер telegram.

## Админ зона:
Сайт имеет административную панель для управления контентом:
URL: '/admin'
- Доступ: через учетную запись администратора (логин + пароль)  
- Возможности:
  - Управление продукцией (добавление, редактирование, удаление)
  - Категории продукции
  - Настройка главной страницы (текст, изображения, контакты)
  - Работа с пользователями
  - Журнал системных событий и ошибок

![Скриншот](https://github.com/user-attachments/assets/270e83fd-2964-4a2d-adad-edcee70f7ca1)
> [!WARNING]
> При деплое в продакшен создается пользователь:
> ```
> user: admin
> password: secret123
> ```
> ❗ Не забудьте сменить пароль в админке после первого входа!

## Автор:
Проект разработан 
[Павел Куличенко](https://github.com/Inswty)