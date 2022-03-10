FROM python:3.7.12-slim

ARG UID
ARG GID

COPY ./BankAccount/requirements.txt /tmp/requirements.txt

RUN \
	useradd -d /var/lib/django -u $UID django && \
	groupmod -g $GID django && \
  	apt-get update && \
	apt-get install -y \
		nano \
		logrotate \
		supervisor && \
	apt-get clean && \
	mkdir -p /run/supervisor && \
	mkdir -p /etc/supervisor && \
	mkdir -p /var/log/django && \
	mkdir -p /var/lib/django/static && \
	mkdir -p /var/lib/django/media && \
	chown -R $UID:$GID /var/lib/django/static && \
	chown -R $UID:$GID /var/lib/django/media && \
  	chown -R $UID:$GID /var/log/django && \
	chown -R $UID:$GID /var/log/supervisor && \
	chown -R $UID:$GID /run/supervisor && \
	chown -R $UID:$GID /etc/supervisor && \
	chown -R $UID:$GID /var/lib/django && \
	chmod o+w /etc/logrotate.d && \
  	python3 -m pip install -r /tmp/requirements.txt --no-cache-dir && \
  	rm /tmp/requirements.txt

USER $UID

COPY ./entrypoint.sh /var/lib/django/entrypoint.sh

COPY ./supervisord.conf /etc/supervisor/supervisord.conf

COPY ./logrotate.conf /etc/logrotate.d/postgresql.conf

EXPOSE 8000

WORKDIR /var/lib/django

ENTRYPOINT /var/lib/django/entrypoint.sh
