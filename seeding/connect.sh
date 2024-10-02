# When working from the pipeline dir, source .env causes an error, 
# as if can't find an .env file from it's local seeding directory.
# REPO_ROOT reverts to the base dir relative to the GitHub repo, 
# so all files can be accessed and run.
REPO_ROOT="$(git rev-parse --show-toplevel)"
source "$REPO_ROOT/pipeline/.env"
# A certificate is needed for secure connection without an error, '-C' works for now, 
# but in commercial development environments you would need to download a certificate apparently.
sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -d $DB_NAME -C

