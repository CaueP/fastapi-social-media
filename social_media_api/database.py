import databases
import sqlalchemy
from social_media_api.config import config

metadata = sqlalchemy.MetaData()

# Database tables
post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    ),
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create tables in the database
metadata.create_all(engine)

database = databases.Database(
    config.DATABASE_URL,
    force_rollback=config.DB_FORCE_ROLL_BACK,
)
