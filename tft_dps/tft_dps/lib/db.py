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
                id_combo    TEXT        NOT NULL
                    REFERENCES combo (id)
                    ON DELETE CASCADE,
                type        TEXT        NOT NULL,   -- auto | cast | misc
                t           REAL        NOT NULL,
                mult        REAL        NOT NULL,
                physical    REAL        NOT NULL,
                magical     REAL        NOT NULL,
                true        REAL        NOT NULL
            ) STRICT;
            
            CREATE INDEX IF NOT EXISTS dps_id_combo ON dps (id_combo);

            CREATE TABLE IF NOT EXISTS stats (
                id_combo    TEXT        NOT NULL
                    REFERENCES combo (id)
                    ON DELETE CASCADE,
                data        TEXT        NOT NULL,

                UNIQUE (id_combo)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_unit (
                id_combo    TEXT        NOT NULL
                    REFERENCES combo (id)
                    ON DELETE CASCADE,
                unit        TEXT        NOT NULL,
                stars       INTEGER     NOT NULL,

                UNIQUE (id_combo, unit, stars)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_item (
                id_combo    TEXT        NOT NULL
                    REFERENCES combo (id)
                    ON DELETE CASCADE,
                item        TEXT        NOT NULL,
                idx         INTEGER     NOT NULL,

                UNIQUE (id_combo, item, idx)
            ) STRICT;

            CREATE TABLE IF NOT EXISTS combo_trait (
                id_combo    TEXT        NOT NULL
                    REFERENCES combo (id)
                    ON DELETE CASCADE,
                trait       TEXT        NOT NULL,
                tier        INTEGER     NOT NULL,

                UNIQUE (id_combo, trait, tier)
            ) STRICT;

            COMMIT;
            """
        )
