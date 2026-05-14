from pathlib import Path
import sqlite3
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app

DATABASE_PATH = BASE_DIR / 'instance' / 'app.db'
SQL_DIR = BASE_DIR / 'analytics' / 'sql'


def main():
    create_app()
    sql_files = sorted(SQL_DIR.glob('*.sql'))
    if not sql_files:
        raise SystemExit('No SQL files found in analytics/sql.')

    conn = sqlite3.connect(DATABASE_PATH)
    try:
        for sql_file in sql_files:
            conn.executescript(sql_file.read_text())
            print(f'Applied {sql_file.name}')
        conn.commit()

        print('\nAvailable analytics views:')
        for row in conn.execute(
            """
            select name
            from sqlite_master
            where type = 'view'
              and name in (
                  'session_facts',
                  'funnel_rollup',
                  'path_performance',
                  'lead_scoring',
                  'lead_score_summary',
                  'content_performance',
                  'lead_intent_features',
                  'growth_decision_ranking',
                  'content_label_diagnostics',
                  'enriched_growth_decision_ranking',
                  'content_label_comparison',
                  'model_assisted_growth_decision_ranking'
              )
            order by name
            """
        ):
            print(f'- {row[0]}')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
