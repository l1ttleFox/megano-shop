## Megano manual ##
Megano - интернет магазин со всем необходимым для работы и простого развертывания.


#### развертывание пустого проекта ####
в консоль в директории с этим файлом:
```
cd megano/
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```


#### добавление фикстур для проверки работы сайта ####
в консоль в директории с этим файлом:
```
cd megano/
python3 manage.py loaddata fixtures.json
```


#### создание суперпользователя ####
в консоль в директории с этим файлом:
```
cd megano/
python3 manage.py createsuperuser
```
после этого вас попросят ввести email, username и пароль суперпользователя.