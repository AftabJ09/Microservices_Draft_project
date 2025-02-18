FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=user_data
ENV MYSQL_USER=aftab_1
ENV MYSQL_PASSWORD=Qwerty12345

COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306
