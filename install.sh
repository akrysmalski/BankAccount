#!/bin/bash


# Make an entrypoint for each container executable
for directory in */ ; do
  sudo chmod +x $directory/entrypoint.sh
done


# Generate random passwords
DB_PASSWORD=$(openssl rand -base64 32)
DJANGO_SECRET=$(</dev/urandom tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' | head -c 50  ; echo)


# Remove old env file
if [ -f ".env" ]; then
  sudo rm .env
fi


# Save current user id, group id and generated passwords into env file
echo "UID=$(id -u)" >> .env
echo "GID=$(id -g)" >> .env
echo "DB_PASSWORD=$DB_PASSWORD" >> .env
echo "DJANGO_SECRET=$DJANGO_SECRET" >> .env


# Default values for Django and PostgreSQL users
DJANGO_EMAIL_DEFAULT=test@example.com
DJANGO_PASSWORD_DEFAULT=admin
POSTGRESQL_PASSWORD_DEFAULT=postgres


# Provide passwords for Django admin user and for PostreSQL
read -p "Email for Django admin user [$DJANGO_EMAIL_DEFAULT]: " DJANGO_EMAIL
echo -n "Password for Django admin user [$DJANGO_PASSWORD_DEFAULT]: "
read -s DJANGO_PASSWORD
echo
echo -n "Password for PostgreSQL user [$POSTGRESQL_PASSWORD_DEFAULT]: "
read -s POSTGRESQL_PASSWORD
echo


# Set default if any of provided values are null
DJANGO_EMAIL=${DJANGO_EMAIL:-$DJANGO_EMAIL_DEFAULT}
DJANGO_PASSWORD=${DJANGO_PASSWORD:-$DJANGO_PASSWORD_DEFAULT}
POSTGRESQL_PASSWORD=${POSTGRESQL_PASSWORD:-$POSTGRESQL_PASSWORD_DEFAULT}


# Build images
docker-compose build --force-rm --no-cache


# # Start containers
docker-compose up -d


sleep 30


# Configure PostgreSQL database and user
docker exec -it bank_account_postgresql bash -c "createdb bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"create user bank_account with encrypted password '$DB_PASSWORD'\" | psql bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"alter user bank_account with encrypted password '$DB_PASSWORD'\" | psql bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"alter user bank_account set client_encoding to 'utf-8'\" | psql bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"alter user bank_account set default_transaction_isolation to 'read committed'\" | psql bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"alter user pgsql with password '$POSTGRESQL_PASSWORD'\" | psql bank_account"
docker exec -it bank_account_postgresql bash -c "echo \"grant all privileges on database bank_account to bank_account\" | psql bank_account"


# Give Django access to the database
docker exec -it bank_account_postgresql bash -c "echo \"host bank_account bank_account 10.5.0.5/16 md5\" >> /var/lib/pgsql/data/pg_hba.conf"
docker exec -it bank_account_postgresql bash -c "supervisorctl restart all"


sleep 60


# Create Django admin user
docker exec -it bank_account_django bash -c "echo \"from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', '$DJANGO_EMAIL', '$DJANGO_PASSWORD')\" | python3 BankAccount/manage.py shell"
