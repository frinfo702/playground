#!/usr/bin/env bash
# Row lock wait: A holds a row lock, B blocks on it, we look at who waits for whom.
set -euo pipefail
sql="$(dirname "$0")/../bin/sql"

"$sql" -e "START TRANSACTION; UPDATE accounts SET balance = 0 WHERE id = 1; DO SLEEP(4); ROLLBACK" &
sleep 1
"$sql" -e "UPDATE accounts SET balance = 1 WHERE id = 1" && echo "[B] got the lock after A rolled back" &
sleep 1

echo "--- sys.innodb_lock_waits: B is waiting on A"
"$sql" -e "SELECT waiting_query, blocking_pid, wait_age, locked_index, locked_type FROM sys.innodb_lock_waits\G"
echo "--- performance_schema.data_locks: every lock currently held/requested"
"$sql" -e "SELECT thread_id, object_name, index_name, lock_type, lock_mode, lock_status, lock_data
           FROM performance_schema.data_locks"
wait
"$sql" -e "UPDATE accounts SET balance = 1000 WHERE id = 1"  # restore
