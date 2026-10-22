#!/usr/bin/env bash
# Non-repeatable read: A reads twice, B commits an update in between.
#   experiments/isolation.sh                    # REPEATABLE READ (default): both reads equal
#   experiments/isolation.sh 'READ COMMITTED'   # second read sees B's update
set -euo pipefail
sql="$(dirname "$0")/../bin/sql"
level="${1:-REPEATABLE READ}"

"$sql" -N <<SQL | sed 's/^/[A] /' &
SET SESSION TRANSACTION ISOLATION LEVEL $level;
START TRANSACTION;
SELECT 'read 1', balance FROM accounts WHERE id = 1;
DO SLEEP(2);
SELECT 'read 2', balance FROM accounts WHERE id = 1;
COMMIT;
SQL

sleep 1
"$sql" -e "UPDATE accounts SET balance = balance + 100 WHERE id = 1" && echo "[B] +100 committed"
wait
"$sql" -e "UPDATE accounts SET balance = 1000 WHERE id = 1"  # restore
