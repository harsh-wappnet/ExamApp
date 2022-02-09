FROM ubuntu:latest

RUN apt update
RUN apt -y install postgresql

RUN apt autoremove -y && apt autoclean -y

USER postgres

RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER root WITH SUPERUSER PASSWORD 'root';" &&\
    createdb -O docker docker

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/main/postgresql.conf
EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
CMD ["/usr/lib/postgresql/bin/postgres", "-D", "/var/lib/postgresql/main", "-c", "config_file=/etc/postgresql/main/postgresql.conf"]