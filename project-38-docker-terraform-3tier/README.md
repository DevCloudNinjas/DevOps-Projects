# ⇥ Docker & Terraform Three Tier Architecture

### 𝐴 𝑑𝑒𝑚𝑜𝑛𝑠𝑡𝑟𝑎𝑡𝑖𝑜𝑛 𝑜𝑓 𝑑𝑜𝑐𝑘𝑒𝑟 𝑎𝑛𝑑 𝑡𝑒𝑟𝑟𝑎𝑓𝑜𝑟𝑚 𝑡𝑜 𝑖𝑚𝑝𝑙𝑒𝑚𝑒𝑛𝑡 𝑎 𝑠𝑖𝑚𝑝𝑙𝑒 3 𝑡𝑖𝑒𝑟 𝑎𝑟𝑐ℎ𝑖𝑡𝑒𝑐𝑡𝑢𝑟𝑒 

##  ⇥ Terraform Setup Info

![terraformlogo](https://github.com/harshhaareddy/docker_terraform-three-tier-architecture/blob/master/terraformlogo.png)

```
      ------------------------------------------
      |  Terraform will create below resources |
      ------------------------------------------

      > VPC
      > Application Load Balancer
      > Public & Private Subnets
      > EC2 instances
      > RDS instance
      > Route Table
      > Internet Gateway
      > Security Groups for Web & RDS instances
      > Route Table

      ---------------------------------
      | Instructions to apply changes |
      ---------------------------------

      > terraform init is to initialize the working directory and downloading plugins of the provider
      > terraform plan is to create the execution plan for our code
      > terraform apply is to create the actual infrastructure. It will ask you to provide the Access Key and Secret Key in order to create the infrastructure. So, instead of hardcoding the Access Key and Secret Key, it is better to apply at the run time

```


##  ⇥ Task Info

```
I am going to talk about how to do a classic 3-tier architecture using docker containers and setup infrastructure using terraform
    The 3-tiers will be:

 → Frontend tier: This will host the web application.
 → Middle tier: This will host the api, in our case the REST api.
 → Database tier: This will host the database.
 ```

## 🛡️ 2026 DevSecOps Enhancements (What You Will Learn)
This repository demonstrates a legacy Docker-based 3-tier architecture. In a modern 2026 DevSecOps context, the following critical upgrades have been identified:
1. **Container Privilege De-Escalation:** The provided `Dockerfile` leverages `node:17-alpine` but fails to define an explicitly unprivileged user. To prevent container escapes, modern deployments append a `USER node` directive before executing the CMD.
2. **Multi-Stage Builds:** The current `Dockerfile` contains source code and entire dependency trees. A true DevSecOps implementation refactors this into a two-stage build (Build & Output), ensuring compilers and build-time secrets never exist in the final production artifact.

##  ⇥ Task Conditions 

```
We want to expose the web application to the outside world. 
Simultaneously, we want this layer to be able to talk with the middle tier only not the database tier.

The middle tier will be able to talk with the database only.
```

##  ⇥ Task Documentation 

```
* We are going to build a web application that will display a list of countries and their capitals in a plain old html table. 
* This applications is going to get this data from a rest api which in turn will fetch it from a postgresql database. 
* Its a dead simple app partitioned into 3-tiers. We are going to build the webapp and the rest api in node. 
* Note that this is not going to be a primer on node apps. I assume that the reader is comfortable with creating node webapps.
```

𝑂𝑘 ! 𝐿𝑒𝑡𝑠 𝐵𝑒𝑔𝑖𝑛

###  ⇥ Application

```
→ We are going to build a web application that will display a list of countries and their capitals in a plain old html table. 
→ This applications is going to get this data from a rest api which in turn will fetch it from a postgresql database. 
→ Its a dead simple app partitioned into 3-tiers.
```

###  ⇥ Database Tier

We first create the table structure to hold the data. Here is the table:
```
create table country_and_capitals (
  country text,
  capital text
);
```
We are not bothered about primary key and other things right now to keep it simple.

###  ⇥ Middle Tier

The middle tier is going to be simple node app. I have used the express framework. Here it goes …
```
const express = require('express');
const {
    Pool,
    Client
} = require('pg');
const app = express();
const port = 3001;

const pool = new Pool({
    connectionString: process.env.CONNECTION_STRING
});

app.get('/data', function(req, res) {
    pool.query('SELECT country, capital from country_and_capitals', [], (err, result) => {
        if (err) {
            return res.status(405).jsonp({
                error: err
            });
        }

        return res.status(200).jsonp({
            data: result.rows
        });

    });
});

app.listen(port, () => console.log(`Backend rest api listening on port ${port}!`))
```
Its a simple app listening on port 3001. 
We are using express and pg packages. 
You will have to install them.

Now that we have our app, we proceed to containerise it. Here goes the `Dockerfile` for this app.
```
FROM node:24-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 3001
USER node
CMD [ "node", "index.js" ]
```

You can test this out by issuing the following commands:
```
$ docker build . 
```

This will build the image. To check:
```
$ docker image ls
```

Run the app, we map the machine’s 3001 port to the container’s 3001 using `-p`:
```
$ docker run -p 3001:3001 api
```

Open your browser and go to `http://localhost:3001/data`. You should see a json response like this:
```
JSON will go here
```

###  ⇥ Frontend Tier

The frontend will be again a simple node webapp. Here is the code.
```
const express = require('express');
const request = require('request');

const app = express();
const port = 3000;
const restApiUrl = process.env.API_URL;

app.get('/', function(req, res) {
    request(
        restApiUrl, {
            method: "GET",
        },
        function(err, resp, body) {
            if (!err && resp.statusCode === 200) {
                var objData = JSON.parse(body);
                var c_cap = objData.data;
                var responseString = `<table border="1"><tr><td>Country</td><td>Capital</td></tr>`;

                for (var i = 0; i < c_cap.length; i++)
                    responseString = responseString +
                      `<tr><td>${c_cap[i].country}</td><td>${c_cap[i].capital}</td></tr>`;

                responseString = responseString + `</table>`;
                res.send(responseString);
            } else {
                console.log(err);
            }
        });
});

app.listen(port, () => console.log(`Frontend app listening on port ${port}!`))
```

This app is calling the REST api we created earlier using request package and displaying the data as a table. The api url is taken from a environment variable. The Dockerfile for this app is exactly the same from the middle tier but for the port. We are using the port 3000.
```
FROM node:24-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 3000
USER node
CMD [ "node", "index.js" ]
```

###  ⇥ Putting this together

We are going to run these two containers and a postgresql database container using `docker-compose`. Note that docker-compose is a separate tool that needs to be installed separately. This tool works with docker to orchestrate containers and services.

For this demonstration, we are going to use this folder structure:
```
|
+---frontend
|     +--index.js
|     +--package.json
|     +--package-json.lock
|     +--Dockerfile
+---backend
|    +--index.js
|    +--package.json
|    +--package-json.lock
|    +--Dockerfile
+---init_sql_scripts
|     +--init.sql
+--.dockerignore
+--docker-compose.yml
```

* frontend: has the frontend code and its Dockerfile.
* backend: has the api code and its Dockerfile
* init_sql_scripts: has the sql scripts to populate the database.
* .dockerignore: similar to .gitignore, has entries that the docker will ignore when creating the images.

Here is the `docker-compose.yml` file.
```
version: "3.7"

services:
  api:
    build: ./backend
    environment:
      - CONNECTION_STRING=postgres://demo_user:demo_user@db/demo_db
    depends_on:
      - db
    networks:
      - network-backend
      - network-frontend

  webapp:
    build: ./frontend
    environment:
      - API_URL=http://api:3001/data
    depends_on:
      - api
    ports:
      - "3000:3000"
    networks:
      - network-frontend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: demo_user
      POSTGRES_PASSWORD: demo_user
      POSTGRES_DB: demo_db
    volumes:
      - ./init_sql_scripts/:/docker-entrypoint-initdb.d
    networks:
      - network-backend

networks:
  network-backend:
  network-frontend:
  ```
 We have three services here, `api`, `webapp` and `db`. We will look at these one by one.
 
 Now that we have the `docker-compose.yml` done. We run it.
 ```
 $ docker-compose up --build
 ```
 Here is what you will probably see on the terminal:
 ```
 docker@mc:~/projects/docker-frontend-backend-db$ docker-compose up --build 
Creating network "docker-frontend-backend-db_network-backend" with the default driver
Creating network "docker-frontend-backend-db_network-frontend" with the default driver
Building api
Step 1/8 : FROM node:24-alpine
 ---> d7c77d094be1
Step 2/7 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 09d13bfee0a4
Step 3/7 : COPY package*.json ./
 ---> Using cache
 ---> a37d0fdc2f91
Step 4/7 : RUN npm install
 ---> Using cache
 ---> 26f17e2c518a
Step 5/7 : COPY . .
 ---> Using cache
 ---> f39eb8092a7e
Step 6/7 : EXPOSE 3001
 ---> Using cache
 ---> c327df3d45a1
Step 8/8 : CMD [ "node", "index.js" ]
 ---> Using cache
 ---> 188ce85bbe45

Successfully built 188ce85bbe45
Successfully tagged docker-frontend-backend-db_api:latest
Building webapp
Step 1/8 : FROM node:24-alpine
 ---> d7c77d094be1
Step 2/7 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 09d13bfee0a4
Step 3/7 : COPY package*.json ./
 ---> Using cache
 ---> a7b6397c5f76
Step 4/7 : RUN npm install
 ---> Using cache
 ---> b2bb5b39aa65
Step 5/7 : COPY . .
 ---> Using cache
 ---> 89fef6bdd583
Step 6/7 : EXPOSE 3000
 ---> Using cache
 ---> 972d4ec97d04
Step 7/7 : CMD [ "node", "index.js" ]
 ---> Using cache
 ---> a6371b322bad

Successfully built a6371b322bad
Successfully tagged docker-frontend-backend-db_webapp:latest
Creating docker-frontend-backend-db_db_1 ... done
Creating docker-frontend-backend-db_api_1 ... done
Creating docker-frontend-backend-db_webapp_1 ... done
Attaching to docker-frontend-backend-db_db_1, docker-frontend-backend-db_api_1, docker-frontend-backend-db_webapp_1
db_1      | The files belonging to this database system will be owned by user "postgres".
db_1      | This user must also own the server process.
db_1      | 
api_1     | Backend rest api listening on port 3001!
db_1      | The database cluster will be initialized with locale "en_US.utf8".
db_1      | The default database encoding has accordingly been set to "UTF8".
db_1      | The default text search configuration will be set to "english".
db_1      | 
db_1      | Data page checksums are disabled.
db_1      | 
db_1      | fixing permissions on existing directory /var/lib/postgresql/data ... ok
db_1      | creating subdirectories ... ok
db_1      | selecting default max_connections ... 100
db_1      | selecting default shared_buffers ... 128MB
db_1      | selecting dynamic shared memory implementation ... posix
db_1      | creating configuration files ... ok
db_1      | running bootstrap script ... ok
db_1      | performing post-bootstrap initialization ... sh: locale: not found
db_1      | 2019-05-27 16:19:15.295 UTC [26] WARNING:  no usable system locales were found
db_1      | ok
db_1      | syncing data to disk ... 
db_1      | WARNING: enabling "trust" authentication for local connections
db_1      | You can change this by editing pg_hba.conf or using the option -A, or
db_1      | --auth-local and --auth-host, the next time you run initdb.
db_1      | ok
db_1      | 
db_1      | Success. You can now start the database server using:
db_1      | 
db_1      |     pg_ctl -D /var/lib/postgresql/data -l logfile start
db_1      | 
db_1      | waiting for server to start....2019-05-27 16:19:19.072 UTC [30] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1      | 2019-05-27 16:19:19.343 UTC [31] LOG:  database system was shut down at 2019-05-27 16:19:16 UTC
db_1      | 2019-05-27 16:19:19.412 UTC [30] LOG:  database system is ready to accept connections
db_1      |  done
db_1      | server started
db_1      | CREATE DATABASE
db_1      | 
db_1      | 
db_1      | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
db_1      | CREATE TABLE
db_1      | INSERT 0 1
db_1      | INSERT 0 1
db_1      | INSERT 0 1
db_1      | INSERT 0 1
db_1      | 
db_1      | 
db_1      | waiting for server to shut down...2019-05-27 16:19:20.712 UTC [30] LOG:  received fast shutdown request
db_1      | .2019-05-27 16:19:20.758 UTC [30] LOG:  aborting any active transactions
db_1      | 2019-05-27 16:19:20.762 UTC [30] LOG:  background worker "logical replication launcher" (PID 37) exited with exit code 1
db_1      | 2019-05-27 16:19:20.762 UTC [32] LOG:  shutting down
webapp_1  | Frontend app listening on port 3000!
db_1      | 2019-05-27 16:19:21.182 UTC [30] LOG:  database system is shut down
db_1      |  done
db_1      | server stopped
db_1      | 
db_1      | PostgreSQL init process complete; ready for start up.
db_1      | 
db_1      | 2019-05-27 16:19:21.265 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
db_1      | 2019-05-27 16:19:21.265 UTC [1] LOG:  listening on IPv6 address "::", port 5432
db_1      | 2019-05-27 16:19:21.344 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
db_1      | 2019-05-27 16:19:21.479 UTC [43] LOG:  database system was shut down at 2019-05-27 16:19:21 UTC
db_1      | 2019-05-27 16:19:21.516 UTC [1] LOG:  database system is ready to accept connections
```

To confirm we run docker ps in a new terminal window. This command will display all the containers running.
```
$ docker ps
CONTAINER ID        IMAGE                               COMMAND                  CREATED             STATUS              PORTS                    NAMES
adf24f72e32a        docker-frontend-backend-db_webapp   "node index.js"          25 hours ago        Up 7 minutes        0.0.0.0:3000->3000/tcp   docker-frontend-backend-db_webapp_1
aa97936f829d        docker-frontend-backend-db_api      "node index.js"          25 hours ago        Up 7 minutes        3001/tcp                 docker-frontend-backend-db_api_1
44d732a8f10d        postgres:16-alpine                  "docker-entrypoint.s…"   25 hours ago        Up 7 minutes        5432/tcp                 docker-frontend-backend-db_db_1
```

##  ⇥ Thanks for watching... !!! 
𝐶𝑜𝑝𝑦𝑟𝑖𝑔ℎ𝑡𝑠 𝐼𝑠𝑠𝑢𝑒𝑑..
