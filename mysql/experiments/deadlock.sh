#!/usr/bin/env bash
# Deadlock: A locks row 1 then 2, B locks row 2 then 1. InnoDB kills one (ERROR 1213).
set -euo pipefail
sql="$(dirname "$0")/../bin/sql"

"$sql" -e "START TRANSACTION; UPDATE accounts SET balance = balance - 1 WHERE id = 1;
           DO SLEEP(1); UPDATE accounts SET balance = balance + 1 WHERE id = 2; ROLLBACK" 2>&1 | sed 's/^/[A] /' &
"$sql" -e "START TRANSACTION; UPDATE accounts SET balance = balance - 1 WHERE id = 2;
           DO SLEEP(1); UPDATE accounts SET balance = balance + 1 WHERE id = 1; ROLLBACK" 2>&1 | sed 's/^/[B] /' &
wait

echo "--- LATEST DETECTED DEADLOCK"
"$sql" -N --raw -e "SHOW ENGINE INNODB STATUS" \
  | sed -n '/LATEST DETECTED DEADLOCK/,/^TRANSACTIONS$/p'
