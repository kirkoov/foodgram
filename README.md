# Foodgram

## Description
A website for registered users to post their recipes, add others' as their favourites, subscribe to recipe authors & generate downloadable shopping lists (pdf) in line with the cooking instructions under the recipes they'd like to try.

- This Django+Postgre+Docker+GitHubActions+yaml+TelegramBot for CI/CD project is based on YandexPracticum's template (inc. React) & serves for your favourite cats to be added & boasted of online
- The motivation behind is better learn this backend dev stack & include it in my CV
- Once modified locally & pushed to its GitHub repo, this project moves on along the yaml-based orchestration lines to Actions-rebuild the docker images accordingly & auto-redeploy the project to the live server; the associated Telegram bot will notify me about the deploy
- If you're passionate about sharing your feline pet's pix online & seeing same from other cat people, please head for the [website](https://kittygramme.zapto.org/), sign up & on


1. Сайт, где пользователи публикуют/редактируют/удаляют свои любимые рецепты, управляют своими любимыми рецептами и подписками на публикации других авторов. Зарегистрированным авторам доступен сервис «Список покупок»: для приготовления выбранных блюд создается и скачивается (в формате PDF) список нужных продуктов - суммарно по каждому, без дублирования. В ходе работы над проектом настроено взаимодействие Python-приложения с внешними API-сервисами, создан собственный API-сервис на базе проекта Django; подключено SPA (React) к бэкенду на Django через API; созданы образы и запущены контейнеры Docker; закреплены на практике основы DevOps, включая CI&CD.

Инструменты и стек: #python #JSON #YAML #Django #React #Telegram #API #Docker #Nginx #PostgreSQL #Gunicorn #JWT #Postman





## Table of contents

- [Usage](#usage)
- [Credits](#credits)
- [Licence](#licence)
- [How to contribute](#how-to-contribute)

## Usage

- Register with a username & a password, use them to log in right away
- Upload your pet's pic under 3 Mb in size & see them there
- Spread the word))
- [Back to TOC](#table-of-contents)

## Credits

- Fork from YandexPracticum's repo [here](https://github.com/yandex-praktikum/kittygram_final)
- If interested, follow their [courses](https://practicum.yandex.ru/catalog/programming/?from=main_header-programming_button)
- [Back to TOC](#table-of-contents)

## Licence

MIT [https://choosealicense.com/](https://choosealicense.com/). [Back to TOC](#table-of-contents)

## Features

Add a pic & some details on your pet & make it stand out; edit or delete if needed. Once logged in, you'll see all the registered users' cat pix on the main page. [Back to TOC](#table-of-contents)

## How to contribute

Don't hesitate to contact in case you'd like to contribute. We'd both be better off reading the [Contributor Covenant](https://www.contributor-covenant.org/) which is a standard to start with. [Back to TOC](#table-of-contents)





<span style="color:black;">IP address</span>
<span style="color:red;">goes here</span></br>
<span style="color:black;">Admin login</span>
<span style="color:red;">goeshere</span></br>
<span style="color:black;">Admin pwd</span>
<span style="color:red;">goeshere</span></br>

###### Technology stack: React Python Django DRF PostgreSQL Poetry

### Installations
#### Local install

- goes here

#### Remote install

- goes here


#### .env.example
```
DEBUG
ALLOWED_HOSTS
SECRET_KEY
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
DB_NAME
DB_HOST
DB_PORT
DOCKER_USERNAME
```

For a local non-Docker dev (db.sqlite3-based):

Clone the project and create your virtual env.

1. From the frontend folder run in the Terminal
  - change the package.json's "proxy" from "http://web:8000/" for "http://127.0.0.1:8000/"
  - npm install [ignore the warnings]
  - nmp run build [ignore the warnings]
  - npm start [ignore the warnings]

2. From the backend folder make sure your DEBUG=True, then run
 - make sure your virtual env has all the required packages:
  (e.g. with <poetry add $( cat requirements.txt )>)
 - python manage.py makemigrations
 - python manage.py migrate
 - [no need to loaddata, since the db.sqilte3 is there for you, with all the test data] still run 'python manage.py loaddata db.json' if necessary

 NB: to handle img consistency, <b>django-cleanup</b> is used thanx to the author(s): https://pypi.org/project/django-cleanup/
 By default, the admin zone accepts images <= 1Mb. The live server will be instructed accordingly when the project Dockers there.

3. Back in the browser reload the page http://localhost:3000

4. Admin page is here http://localhost:8000/admin/
   Kindly, 'createsuperuser' yourself.

If some testing is welcome, pls run e.g. 'poetry run pytest' from the backend folder containing the pytest.ini

5. The admin/frontend language can be swapped for Russian before the runserver. See the local Docker deploy instructions for details.

6. For language translation control, visit http://localhost:8000/rosetta/

7. Run 'python manage.py runserver' and refresh the http://localhost:3000 if necessary

8. Navigate, do/undo favourites/sunscriptions, try the PDF shopping list download

test users: yule.neverknow@me.ir        2h5wJ;S%!w.SZDN
            jam.serious@awesome.org     JzvDvNvvc2+a)w4
            juicy.ham@gorgeous.org      U996vS#mHCV87B@




Локальный запуск через Docker

Убедитесь, что у вас в системе установлен Docker (изначально 25.0.4) + docker compose (изначально v2.24.7) и не занят 80-й порт (используется по умолчанию, но можно изменить). Проект создавался и проверялся на Убу 22.

1. Клонировать репозиторий:
mkdir foodgram && cd foodgram && git clone git@github.com:kirkoov/foodgram-project-react.git

cd foodgram-project-react && nano .env
(пример - см .env.example), заполните поля значениями
    DEBUG=False
    ALLOWED_HOSTS="127.0.0.1 0.0.0.0 localhost foodgram.zapto.org"
    SECRET_KEY
    POSTGRES_DB=foodgram_postgre
    POSTGRES_USER=foodgram_user
    POSTGRES_PASSWORD
    DB_HOST=db
    DB_PORT=5432
    DOCKER_USERNAME

NB: файл settings.py настроен так, что для контейнеров значение DEBUG в файле .env должно быть False. True используется в режиме разработки (для DjDT, db.sqlite3). При DEBUG=False БД становится PostgreSQL и пр. (см файл настроек проекта). Так и стоит по умолчанию.

2. Определиться, какие порты пробрасывать локально под контейнеры (по умолчанию на локальный деплой стоят 80:80). Если нужент другой поменяйте в infra/docker-compose.yaml значение ports для контейнера nginx:
    image: nginx:1.19.3
    ports:
      # Live server
      # - "8000:80"
      # Loc dev
      - "80:80"

    If the 80th port is busy, free it or change the above as needed and restart the deploy.

3. Определиться, какой язык будет использован в админке (англ vs рус, en by default):
  - измените в settings.py проекта значение LANGUAGE_CODE = "ru"
  - если язык фронта тоже дб русский, замените папки фронта (public & src) на те, что в архиве (front_end_folders_rus.zip) - там исходный код с русскими названиями, заголовками и пр.
  - если язык ингредиентов дб англ, и далее по переводам в админке см ниже, но имейте в виду, что все ингредиенты можно менять в csv-файлах в корне папки backend (резервные копии этих файлов есть в папке data)

4. In the frontend folder's package.json, make sure the "proxy" field is "http://web:8000/" at the file bottom.

5. Обратно в Терминале идем в папку infra, где есть файл docker-compose.yaml выполнить in the Terminal и дождаться сборки и запуска контейнеров:
sudo docker compose up
->
✔ Network infra_default           Created 0.1s
✔ Volume "infra_media"            Created 0.1s
✔ Volume "infra_static_frontend"  Created 0.0s
✔ Volume "infra_pg_data"          Created 0.0s
✔ Volume "infra_static"           Created 0.0s
✔ Container infra-db-1            Created 0.4s
✔ Container infra-frontend-1      Created 0.3s
✔ Container infra-backend-1       Created 0.3s
✔ Container infra-nginx-1         Created

6. Continue in another Terminal window, из той же папки (infra):
sudo docker compose exec backend python manage.py migrate

sudo docker compose exec backend python manage.py collectstatic
->
169 static files copied to '/app/static_django'

7. если хотите начать "с нуля" (новые админ, пользователи, рецепты, ингредиенты, подписки, избранное):
  - sudo docker compose python manage.py createsuperuser
  - заполняйте в админке соответствующие таблицы, в т.ч. с ингредиентами (название, единица измерения)

+ get the look and feel locally если не хотите ничего заполнять сами, а использовать предварительно подготовленные данные (админ, тестовые пользователи, рецепты, ингредиенты на русском языке, подписки и пр.) just загрузите фикстуру:
  - sudo docker compose exec backend python manage.py loaddata db.json
->
Installed 2240 object(s) from 1 fixture(s)

+ если хотите воспользоваться подготовленными ингредиентами из файлов csv:
  - sudo docker compose exec backend python manage.py import_csv eng
  - OR/AND 'sudo docker compose exec backend python manage.py import_csv rus'
  - then check in the admin zone if these imported ingredients (translated) are in the DB

- NB: если это не первый запуск, а тома не были удалены - все ранее записанные в них данные сохранятся и на этот раз, и будут сообщения, что данные уже есть, и необходимость миграций отпала

- NB2:
If you plan to work with both Russian/English translations, make sure the settings.py's lang_code is the one you need, and the make/compilemessages works in the backend container, open another Terminal and from the same infra folder run:

```sudo docker compose exec backend bash```

```apt update && apt upgrade -y && apt install gettext-base && apt install gettext```

Ctrl+d

sudo docker compose exec -it backend django-admin makemessages --all --ignore=env
sudo docker compose exec -it backend django-admin compilemessages --ignore=env

For the language changes to take effect:

Ctrl+c in the other Terminal to stop the containers and ```sudo docker compose up --build``` with the new lang settings, refresh the admin zone page.

Should there occur any untranslated fields, stop & down the containers, check the lang_code in the settings.py, docker system prune -af & repeat from para. 3 included.

8.
+ для (вдруг необходимой) очистки кэша
  - sudo docker compose exec backend python manage.py clear_cache

9.
Проект будут доступен - в зависимости от выбранного порта/файла докер-компоуз - по адресу: http://127.0.0.1/
(логины и пароли тестовых пользователей см выше)
Админка: http://127.0.0.1/admin/
(для использования админки в случае заполнения БД тестовыми данными -
sudo docker compose exec backend python manage.py createsuperuser)
Документация (изначально на рус) находится по адресу: http://127.0.0.1/api/docs/

10. Удалить проект = остановить контейнеры (ctl+c), удалить их вместе с томами (sudo docker compose down -v), удалить образы и пр. + удалить корневую папку проекта


Запуск проекта в контейнерах на боевом сервере, через репу from GitHub

Убедитесь, что у вас в системе установлен Docker (изначально 25.0.4) + docker compose (изначально v2.24.7) и не занят 80-й порт (используется по умолчанию, но можно изменить). Проект создавался и проверялся на Убу 22.

1. Войти на сайт через SSH, make sure the same about Docker & docker compose as in Локальный запуск через Docker's preamble; make sure port 8090 there is free (ss -ltn), since it's the project's backend default port as indicated in the live server's nginx conf.

2. git clone git@github.com:kirkoov/foodgram-project-react.git
3. cd foodgram-project-react
   Create your .env file there (see the example above)

4. cd infra
    in the docker-compose.yaml change the ports for a live server:
    nginx:
    image: nginx:1.22.1
    ports:
      # Live server
      - "8090:80"
      # Local Docker dev
      # - "80:80"
    volumes:

5. Follow the same steps as in the Локальный запуск через Docker above
   from its para. 3 down to para. 8.

6. Проект будут доступен - в зависимости от выбранного порта - по адресу: https://<yourDomainOrIPaddress>
(логины и пароли тестовых пользователей см выше)
Админка: https:/<yourDomainOrIPaddress>/admin/
Документация (изначально на рус) находится по адресу: https://<yourDomainOrIPaddress>/api/docs/



Запуск проекта в контейнерах локально, с готовыми образами от Docker Hub

Убедитесь, что у вас в системе установлен Docker (изначально 25.0.4) + docker compose (изначально v2.24.7) и не занят 80-й порт (используется по умолчанию, но можно изменить). Проект создавался и проверялся на Убу 22.

1. Build your images locally or use kirkoov's to
sudo docker compose -f docker-compose.production.yaml up (take note of the names of the containers to run)

2. In another Terminal, take the steps above from "Локальный запуск через Docker", w/out the git-cloning, and remember that the ```sudo docker compose``` commands must be used with the ```-f docker-compose.production.yaml``` rather, since it's a different configuration for your Docker deploy based on ready-made images. And remember the case when you nee your frontend in the other language (this requires a separate image pre-build on your own after unzipping the frontend zip)

3. To stop & remove them all, run ```sudo docker compose down -v```



Запуск проекта в контейнерах локально, с готовыми образами от Docker Hub

Убедитесь, что у вас в системе установлен Docker (изначально 25.0.4) + docker compose (изначально v2.24.7) и не занят 80-й порт (используется по умолчанию, но можно изменить). Проект создавался и проверялся на Убу 22.

1. SSH to it
    npm cache clean --force
    sudo apt clean
    sudo journalctl --vacuum-time=1d
2. sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt install docker-compose-plugin

3. mkdir foodgram && cd foodgram

4. From your local Terminal where the project been git-cloned and from its infra folder, check the conf of the docker-compose.production.yaml:

nginx:
    image: nginx:1.22.1
    ports:
      # Live server
      - "8090:80"
      # Local Docker dev
      # - "80:80"

save, close & run
```scp docker-compose.production.yaml root@77.222.43.136:foodgram```

5. Create remotely or scp to the same remote folder your .env file (see above) & nano .env there to change the paths to where your new dot env file is.

+ scp the nginx.conf file to the same remote folder you're working in
scp nginx.conf root@77.222.43.136:foodgram

6. docker compose -f docker-compose.production.yaml up -d

7. Then, if ok, run
the same commands as from the Запуск проекта в контейнерах локально, с готовыми образами от Docker Hub's para 2. Otherwise, stop & run without the -d flag to see the output

8. Проект будут доступен - в зависимости от выбранного порта - по адресу: https://<yourDomainOrIPaddress>
(логины и пароли тестовых пользователей см выше)
Админка: https:/<yourDomainOrIPaddress>/admin/
The docs are not there, but if needed, copy the doc folder manually & indicate its path in the docker-compose.production.yaml before taking step 6 hereof.



#### Authors
###### Frontend YandexPracticum
###### Backend kirkoov
