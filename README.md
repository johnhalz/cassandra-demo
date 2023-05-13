# Cassandra Demo

This repo is to learn about the cassandra database, and create a general purpose interface with cassandra databases.

## Creating a Cassandra instance on Docker

Run the command to pull the image:

``` bash
docker pull cassandra:latest
```

Run the command to start a container (named `cassandra_test`) running on port 9042:

``` bash
docker run -d --name cassandra_test -p 9042:9042 cassandra
```

Pytho library [documentation link](https://docs.datastax.com/en/developer/python-driver/3.27/)