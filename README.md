# ELK Airflow - Analysis of Load Balance for Distributed Web Systems

This repo it's used to explain the functionality of a Load Balance Software, fully programmed with Python. 

## Used Services:

* Docker.
* Airflow.
* Nginx.
* Elasticsearch.
* Logstash.
* Kibana.

## Install consideartions:

We need to put the files in order to work correctly in the docker container. I recommend to take some consdierations:

* "docker composer.yml" - yml to deploy the container with all the services and volumes.
* DAGs Python - ".py" files. The name contains "dag". Put it in the dag folder generated for the composer.
* nginx.conf - Nginx configuration file - Put it in the dag folder generated for the composer, configure as you need.
* log tfinal.conf - Logstash configuration file - Put it in the bin folder generated for logstash service.
* BDD MySQL.sql - T-SQL scripts to define all the tables used and some other useful querys.

## General Architecture:


