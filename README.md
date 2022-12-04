# db-insert-creator
Generates random insert data for sql

## config_sample.yml
```sh
insert:
- filename: out/test.sql
  row_per_insert: 3
  row_total: 7
  schema:
  - key: id
    start: 10000
    type: primary
  - key: int_as_bool
    range:
    - 0
    - 1
    type: int
  - key: const_int
    type: int
    value: 777
  - allow_null: true
    key: range_int
    range:
    - 1
    - 7
    type: int
  - key: const_float
    type: float
    value: 99.99
  - allow_null: true
    key: range_float
    range:
    - 1
    - 7
    type: float
  - key: firstname
    str_type: firstname
    type: str
  - key: lastname
    str_type: lastname
    type: str
  - key: fullname
    str_type: fullname
    type: str
  - key: sentence
    length: sentence
    type: text
  table_name: test_table
```

## sample of generated output
```sh
INSERT INTO test_table
(`id`,`int_as_bool`,`const_int`,`range_int`,`const_float`,`range_float`,`firstname`,`lastname`,`fullname`,`sentence`)
VALUES
(10001,0,777,3,99.99,2.4742033609769747,"Sherry","Christopher","Stephen Ryan","Tempora est magnam dolor voluptatem sit sed magnam."),
(10002,1,777,3,99.99,NULL,"Charles","Schwartz","Marie Ortega","Ipsum eius non ipsum voluptatem porro labore aliquam."),
(10003,1,777,6,99.99,5.820360878308372,"Carol","Chehebar","Tony Cruz","Modi quaerat ipsum dolore neque dolore eius modi.");

INSERT INTO test_table
(`id`,`int_as_bool`,`const_int`,`range_int`,`const_float`,`range_float`,`firstname`,`lastname`,`fullname`,`sentence`)
VALUES
(10004,0,777,NULL,99.99,NULL,"Rebecca","Reed","Thelma Gordon","Sit quiquia consectetur amet."),
(10005,1,777,2,99.99,5.8376610385291325,"Charles","Greek","Margeret Hernandez","Dolore est modi eius dolore amet."),
(10006,1,777,7,99.99,2.2970353018962633,"Robert","Smith","Lisa Cronin","Eius quiquia voluptatem velit.");

INSERT INTO test_table
(`id`,`int_as_bool`,`const_int`,`range_int`,`const_float`,`range_float`,`firstname`,`lastname`,`fullname`,`sentence`)
VALUES
(10007,0,777,2,99.99,2.170473657453792,"Brian","Mortimer","Doris Bynum","Ut sit velit tempora quiquia.");
```

# How to use
## Python

1. Install python requirements
```sh
pip install -r requirements.txt
```

2. Use `--create` to create config file for schema configurations
```sh
python DBInsertCreator.py --create
```

3. Set configured config file with `--config` for generation
```sh
python DBInsertCreator.py --config config_sample.yml
```

## Docker

* Requires `docker` to be installed

1. Build a docker image and tag a name with `-tag`
```sh
# same directory as the Dockerfile
docker build -t dbinsertcreator .
```

2. Create config file using the `--create` flag
```sh
docker run --mount type=bind,source="$(pwd)",target=/usr/src/app dbinsertcreator --create
```

3. Generate the db insert file setting the config file to `--config`
```sh
docker run --mount type=bind,source="$(pwd)",target=/usr/src/app dbinsertcreator --config config_sample.yml
```