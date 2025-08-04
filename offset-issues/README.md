# offset issues

offset is very slow and might miss new added rows.

its slow since its fetching the all offset value and then get the selected rows.

1- build the image

`docker build -t pg-offset .`


2- spin up a container
`
docker run --name pg-offset-1 -p 5544:5449 -d -e POSTGRES_PASSWORD=mysecretpassword pg-offset
`

3- enter the container, change the offset, and check the results
```
docker exec -it pg-offset-1 bash
psql -U postgres

explain analyse select title from news order by id desc offset 1000 limit 10 ;
-- the fetched rows = 1010 however we only need 10!!!
```

## fixes
- use the id :).

```
docker exec -it pg-offset-1 bash
psql -U postgres

explain analyse select title from news where id> 10000 order by id desc limit 10 ;

-- the fetched rows = 10

```