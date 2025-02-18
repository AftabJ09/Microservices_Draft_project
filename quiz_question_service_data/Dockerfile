FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=admin_data
ENV MYSQL_USER=aftab_2
ENV MYSQL_PASSWORD=Qwerty12345

COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306
