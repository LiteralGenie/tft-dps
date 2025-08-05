import sqlite3
from pathlib import Path
from typing import Any, TypeAlias

from tft_dps.lib.utils.misc_utils import to_path
from tft_dps.lib.web.job_worker import SimulateRequest

Db: TypeAlias = sqlite3.Connection


class DbWrapper:
    def __init__(
        self,
        fp: Path | str,
        missing_ok=False,
        readonly=False,
        foreign_keys=True,
    ):
        assert not (missing_ok and readonly)

        self.foreign_keys = foreign_keys
        self.readonly = readonly

        self.fp = to_path(fp)
        if not missing_ok and not self.fp.exists():
            raise Exception(f"Database file does not exist {self.fp.absolute()}")

        if not self.readonly:
            with self.connect() as conn:
                self.init_schema(conn)

    def connect(self):
        db = sqlite3.connect(self.fp)

        db.row_factory = sqlite3.Row

        db.execute("PRAGMA journal_mode=WAL")

        if self.readonly:
            db.execute("PRAGMA query_only=true")

        if self.foreign_keys:
            db.execute("PRAGMA foreign_keys = ON")

        return db

    def init_schema(self, conn: Db):
        pass

    def execute_and_commit(self, query: str, args: list | None):
        db = self.connect()
        db.execute(query, args or [])
        db.commit()

    def select_single_key(self, key: str, query: str, args: list | None) -> Any | None:
        db = self.connect()
        r = db.execute(query, args or []).fetchone()
        if r:
            return r[key]
        else:
            return None


def dbid_from_request(req: SimulateRequest):
    parts = [req["id_unit"]]

    parts.append(str(req["stars"]))

    parts.extend(sorted(req["items"]))

    parts.extend(
        [f"{k}|{v}" for k, v in sorted(req["traits"].items(), key=lambda kv: kv[0])]
    )

    return "_".join(parts)
