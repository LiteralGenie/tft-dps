from tft_dps.lib.paths import TFT_DB_FILE
from tft_dps.lib.utils.db_utils import Db, DbWrapper


class TftDb(DbWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(TFT_DB_FILE, *args, **kwargs)

    def init_schema(self, conn: Db):
        conn.executescript(
            """
            BEGIN;

            CREATE TABLE IF NOT EXISTS combo (
                id          TEXT        PRIMARY KEY
            ) STRICT;

            CREATE TABLE IF NOT EXISTS dps (
                id_combo    TEXT        NOT NULL,
                type        TEXT        NOT NULL,   -- auto | cast
                t           REAL        NOT NULL,
                physical    REAL        NOT NULL,
                magical     REAL        NOT NULL,

                UNIQUE (id_combo, type, t),
                FOREIGN KEY (id_combo) REFERENCES combo (id)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_unit (
                id_combo    TEXT        PRIMARY KEY,
                unit        TEXT        NOT NULL,
                stars       INTEGER     NOT NULL,

                UNIQUE (id_combo, unit, stars)
                FOREIGN KEY (id_combo) REFERENCES combo (id)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_item (
                id_combo    TEXT        PRIMARY KEY,
                item        TEXT        NOT NULL,

                UNIQUE (id_combo, item)
                FOREIGN KEY (id_combo) REFERENCES combo (id)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_trait (
                id_combo    TEXT        PRIMARY KEY,
                trait       TEXT        NOT NULL,
                count       INTEGER     NOT NULL,

                UNIQUE (id_combo, trait, count)
                FOREIGN KEY (id_combo) REFERENCES combo (id)
            ) STRICT;

            COMMIT;
            """
        )
