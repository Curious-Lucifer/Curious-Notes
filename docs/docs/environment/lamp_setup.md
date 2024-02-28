# LAMP Setup

## Directory Structure
```
.
├── Dockerfile
├── db
├── docker-compose.yml
└── web
    └── 
```

---
## Files
### Dockerfile
```Dockerfile
FROM php:7.4-apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

RUN apt update && apt upgrade -yq
```

### db
```shell
#!/bin/bash

docker exec -it mysql mysql -u root -p
```

### docker-compose.yml
```yml
version: '2'

services:
    php_apache:
        container_name: php_apache
        build: .
        ports:
            - 8000:80
        volumes:
            - ./web:/var/www/html

    mysql:
        container_name: mysql
        image: mysql
        environment: 
            MYSQL_ROOT_PASSWORD: root
            MYSQL_DATABASE: TESTDB
            MYSQL_USER: curious
            MYSQL_PASSWORD: curious
```