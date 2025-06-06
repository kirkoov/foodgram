# Foodgram
Both a recipe website & a shopping list service for you to never forget what 
you need to buy to cook that fancy meal you've heard or seen. The project 
can be tweaked to either an English or Russian interface thanks to `rosetta` 
and it showcases my skills as a Python backend developer able to docker & 
pytest. Please find in the description below the tools and stack used and 
the motivation behind the project.

## Table of contents
- [Description](#description)
- [Usage](#usage)
- [Installations](#installations)
 - [Local non-Docker](#local-non-Docker)
 - [Local Docker](#local-docker)
 - [Remote Docker, GitHub repo-based](#remote-docker-github-repo-based)
 - [Local containers, Docker image-based](#local-containers-Docker-image-based)
 - [Remote containers, Docker image-based](#remote-containers-Docker-image-based)
- [Credits](#credits)
- [Licence](#licence)
- [How to contribute](#how-to-contribute)
- [Authors](#authors)


## Description
Ever wanted to become a gourmet or a real meal maker? Try out others' 
recipes to both your and their satisfaction or otherwise? Or build on this 
to come up with a better-looking thingy, featuring more languages than just 
Eng/Rus? Well, [this project](https://foodgram.zapto.org/) may be your 
starting point. Sign up/in to post/edit/delete your recipes, add others' as 
your favourites or subscriptions & generate downloadable pdf shopping lists 
in line with the recipes you'd like to try. The shop items just sum up if 
duplicate, and go alphabetically. [The admin zone](https://foodgram.zapto.org/admin/) & [the docs](https://foodgram.zapto.org/api/docs/) (in Russian) follow. 

This project helped me a lot in further grasping the following:
- Set up a Django app for it to interact with third-party APIs;
- Use own scripts to populate the database from csv after re-deployments via 
  CI-CD;
- Create a custom API based on a Django project & as per its tech docs/requirements;
- Connect friendlily a React SPA to a backend app for both to perform as one;
- Build & deploy both locally & remotely docker images & containers;
- Enjoy more of DevOps, including CI/CD;
- Use further both [DjDT](https://django-debug-toolbar.readthedocs.io/en/latest/)  for the dev & Telegram bot notifications about GitHub Actions deploys - for better performance & automated deployments;
- Create a downloadable PDF with ingredients & their quantities for your 
  favourite recipes to go shopping with.

Tools & stack: #Python #Django #DRF #Json #Yaml #API #Docker #Nginx 
#PostgreSQL #Gunicorn #Djoser #JWT #Postman #TelegramBot #Flake8 #Ruff 
#Black #Mypy #DjDT #Django-cleanup

[Back to TOC](#table-of-contents)

## Usage
- [Visit](https://foodgram.zapto.org/) & sign up/in with an email-password 
 pair, log in
- Or get straight to the [recipes](https://foodgram.zapto.org/recipes) anonymously
- See the [demo video](https://disk.yandex.ru/i/oBSfTFd1FoFDlA)

[Back to TOC](#table-of-contents)

## Installations
### Local non-Docker
`cd` into a folder of your choice, clone the project from https://github.com/kirkoov/foodgram.git,  `cd foodgram` & create your virtual env (venv, e.g.
with `poetry`). This installation case is best to tweak to your needs and 
language. `rosetta` comes included, but for further ops should be 
re-installed in place to work properly & entered like 
`http://localhost:8000/rosetta/` only while under an admin session. If you care 
about English wording only for your admin zone, uninstall `rosetta`.
##### 1. In the same Terminal, `cd backend` or elsewhere you've put the requirements.txt & run `poetry add $( cat requirements.txt )`. Take the above note about `rosetta` or just remove its lines from the requirements.txt before running this command.

##### 2. If you want to try both the frontend and backend locally, in the frontend folder package.json's "proxy" change the `"http://web:8000/"` to `"http://127.0.0.1:8000/"` & do not forget to undo this change later if required. Then in a Terminal, to launch the frontend, run & ignore warnings:
- `npm install`;
- `npm run build`;
- `npm start`.

##### 3. In the project folder, where the ```.env.example``` file is, create your own .env file like below. If you plan to work with an sqlite3 db only, no need to include all the fields:
```
DEBUG=True
ALLOWED_HOSTS="127.0.0.1 0.0.0.0 localhost foodgram.zapto.org"
SECRET_KEY='django-insecure-tzt1(#hb_0%wb!!12@1$h#-4a36=)d4=(a3cyt%+hgf$x7o$hc'
POSTGRES_DB=foodgram_postgre
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=<insert your pwd>
DB_HOST=db
DB_PORT=5432
```
Then run:
- ```python manage.py makemigrations``` (usually unnecessary with an sqlite3);
- ```python manage.py migrate```;
- ```python manage.py createsuperuser```;
- (optional) `python manage.py test` or `poetry run pytest` from the backend 
 folder containing the `pytest.ini`;
- ```python manage.py runserver```.

<b>NB</b>: to handle img consistency, <b>[django-cleanup](https://pypi.org/project/django-cleanup/)</b> is used. By default, the admin zone accepts 
images<=1Mb, although when running live locally, the frontend may accept 
larger images. Still, in a live server case, the nginx container will 
instruct its Docker cousins not to.

##### 4. Skip if para. 2 above doesn't apply. Back in the browser, reload the page http://localhost:3000 for the test recipes to appear.

##### 5. Admin page: http://localhost:8000/admin/.

##### 6. The admin/frontend language can be swapped for Russian before the runserver command. See the local Docker deploy instructions below for details.

##### 7. For language translation control, if applies, visit http://localhost:8000/rosetta/.

##### 8. Run ```python manage.py runserver``` and refresh the http://localhost:3000 if necessary.

##### 9. Navigate, do/undo favourites/subscriptions, try the pdf shopping list download and/or build on this repo.

[Back to TOC](#table-of-contents)

### Local Docker
Ubuntu 22, Docker 25.0.4, docker compose v2.24.7
##### 1. Make sure your system's port 80 is not busy (by default the project uses this port, which can be changed though) and run in a Terminal:

- make the initial clone steps as [above](#local-non-Docker);
- ```cd foodgram && nano .env``` like in the previous installation instructions.

<b>NB</b>: the settings.py has it in such a way that Docker containers need 
its DEBUG var in the .env as False. The opposite is used for dev (DjDT, db.
sqlite3), while with `False` the project defaults to PostgreSQL.

##### 2. Decide what ports will be piped locally for the containers to run (by default 80:80). Different ports should be indicated in the infra/docker-compose.yaml, e.g. in the nginx service:
```
image: nginx:1.19.3
 ports:
 # Live server
 # - "8000:80"
 # Loc dev
 - "80:80"
```

##### 3. Define the admin zone language (the default Eng vs Rus):
 - change the LANGUAGE_CODE accordingly (settings.py);
 - unzip/replace the frontend public & src folders (see the zip files);
 - if you want the ingredients in Eng too, see more details below, just bear 
 in mind that all of them can be changed in the backend root folder's 
 csv-files (with their bak cousins saved in the data folder).

##### 4. In the frontend folder's package.json, make sure the "proxy" field at the file bottom has the value of ```"http://web:8000/"```.

##### 5. Back in the Terminal, cd to the infra folder containing the docker-compose.yaml, run & wait for the commands to finish & start the containers:
```sudo docker compose up```
which may eventually include (->):
```
✔ Network infra_default Created 0.1s
✔ Volume "infra_media" Created 0.1s
✔ Volume "infra_static_frontend" Created 0.0s
✔ Volume "infra_pg_data" Created 0.0s
✔ Volume "infra_static" Created 0.0s
✔ Container infra-db-1 Created 0.4s
✔ Container infra-frontend-1 Created 0.3s
✔ Container infra-backend-1 Created 0.3s
✔ Container infra-nginx-1 Created
```

##### 6. Continue in another Terminal window, from the same infra folder:
- ```sudo docker compose exec backend python manage.py migrate```;
- ```sudo docker compose exec backend python manage.py collectstatic```.

-> ```169 static files copied to '/app/static_django'```

##### 7. If you want none of the test admin, users, recipes, ingredients, subscriptions, & would rather do them on your own, run:
 - ```sudo docker compose python manage.py createsuperuser```;
 - populate them tables from the admin zone, do your ingredients (name, 
 measurement unit), etc;
 - still, to get the look and feel locally, you may want to use the defaults 
 in Rus, just load this fixture: ```sudo docker compose exec backend python manage.py loaddata db.json```;

-> ```Installed 2240 object(s) from 1 fixture(s)```

 - or/and you may also want to use the default ingredients: ```sudo docker compose exec backend python manage.py import_csv eng``` + ```sudo docker compose exec backend python manage.py import_csv rus```;
 - then check in the admin zone if these imported ingredients (translated) 
 are in the DB.

<b>NB</b>: if for some reason this is not the first time you run these 
commands & the Docker volumes have not been `rm`ed, all such data will 
remain as is & you may see messages about duplicate values in the DB or/and 
that no migrations are necessary.

<b>NB</b>: if you plan to work with both Rus/Eng translations, make sure the 
settings.py lang_code has the value you need, and the 
`makemessages`/`compilemessages` do work in the backend container. Open 
another Terminal and from the same infra folder run:
```sudo docker compose exec backend bash```;
```apt update && apt upgrade -y && apt install gettext-base && apt install gettext```. Then quit (```Ctrl+d```) and run:

```sudo docker compose exec -it backend django-admin makemessages --all --ignore=env```; 
```sudo docker compose exec -it backend django-admin compilemessages --ignore=env```.

And for the language changes to take effect, ```Ctrl+c``` in the other 
Terminal to stop the containers and ```sudo docker compose up --build``` 
again. Refresh the admin zone page. Should there occur any untranslated 
fields, stop & down the containers, check the lang_code in the settings.py, 
do the ```sudo docker system prune -af``` & repeat from para. 3 hereof.

##### 8. If for some reason you need a cache purge, run ```sudo docker compose exec backend python manage.py clear_cache```.

##### 9. If you never changed the ports & docker-compose file, the ready-made recipes, admin zone & docs should be live & kicking at:
- http://127.0.0.1/recipes/;
- http://127.0.0.1/admin/;
- http://127.0.0.1/api/docs/ correspondingly.

##### 10. To delete it all, do the ```Ctrl+c``` + ```sudo docker compose down -v``` + ```sudo docker system prune -af``` + `rm -r` the project folder too.

[Back to TOC](#table-of-contents)

### Remote Docker, GitHub repo-based
Ubuntu 22, Docker 25.0.4 & docker compose v2.24.7
##### 1. Make sure your system's port 80 is not busy (see the prev installation intro) & ssh to your live server. If needed, check that port 8090 there is free (```ss -ltn```), since it's the project's backend default.

##### 2. Git-clone & `.env` the project as before (see [above](#local-non-Docker)).

##### 3. ```cd infra``` & in the docker-compose.yaml change the ports for a live server run like so:
```
 nginx:
 image: nginx:1.22.1
 ports:
 # Live server
 - "8090:80"
 # Local Docker dev
 # - "80:80"
 volumes:
 ...
```
##### 4. Follow the 3-8 steps of the [Local Docker](#local-docker) install.

##### 5. If you never changed the ports & docker-compose file, the project recipes, admin page & docs should be live at:
- http(s)://your_domain_or_IP_address/;
- http(s)://your_domain_or_IP_address/admin/;
- http(s)://your_domain_or_IP_address/api/docs/.

[Back to TOC](#table-of-contents)

### Local containers, Docker image-based
Ubuntu 22, Docker 25.0.4 & docker compose v2.24.7
##### 1. Git-clone the repo (see [above](#local-non-Docker)), tweak the backend/front end folders if needed, build your images locally or use mine, then cd to the infra folder & run:
```sudo docker compose -f docker-compose.production.yaml up``` (please check the names of the containers & ports)

##### 2. In another Terminal, do the same as in the previous install instructions, but skip the git-cloning; and remember that the ```sudo docker compose``` commands must be used with the ```-f docker-compose.production.yaml``` rather. And remember the case when you need your frontend in the other language (this requires a separate image pre-build on your own after unzipping the frontend archive).

##### 3. To stop & remove container, run ```sudo docker compose down -v``` + the ones specified in the prev instructions (e.g. the [Local Docker](#local-docker)'s step 10).

##### 4. The ready recipes, admin & docs pages should be at:
- http://127.0.0.1/ (if you never changed the ports & docker-compose file)
- http://127.0.0.1/admin/
- http://127.0.0.1/api/docs/

[Back to TOC](#table-of-contents)

### Remote containers, Docker image-based
This project been tested on a live server with Ubuntu 22, Docker 25.0.4 & 
docker compose v2.24.7.
##### 1. Ssh to your server & run:
```
npm cache clean --force
sudo apt clean
sudo journalctl --vacuum-time=1d
```
##### 2. Then do:
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin
```
##### 3. ```mkdir foodgram && cd foodgram``` & from your local Terminal where the project been git-cloned and from its infra folder, check the conf of the docker-compose.production.yaml:
```
nginx:
 image: nginx:1.22.1
 ports:
 # Live server
 - "8090:80"
 # Local Docker dev
 # - "80:80"
```
save, close & run
```scp docker-compose.production.yaml <yourServerUser>@<yourServerIP>:foodgram```

##### 4. Create remotely or scp from local Terminal to the same remote folder your .env file (see above) + ```scp nginx.conf <yourServerUser>@<yourServerIP>:foodgram```

##### 5. Then from the remote ssh-Terminal run ```docker compose -f docker-compose.production.yaml up -d```

##### 6. If ok, take the same steps as from the prev instructions' para 2. Otherwise, stop & run without the -d flag to see the output.

##### 7. The project, admin page & docs availability:
- http(s)://your_domain_or_IP_address/ (if you never changed the ports & 
 docker-compose file);
- http(s)://your_domain_or_IP_address/admin/;
- http(s)://your_domain_or_IP_address/api/docs/.

[Back to TOC](#table-of-contents)

## Credits
- The frontend (React) is a fork from YandexPracticum's [repo](https://github.com/yandex-praktikum/foodgram-project-react).

[Back to TOC](#table-of-contents)

## Licence
[MIT]([https://choosealicense.com/])

[Back to TOC](#table-of-contents)

## How to contribute
Do contact in case you think there's a chance to. We'd both be better off 
reading the [Contributor Covenant](https://www.contributor-covenant.org/) which is a standard to start with.

[Back to TOC](#table-of-contents)


## Authors
kirkoov (Django backend), YandexPracticum (React frontend)



