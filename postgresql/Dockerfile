FROM debian:bullseye-slim

ARG UID
ARG GID

ENV \
	LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
	PGDATA=/var/lib/pgsql/data \
	PGPORT=5432

RUN \
	useradd -d /var/lib/pgsql -u $UID pgsql && \
	groupmod -g $GID pgsql && \
	apt-get update && \
	apt-get -y install \
		nano \
		locales \
		supervisor \
		logrotate \
		postgresql && \
	apt-get clean && \
	localedef -c -f UTF-8 -i en_US en_US.UTF-8 && \
	mkdir -p /run/supervisor && \
	mkdir -p /etc/supervisor && \
	mkdir -p /var/lib/pgsql/data && \
	mkdir -p /var/log/postgresql && \
	mkdir -p /var/run/postgresql && \
	chown -R $UID:$GID /var/run/postgresql && \
	chown -R $UID:$GID /var/log/postgresql && \
	chown -R $UID:$GID /var/log/supervisor && \
	chown -R $UID:$GID /run/supervisor && \
	chown -R $UID:$GID /etc/supervisor && \
	chown -R $UID:$GID /var/lib/pgsql && \
	chmod o+w /etc/logrotate.d

USER $UID

RUN /usr/lib/postgresql/13/bin/initdb --pgdata='/var/lib/pgsql/data' --auth='ident'

COPY ./entrypoint.sh /var/lib/pgsql/entrypoint.sh

COPY ./postgresql.conf /var/lib/pgsql/data/postgresql.conf

COPY ./supervisord.conf /etc/supervisor/supervisord.conf

COPY ./logrotate.conf /etc/logrotate.d/postgresql.conf

EXPOSE 5432

WORKDIR /var/lib/pgsql

ENTRYPOINT /var/lib/pgsql/entrypoint.sh
