from pathlib import Path
import os
import sqlite3

from flask import Flask, g


BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
DEFAULT_DATABASE_PATH = INSTANCE_DIR / "app.db"


def resolve_database_path():
    configured_path = os.getenv("DATABASE_PATH")
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return DEFAULT_DATABASE_PATH


DATABASE_PATH = resolve_database_path()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def ensure_column(db, table_name, column_name, column_sql):
    existing_columns = {row[1] for row in db.execute(f"pragma table_info({table_name})")}
    if column_name not in existing_columns:
        db.execute(f"alter table {table_name} add column {column_sql}")


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DATABASE_PATH)
    db.executescript(
        """
        create table if not exists raw_events (
            event_id integer primary key autoincrement,
            event_time text default current_timestamp,
            event_name text not null,
            anonymous_id text,
            session_id text,
            page_url text,
            page_title text,
            content_theme text,
            message_framing text,
            funnel_stage_intent text,
            cta_label text,
            form_name text,
            article_slug text,
            path_history text,
            landing_page text,
            utm_source text,
            utm_medium text,
            utm_campaign text,
            referrer text,
            traffic_type text default 'live'
        );

        create table if not exists newsletter_signups (
            signup_id integer primary key autoincrement,
            submitted_at text default current_timestamp,
            email text not null,
            job_title text,
            industry text,
            anonymous_id text,
            session_id text,
            landing_page text,
            utm_source text,
            utm_medium text,
            utm_campaign text,
            referrer text,
            traffic_type text default 'live'
        );

        create table if not exists consultation_leads (
            lead_id integer primary key autoincrement,
            submitted_at text default current_timestamp,
            name text not null,
            email text not null,
            job_title text not null,
            industry text not null,
            company_size text,
            primary_goal text,
            urgent_challenge text,
            anonymous_id text,
            session_id text,
            landing_page text,
            content_path_summary text,
            utm_source text,
            utm_medium text,
            utm_campaign text,
            referrer text,
            traffic_type text default 'live'
        );
        """
    )
    ensure_column(db, "raw_events", "traffic_type", "traffic_type text default 'live'")
    ensure_column(db, "newsletter_signups", "traffic_type", "traffic_type text default 'live'")
    ensure_column(db, "consultation_leads", "traffic_type", "traffic_type text default 'live'")
    db.commit()
    db.close()


def create_app():
    app = Flask(__name__, instance_path=str(INSTANCE_DIR))
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-shadow-implementation-key")

    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    init_db()
    app.teardown_appcontext(close_db)

    from .routes import bp

    app.register_blueprint(bp)
    app.get_db = get_db
    return app
