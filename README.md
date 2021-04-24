# BookmarkManager

SPE Final Project for Bookmark Manager

## Production Docker Container Creation and setup

Just run the following commands:

```shell
docker-compose -f docker-compose.prod.yml up -d --build
```

Then, run the command below to view the logs and check status of the containers

```shell
docker-compose -f docker-compose.prod.yml logs -f
```

After all the containers are up and running, you can visit <http://localhost:1337/admin/> and login to the admin interface. To bring down the container run

```shell
docker-compose -f docker-compose.prod.yml down -v
```

## Docker Dev Environment Setup Instructions

```shell
docker-compose up -d --build
```

This should build the images and start running the containers.
To check if the server went up, run

```shell
docker-compose logs -f
```

This should show any errors that might have occured while building.
If everything worked properly, you can visit <http://localhost:8000/> and see if you get the Django Startup page.

## Dev Setup Instructions

### DB and Django Setup Commands

#### Required installs and updates

```shell
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

#### POSTGRES setup

```shell
sudo -u postgres psql
postgres=# CREATE DATABASE bookmark_manager;
postgres=# CREATE USER djangouser WITH PASSWORD 'password';
postgres=# ALTER ROLE djangouser SET client_encoding TO 'utf8';
postgres=# ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE djangouser SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE bookmark_manager TO djangouser;
postgres=# \q
```

#### Virual ENV setup

```shell
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
mkdir ~/myprojectdir <your project directory (where there is going to be manage.py file)>
cd ~/myprojectdir
virtualenv bmenv
source bmenv/bin/activate <Activating your env>
pip install django gunicorn psycopg2-binary
```

<<<<<<< HEAD
#### Django Starting Setup
=======
### Django Starting Setup
>>>>>>> Jenkins ready trial 1

The startup is something that I have already done on my side, as well as the project settings required for setup.
Now to setup your local db. (Ensure venv is active)

```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

username: ram/rahul; password:password; no email;

```shell
python3 manage.py collectstatic
```

Now, you can check if Django normally works (default django server with postgres) through these commands

```shell
sudo ufw allow 8000
~/myprojectdir/manage.py runserver 0.0.0.0:8000
```

Visit <http://0.0.0.0:8000> and check if Django is working.

### Gunicorn and Nginx Setup Commands

If you can't figure out why, check the guide here and troubleshoot: <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04>
The steps are very similar except for the paths.

#### Gunicorn Commands

```shell
cd ~/myprojectdir <Go to directory with manage.py>
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

Check if at the above link if the Django app has loaded. This implies that gunicorn has started serving the Django App.
Now, leave the django app.

```shell
deactivate
```

```shell
Go to the file below:
sudo vim /etc/systemd/system/gunicorn.socket
```

Add the following lines:

```text
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Go to the file below:

```shell
sudo nano /etc/systemd/system/gunicorn.service
```

Look carefully at the text below and replace the required paths with ones relevant to your system.
Add the following lines:

```text
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy<user>/myprojectdir<project directory>
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Now, let's reload gunicorn and see if it worked.

```shell
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

It should say 'active'. Don't run the start command twice within 10 secs, it will fail.
Troubleshoot using this command.

```shell
sudo journalctl -u gunicorn.socket
```

This shows some logs as to why it could be an issue.

```shell
sudo systemctl status gunicorn
```

Now, to check if it works through curl.
This should be inactive, cause we haven't started the server yet. If it says active, stop it using

```shell
sudo systemctl stop gunicorn.socket
```

Now, try running

```shell
curl --unix-socket /run/gunicorn.sock localhost
```

You should get a HTML dump on the terminal. If you don't, then there's some error that needs to be fixed.
Check logs

```shell
sudo journalctl -u gunicorn
```

Also, if you make changes to the files, you need to restart the daemon using these commands:

```shell
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

<<<<<<< HEAD
### Configuring Nginx
=======
#### Configuring Nginx
>>>>>>> Jenkins ready trial 1

Go to this file

```shell
sudo vim /etc/nginx/sites-available/bookmark_manager
```

Add these lines (Ensure that the paths match your system)

```text
server {
    listen 80;
    server_name 127.0.0.1;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ram/IIITB/Sem8/SPE/BookmarkManager/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Add a symlink and check syntax errors

```shell
sudo ln -s /etc/nginx/sites-available/bookmark_manager /etc/nginx/sites-enabled
sudo nginx -t
```

If no errors, restart ngingx

```shell
sudo systemctl restart nginx
```

Now, we can open up the port and check if it works.

```shell
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

Now, you can check whether the project works. Simply head to <http://127.0.0.1/> and see if the django startup screen shows up.

END
