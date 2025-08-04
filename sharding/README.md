# Sharding

testing sharding on local using Flask and Postgres.

## Prepare Shards

1- build the image
``

2- create three Db instaces are created using docker.

`
docker run --name pgshard-1 -p 5441:5432 -d -e POSTGRES_PASSWORD=mysecretpassword pgshard
docker run --name pgshard-2 -p 5442:5432 -d -e POSTGRES_PASSWORD=mysecretpassword pgshard
docker run --name pgshard-3 -p 5443:5432 -d -e POSTGRES_PASSWORD=mysecretpassword pgshard
`

3- check that the three containers are up and running
`
docker ps
`

4- pgadmin to observe data
`
docker run -p 5555:80 --name pgadmin -d -e PGADMIN_DEFAULT_EMAIL="farah@gmail.com" -e PGADMIN_DEFAULT_PASSWORD=password dpage/pgadmin4

`

check the logs of the container 
`docker container logs pgadmin`

once workers are up and running, go to localhost:5555

## Flask app
1- create a virtual machine and activate it 

```
python -m venv flask-env
flask-env\Scripts\activate
```

2- install the needed packages and freeze them

```
pip install flask
pip install uhashring
pip install psycopg2
pip freeze > requirements.txt
```

3- call /POST url with "url" body and check the targeted shard
4- call /GET url with urlId and check the targeted shard