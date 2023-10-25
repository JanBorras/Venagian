# Django Test webapp from Jan Borràs Ros

## Installing

### Docker and docker compose

Instructions from [docker website](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

```
# Docker dependencies
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Docker GPG key
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group
# This is optional, if you don't simply run
# all docker commands as sudo
# Check this for extra info: https://docs.docker.com/engine/install/linux-postinstall/
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

```

# If you run this and you do not have Docker Desktop, nothing will happen

docker context use default

```

# Test that docker is properly installed
docker run hello-world
```

## The App

### Development (such as a local development environment)

1. Clone this repository
2. Copy infra/dev/sample.env to infra/dev/.env, modify the `HOST_UID` and `HOST_GID` variables to match your current user  
   **Note:** You can use the following command to find your UID/GID: `id $USER`

To run it just use the given Makefile:

```
# To build all containers from scratch (useful the first time and when installing new packages)
make build

# To run all containers
make run
```

- The app should work, the `src` folder is mounted inside the containers so any changes to the code should be automagically be reflected
- To go to the swagger pannel go to http://localhost:8080/swagger/
- The default user is suimop/3xh3u5$2021#
- If you mess the DB hard, just delete the directory `infra/dev/database` (will require sudo) and run the app again

**Note:** If you want some test data run `python manage.py loaddata test-data.json`, see the Django section for more information.

```

### Production letsencrypt

1. Clone this repository
2. Copy the letsencrypt certificates to infraestructure/prod-letsencrypt/nginx/ssl

```

# Rename them
mv infra/prod-letsencrypt/nginx/ssl/cert1.pem infra/prod-letsencrypt/nginx/ssl/cert.pem
mv infra/prod-letsencrypt/nginx/ssl/chain1.pem infra/prod-letsencrypt/nginx/ssl/chain.pem
mv infra/prod-letsencrypt/nginx/ssl/fullchain1.pem infra/prod-letsencrypt/nginx/ssl/fullchain.pem
mv infra/prod-letsencrypt/nginx/ssl/privkey1.pem infra/prod-letsencrypt/nginx/ssl/privkey.pem

# Adjust the permisions
chown root:root infra/prod-letsencrypt/nginx/ssl/*.pem
chmod 644 infra/prod-letsencrypt/nginx/ssl/*.pem
```

4. Copy infra/prod-letsencrypt/sample.env to infra/prod-letsencrypt/.env, modify the `HOST_UID` and `HOST_GID` variables to match the desired user
   **Note:** You can use the following command to find the UID/GID: `id <USER>`

5. Modify the infra/prod-letsencrypt/.env and set the variable `DJANGO_CSRF_TRUSTED_ORIGINS`:

```
# For example, when deployed to a AWS server with a DNS of venagian.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://venagian.com:8080
```

6. Run the project:

```
make build ENV=prod
```

7. Now you need to configure Google auth

8. Configure a [Google Project](https://www.rootstrap.com/blog/how-to-integrate-google-login-in-your-django-rest-api-using-the-dj-rest-auth-library)

9. In /admin/sites/site/ add the site

10. In /admin/socialaccount/socialapp/ add a new social application

11. In api.view.auth.GoogleLoginView adjust the callback URL

```
Provider: Google
Name: Main
Client ID: The client id
Secret key: The secret key
Sites: Move the corresponting site to the right
```

**Note:** The `media` path should be changed, this is the directory where all the files will be uploaded. So go into the docker-compose.yml and change the lines (should be 3 lines) that contain `- ./persistent/media:/media` and change the `./persistent/media` with the desired path, note that the folder must be created by the user you will use inside the container. **DO NOT** change the part after the colon, as that is the internal path in the django container.

### Django

**NOTE:** I would strongly recommend everyone to do the [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/) and then the [Django REST tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/), this would be a part from this project, since it comes preconfigured.

- The django commands (the manage.py ones) will have to be run through docker, see next section for extra information
- Anytime you change a class (add a new field, change the type) in models.py, you will require to update the DB, to do so:
  ```
  # This creates a Python file explaining the modifications to the DB
  python manage.py makemigrations
  # And this one makes the actual modifications
  python manage.py migrate
  ```
- If you want to create more users use `python manage.py createsuperuser`
- If you want to open a python shell inside the app: `python manage.py shell`
- If you want a shell to the postgres db: `python manage.py dbshell`

Tip: How to dump all the data:

```
python manage.py dumpdata --natural-foreign --exclude=auth.permission --exclude=contenttypes --exclude=admin.logentry --indent=4 > api/fixtures/test-data.json
```

### Docker

You will mainly want to work with the `dev-venagian` container, some useful commands:

```
# Logs from dev-app container
docker logs -f dev-app

# Open a shell inside the container
docker exec -it dev-app /bin/bash

# Call manage.py from the host
docker exec -it dev-app python manage.py makemigrations
```

### Style

We will use flake8 and isort for stilying, please install isort, flake8 and autopep8 on your preferred virtualenv:

```
pip install autopep8 isort flake8
```

Then:

- Run `make am-i-beautiful` in the root of the project to do changes manually OR
- Run `make beautiful` in the root of the project to style everything

### General notes

**Create user**
**Note: This needs an admin token, in dev ask for a token using suimop/3xh3u5$2021#**

```
curl -X 'POST' \
  'http://localhost:8080/users/' \
  -H 'Authorization: Token ADMIN_TOKEN' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "username@email.com",
  "password": "password"
}'
```

**Get an Authorization Token**

```
curl -X 'POST' \
  'http://localhost:8080/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "username@email.com",
  "password": "password"
}'
```

This will return the token which is valid for one day:
`{"id":13,"email":"username@email.com","token":"470865c9f7883338395bf11859be204964c3697f"}`

**Curl example**
`curl -X GET http://localhost:8080/users/ -H 'Authorization: Token 470865c9f7883338395bf11859be204964c3697f'`

# Misc

## Loading test data

You need to disable all the post_save signals before importing the data (or they will create extra objects when importing the data, which breaks things).

```
python manage.py loaddata test-data.json
```

Then make sure to uncomment those lines!
