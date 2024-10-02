source .env
sqlcmd -S $DB_HOST -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -C