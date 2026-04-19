from decouple import config as decouple_config

DB_HOST = decouple_config("DB_HOST", default="")
DB_PORT = decouple_config("DB_PORT", default="5432")
DB_USER = decouple_config("DB_USER", default="")
DB_PASSWORD = decouple_config("DB_PASSWORD", default="")
DB_NAME = decouple_config("DB_NAME", default="")

DATABASE_URL: str = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

DB_TIMEZONE: str = str(decouple_config("DB_TIMEZONE", default="UTC"))