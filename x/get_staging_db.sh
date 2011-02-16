#!/bin/bash

#
# db backup
# 

#To see output of this script, uncomment the following line:
#set -x

############
DB_BACKUPS=~/db_backups/ecc_backups
PREFIX=smilekit_prod_
DATE=$PREFIX`date +"%F_%R" | sed 's/-/_/g' | sed 's/:/_/g'`
PROD_SERVER_HOSTNAME=mysmilebuddy.ccnmtl.columbia.edu
PROD_DB_NAME=smilekit
LOCAL_DB_NAME=smilekit_staging
############


#Note: this assumes there is a POSTGRES user on the prod server with your username, with read permission to all the tables in the database. You might need to run:
# sudo -u postgres createuser -D -A -P eddie
# worth=# grant all on database worth to eddie;
# worth=# grant all on table auth_group to eddie; -- and so on, for every single table in the database.

echo "OK. We are downloading the production database $PROD_DB_NAME from $PROD_SERVER_HOSTNAME."
echo "File will be backed up in: $DB_BACKUPS/$DATE"
ssh $PROD_SERVER_HOSTNAME "pg_dump $PROD_DB_NAME >  $DB_BACKUPS/$DATE.out"
echo "Fetching file to your backup directory, $DB_BACKUPS."
scp $PROD_SERVER_HOSTNAME:$DB_BACKUPS/$DATE.out $DB_BACKUPS
echo "Dropping local database $LOCAL_DB_NAME"
sudo -u postgres psql -Upostgres -c "drop database $LOCAL_DB_NAME"
echo "Creating database on dev machine."
sudo -u postgres createdb -O postgres $LOCAL_DB_NAME
echo "Adding data to the new database $LOCAL_DB_NAME."
sudo -u postgres psql -Upostgres -d $LOCAL_DB_NAME -f $DB_BACKUPS/$DATE.out
