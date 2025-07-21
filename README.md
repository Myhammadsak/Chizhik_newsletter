# tbank-emo  
## Запуск проекта  
Перейти в директорию проекта 'bot'   
```bash
cd bot
pip install -r requirements.txt
```
\
Заполнить ключи
bot > bot > settings.py > SECRET_KEY   
bot > bot > settings.py > EMAIL_HOST_USER   
bot > bot > settings.py > EMAIL_HOST_PASSWORD
\
Создать файлы миграций и применить их в бд
```bash
python manage.py makemigrations
python mznage.py migrate
```
\
Проект готов к запуску
```bash
python manage.py runserver
```
***
#### Доступные URL:  
<http://127.0.0.1:8000/> - главная страница\
<http://127.0.0.1:8000/signup/> - регистрация\
<http://127.0.0.1:8000/login/> - авторизация\
<http://127.0.0.1:8000/logout/> - выход из аккаунта\
<http://127.0.0.1:8000/telegram/request-code/> - начало сессии телеграм\
<http://127.0.0.1:8000/telegram/confirm-code/> - подтверждение сессии телеграм(после начала)\
<http://127.0.0.1:8000/group/add/> - добавление ссылок на чаты\
<http://127.0.0.1:8000/newsletter/start/<ID>/> - начало рассылки\
<http://127.0.0.1:8000/newsletter/list/> - список рассылок\
<http://127.0.0.1:8000/newsletter/<int:pk>/> - подробная информация о рассылке\
<http://127.0.0.1:8000/newsletter/logs/> - логи процесса рассылки(после старта)\
<http://127.0.0.1:8000/get-logs/> - логи процесса рассылки(после старта)\
<http://127.0.0.1:8000/newsletter/delete/<ID>/> - удаление рассылки\
<http://127.0.0.1:8000/group/> - список чатов\
<http://127.0.0.1:8000/reset_password/> - сброс пароля\
<http://127.0.0.1:8000/reset_password_sent/> - следующий этап сброса\
<http://127.0.0.1:8000/reset_password/> - сброс пароля\
<http://127.0.0.1:8000/reset_password/> - сброс пароля\
