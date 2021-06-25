### Steps to load the SQL Dump:

1. Install PostgreSQL
2. Create Database User and Database
3. Load Database from SQL Dump

### On Debian/Ubuntu:

For 1. and 2. refer to the [Debian Wiki][1].

[1]: https://wiki.debian.org/PostgreSql

For 3. load the Database with

```
psql yourdbname < encdnsdata.sql 
```