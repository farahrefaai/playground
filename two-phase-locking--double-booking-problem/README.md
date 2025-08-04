# two phase locking -- the issue of double booking (race condition) 


1- build the image

`docker build -t two-phase-pg .`

2- create two containers of that image
`
docker run --name pg-two-phase-lock-1 -p 5444:5432 -d -e POSTGRES_PASSWORD=mysecretpassword two-phase-pg
`

3- enter the container and check the data
```
docker exec -it pg-two-phase-lock-1 bash
psql -U postgres

select * from seat_booked;
```

4- in the exec state, start two transactions and try

```
t-1: begin transaction;
t-2: begin transaction;

t-1: select * from seat_booked where seat_id = 1;
t-1: update seat_booked set is_booked = true and customer_name = 'farah' where seat_id = 1;

-- notice that here its returning false
t-2: select * from seat_booked where seat_id = 1;
t-2: update seat_booked set is_booked = true and customer_name = 'farah' where seat_id = 1;
-- pg-2 is frozen now due to locking 

t-1: commit;
t-2: commit;


```


Oops, both got the same seat!!!

5- solution

```
t-1: begin transaction;
t-2: begin transaction;

t-1: select * from seat_booked where seat_id = 4 for update;
t-1: update seat_booked set is_booked = true, customer_name = 'farah' where seat_id = 4;

t-2: select * from seat_booked where seat_id = 4 for update;
-- notice here the terminal is frozen

t-1: commit;

-- t2 is gonna return now that this seat is booked

```