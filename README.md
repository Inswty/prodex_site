[![Prodex workflow](https://github.com/Inswty/prodex_site/actions/workflows/main.yml/badge.svg)](https://github.com/Inswty/prodex_site/actions/workflows/main.yml)
[![Website](https://img.shields.io/badge/Visit-Live%20Site-brightgreen)](https://)
## ProdexSite
ProdexSite — корпоративное веб-решение для производственных компаний с небольшим ассортиментом продукции. Проект включает:

- Страницы с информацией о компании  
- Перечень продукции с описанием
- Контакты и форма для обратной связи  
- CMS-панель для самостоятельного управления контентом

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
[https://](https://)

## Как запустить:
### Локально:
- Клонируйте репозиторий, установите зависимости:
```bash
git clone git@github.com:Inswty/prodex_site.git
pip install -r requirements.txt
``` 
- Создайте и заполните .env файл:
```env
FLASK_APP=app
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<YOUR_SECRET_KEY>
MAIL_SERVER = <YOUR_MAIL_SERVER>
MAIL_PORT = <YOUR_MAIL_PORT>
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME=<YOUR_EMAIL>
MAIL_PASSWORD=<YOUR_MAIL_PASSWORD>
```
Запустите приложение:
```bash
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
- Cкопировать файл .env на сервер в директорию проекта. Пример содержимого:
```env
FLASK_DEBUG=0
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<YOUR_SECRET_KEY>
SERVER_NAME=<YOUR_SERVER_NAME>
MAIL_SERVER = <YOUR_MAIL_SERVER>
MAIL_PORT = <YOUR_MAIL_PORT>
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME=<YOUR_EMAIL>
MAIL_PASSWORD=<YOUR_MAIL_PASSWORD>
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

![Скриншот](https://github.com/user-attachments/assets/db3a126a-dcd4-4f86-897f-004982fc8c45)
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