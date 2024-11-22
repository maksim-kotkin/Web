export PGPASSWORD=secret
psql --host 127.0.0.1 -p 5430 -U app -d postgres -c "drop database app"
psql --host 127.0.0.1 -p 5430 -U app -d postgres -c "create database app"