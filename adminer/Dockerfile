FROM mariadb:10.5

ENV MYSQL_ROOT_PASSWORD=rootpass
ENV MYSQL_USER=lfr_sink_user
ENV MYSQL_PASSWORD=lfr_sink_password
ENV MYSQL_DATABASE=lfr_sink_db

RUN echo "[mysqld]\n" \
         "bind-address = 0.0.0.0\n" \
         "skip_ssl\n" \
         "skip_networking=0" > /etc/mysql/conf.d/custom.cnf

EXPOSE 3306
