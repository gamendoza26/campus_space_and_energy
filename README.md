# rest-api-docker-compose
Example of using docker-compose to orchestrate deployments and interconnections between multiple containers. In this projecty we have a FastAPI web container, a Postgres database container, and a PgAdmin container.

The FastAPI container can call the postgres database container to search and store information
The PgAdmin container provides a web admin interface to the Postgres container (so it talks to the Postgres database container)

The project also illustrates using gitlab's continuous integtration/continuous deploy feature to automate builds and deploys into two different environments. The 'main' branch of this project dropys to the 'production' server when there is a commit pushed to main. The 'development branch builds and deploys to a development server when commits are pushed to the development branch.

## Buiding and running via Gitlab CI/CD

When a commit happens to either of the branches of this project, gitlab looks at the .gitlab-ci.yml script to know what CI/CD pipelines to run.

To run the CI/CD script, gitlab uses 'gitlab-runners' that you have installed and configured on your servers to execute the commands in the .gitlab-ci.yml script. The script uses tags associated with the runners' configuration to differentiate between the production and development runners and servers.

When triggered by a push to the repository, the gitlab runner first pulls a copy of the code from the git repository for the branch, then runs the 'before_script' section of the .gitlab-ci.yml script, followed by the steps for each of the stages. We can associate steps in the stages of a CI/CD script with a specific branch of the project; this is why you see "environment" and "only" items in the task descriptions in .gitlab-ci.yml script.

Most of the real work of building and running the containers is handled by the shell scripts "build-test", "run-test", "build-production", and "run-production". Here we take advantage of docker-compose top orcheatrate builds and deploys.

## docker-compose orchestration

There are two files that define the containers, how they interoperate, and how they are built: "docker-compose-production.yml" and "docker-compose-development.yml". In these files are descriptions of the services (pgdatabase, pgadmin, web) their4 configuration, storage, and interdependencies.


## setting up gitlab-runners

## Overview

This branch is set up to test files before moving them to origin main. It contains several directories:

1. **api:** Contains Dockerfiles, along with subdirectory "app" and "wifi-app"
2. **db:** Holds the scripts such that if we run the terminal, users can use the scripts without having access to the database
3. **jupyter:** Contains necessary files to generate heatmap visualization (html) through widgets
4. **website-front-end:** Contains all the images, resources and python files necessary to generate voila webpage

## Issues

1. **Merge conflicts:** Right now, we are struggling to fix merge conflicts. Jupyter creates new "execution_count" variables every time we render up the notebook through the voila window. This is annoying, but we have been able to work around it.

TEST
=======
``````
     # install gitlab-runner 
     curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
     sudo apt-get install -y gitlab-runner
	 
	 # setup the gitlab-runner user with sudo rights
	 sudo su root
	 echo "#rules for gitlab-runner" > /etc/sudoers.d/90-gitlab-runner
	 echo "gitlab-runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-gitlab-runner
	 echo "" >> /etc/sudoers.d/90-gitlab-runner

	 # now type <control-d> to exit the 'sudo su root' context

``````

 After you have installed the gitlab runner, you can associate it with your project by registering it


## other misc configuration

We want to run the application under a generic user rather than your personal account. There is already a generic user on all VCM linux VMs named 'vcm' -- this is the user the CI/CD script assumes you will use.


``````
	 # on the development VM, create a directory where will will keep the development branch
	 mkdir /home/vcm/development
	 cd /home/vcm/development

	 # on the production VM, create a directory where will will keep the production branch
	 mkdir /home/vcm/production
	 cd /home/vcm/production
``````

We do not want to store sensitive configuration info in this gitlab project, so you will also need to create a configs directory holding a file named 'env' which the CI/CD script copies into place when building the containers.


``````
	 # on both the development and productionVMs, create a configs directory 
	 mkdir /home/vcm/configs
     
``````


 Inside the /home/vcm/configs directory you will need and 'env' file that holds some important settings. Here is an example
 
 
``````
	 POSTGRES_USER=postgres
	 POSTGRES_PASSWORD=change-this-password
	 POSTGRES_DB=postgres
	 # pagadmin login info
	 PGADMIN_DEFAULT_EMAIL=your-netid-goes-here@duke.edu
	 PGADMIN_DEFAULT_PASSWORD=change-this-password
	 # leave the PGADMIN_LISTEN_PORT set to 80, the docker-compose scripts assume this is the setting
	 PGADMIN_LISTEN_PORT=80

``````
 
## connecting to the components

- the PgAdmin container can be accessed at http://your-vcm-server.vm.duke.edu:8090/
-- login using the PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD settings from your env file
- FastAPI is running at http://your-vcm-server.vm.duke.edu:8080/

From the linux command line, you can verify that the web container where FastAPI runs can connect to the Postgres container with the postgres command line client (psql) by first starting a bash shell inside the like this

``````
	 vcm@vcm-41377:~/configs$ sudo docker ps
	 CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                            NAMES
	 dfff007759b2   helix-api               "fastapi run app/mai…"   42 minutes ago   Up 42 minutes   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp        development-web-1
	 812e3f1f1a75   dpage/pgadmin4:latest   "/entrypoint.sh"         42 minutes ago   Up 42 minutes   443/tcp, 0.0.0.0:8090->80/tcp, :::8090->80/tcp   development-pgadmin-1
	 f3310a82ce7b   postgres:16             "docker-entrypoint.s…"   42 minutes ago   Up 42 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp        development-pgdatabase-1
	 vcm@vcm-41377:~/configs$ sudo docker exec -it dfff007759b2 bash
	 jovyan@dfff007759b2:/$ psql postgresql://postgres:change-this-password@pgdatabase/
	 psql (15.6 (Debian 15.6-0+deb12u1), server 16.3 (Debian 16.3-1.pgdg120+1))
	 WARNING: psql major version 15, server major version 16.
	          Some psql features might not work.
	 Type "help" for help.

	 postgres=# \l
	                                                 List of databases
	    Name    |  Owner   | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |   Access privileges   
	 -----------+----------+----------+------------+------------+------------+-----------------+-----------------------
	  postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
	  template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
	            |          |          |            |            |            |                 | postgres=CTc/postgres
	  template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/postgres          +
	            |          |          |            |            |            |                 | postgres=CTc/postgres
	 (3 rows)

	 postgres=# 
     
``````

If you had created a database named 'meow' (something you might do with PgAdmin), some inside the web container this python code would establish a connections

``````
	 import psycopg2
	 connection = psycopg2.connect(user="postgres",  # just use your connection info
	                               password="change-this-password",
	                               host="pgdatabase",
	                               port="5432",
	                               database="meow")
     
``````


In addition to psycopg2, sqlalchemy is another popular approach for accessing SQL database from python... 

  
## To do

Actually hook up FastAPI web code to the database and save something...


TEST TEST TEST
