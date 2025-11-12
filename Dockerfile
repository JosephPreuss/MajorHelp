# Command to run the container:
# docker build -t majorhelp-db .
# docker container run -p 5432:5432 majorhelp-db

FROM ubuntu

USER root
RUN apt update && apt install -y postgresql

WORKDIR /var/lib/postgres
COPY db.postgres.tar.xz data_majorhelp.tar.xz
RUN tar -xf data_majorhelp.tar.xz
RUN rm data_majorhelp.tar.xz
RUN chown postgres:postgres data_majorhelp -R
RUN chmod 0750 data_majorhelp -R

# TODO: start the postgresql server with the correct CMD ["...", "..."]
USER postgres
EXPOSE 5432
CMD ["ls", "data_majorhelp"]

