# db-creator
Generates random insert data for sql

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