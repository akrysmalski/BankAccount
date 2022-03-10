FROM debian:stable-slim

ARG UID
ARG GID

RUN \
	useradd -d /var/lib/nginx -u $UID nginx && \
	groupmod -g $GID nginx && \
  	apt-get update && \
	apt-get install -y \
		nano \
		logrotate \
		nginx \
		supervisor && \
	apt-get clean && \
	mkdir -p /etc/nginx/sites-enabled && \
	mkdir -p /etc/nginx/sites-available && \
	mkdir -p /run/supervisor && \
	mkdir -p /etc/supervisor && \
	mkdir -p /var/log/nginx && \
  	chown -R $UID:$GID /var/log/nginx && \
	chown -R $UID:$GID /var/log/supervisor && \
	chown -R $UID:$GID /run/supervisor && \
	chown -R $UID:$GID /etc/supervisor && \
	chown -R $UID:$GID /var/lib/nginx && \
	chown -R $UID:$GID /etc/nginx && \
	chmod o+w /etc/logrotate.d && \
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/nginx.key -out /etc/ssl/certs/nginx.crt -subj "/C=/ST=/L=/O=/CN=/"

COPY ./entrypoint.sh /var/lib/nginx/entrypoint.sh

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./supervisord.conf /etc/supervisor/supervisord.conf

COPY ./logrotate.conf /etc/logrotate.d/postgresql.conf

COPY ./bank_account.conf /etc/nginx/sites-available/bank_account.conf

COPY ./bank_account.conf /etc/nginx/sites-enabled/bank_account.conf

EXPOSE 80 443

ENTRYPOINT /var/lib/nginx/entrypoint.sh
