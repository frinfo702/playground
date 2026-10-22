# MySQL playground

A place to poke at MySQL 8.4: query plans, indexes, transactions, locks, internals.
The same schema and config run in a container (default) or as a local server.

## Layout

```
compose.yaml        MySQL 8.4 container, port 3306, root/root, DB `playground`
conf/my.cnf         server config shared by both targets (slow log, deadlock logging, ...)
init/*.sql          schema + seed data, applied on first start
bin/sql             mysql client wrapper (container by default, TARGET=local for local)
bin/local           manage the local server (Homebrew mysql@8.4, port 3307, data in ./data)
experiments/        short, self-explaining demos
```

Seed data: `users` (10k rows), `orders` (200k rows, only `user_id` indexed),
`accounts` (2 rows, for transaction/lock demos).

## Container

```sh
docker compose up -d --wait   # first start runs init/*.sql
bin/sql                       # interactive shell
docker compose down -v        # stop and wipe data (next start re-seeds)
```

From a GUI or another client: `127.0.0.1:3306`, user `root`, password `root`.

## Local server

Uses Homebrew's binaries but its own datadir and port, so it doesn't touch any
`brew services` MySQL.

```sh
brew install mysql@8.4
bin/local init                # create ./data/local, seed it, start on 3307
TARGET=local bin/sql
bin/local stop | start | reset
```

Error log and slow log: `data/local/error.log`, `data/local/db/*-slow.log`.

## Experiments

Every script works with either target (`TARGET=local experiments/...`).
The shell scripts open several sessions in parallel and use `SLEEP()` to order them.

| File | What it shows |
|------|---------------|
| `bin/sql < experiments/index.sql` | full scan vs. range scan, function on a column, covering index |
| `experiments/isolation.sh ['READ COMMITTED']` | non-repeatable read: RR vs. RC |
| `experiments/lock-wait.sh` | row lock wait, `sys.innodb_lock_waits`, `performance_schema.data_locks` |
| `experiments/deadlock.sh` | a deadlock and InnoDB's report of it |
| `bin/sql < experiments/inspect.sql` | table sizes, buffer pool, heaviest statements |

Scripts restore any rows they change. To start fresh, `docker compose down -v`
or `bin/local reset`.

## Handy one-liners

```sh
bin/sql -e "EXPLAIN FORMAT=TREE SELECT ..."
bin/sql -e "SHOW ENGINE INNODB STATUS\G"
bin/sql -e "SHOW VARIABLES LIKE 'innodb%'"
bin/sql -e "SELECT * FROM sys.schema_unused_indexes"
docker compose exec mysql bash   # shell inside the container
```
