## Test technique DE

We want to have a dockerized project containing an API and a database.  

### 1. API 
Should accepts XML files containing multiple gas prices for different gas types.  
    - On one endpoint accept these files for upload  
    - On a second one, return the average prices

### 2. Database

To store the aforementionned gas types and gas prices and allow us to calculate the average prices.


## Solution

Dockerized solution using docker-compose to simplify the interactions between the API and Database

### Database used
A simple PostgreSQL instance with the minimal database/user/schema/tables to store gas_type/gas_prices and what files these are coming from.  
Setup shell scripts are in folder **./sql_init_scripts**

### API used

A simple Python Flask API, with a file containing the ORM models and a main.py file containing the URL endpoints and the actual processing of files and querying the averages.  
This Flask API is built with the Dockerfile at the root folder; source code is in **./flask_app** folder. 

## Install process 

Using docker, the project can be built with a simple : 

```bash
docker compose up -d --build --force-recreate
```  

the API can then be used with a browser, accessing http://127.0.0.1:8000/  
The root should return True if correctly started, otherwise a problem might be in the logs; if so, check with :  

```bash
docker compose logs
```  


### Tested config : 

docker version : 

Client: Docker Engine - Community  
 Version:           24.0.7  
 API version:       1.43  
 Go version:        go1.20.10  
 Git commit:        afdd53b  
 Built:             Thu Oct 26 09:07:41 2023  
 OS/Arch:           linux/amd64  
 Context:           default  

docker compose version :  
v2.21.0