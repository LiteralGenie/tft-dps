import asyncio
import multiprocessing as mp
import socket
from dataclasses import dataclass

import uvicorn
from loguru import logger

from tft_dps.lib.constants import PORT


@dataclass
class AppWorkerContext:
    req_queue: mp.Queue
    resp_queue: mp.Queue
    queue_lock: asyncio.Lock
    unit_info: dict
    item_info: dict
    trait_info: dict
    notes: dict
    #
    trait_bits_by_unit_index: dict[int, list[int]]
    unit_info_by_index: dict
    item_info_by_index: dict


@logger.catch(reraise=True)
def run_app_worker(*args, **kwargs):
    asyncio.run(_serve_app(*args, **kwargs))


async def _serve_app(
    req_queue: mp.Queue,
    resp_queue: mp.Queue,
    unit_info: dict,
    item_info: dict,
    trait_info: dict,
    notes: dict,
):
    trait_bits_by_unit_index = dict()
    for unit in unit_info.values():
        trait_bits_by_unit_index[unit["index"]] = [
            trait_info[t]["num_bits"] for t in unit["info"]["traits"]
        ]

    unit_info_by_index = {u["index"]: u for u in unit_info.values()}
    item_info_by_index = {u["index"]: u for u in item_info.values()}

    __builtins__["APP_WORKER_CONTEXT"] = AppWorkerContext(
        req_queue=req_queue,
        resp_queue=resp_queue,
        queue_lock=asyncio.Lock(),
        unit_info=unit_info,
        item_info=item_info,
        trait_info=trait_info,
        notes=notes,
        trait_bits_by_unit_index=trait_bits_by_unit_index,
        unit_info_by_index=unit_info_by_index,
        item_info_by_index=item_info_by_index,
    )

    config = uvicorn.Config(
        "lib.web.app:app",
        port=PORT,
        host="0.0.0.0",
        workers=1,
    )

    server = uvicorn.Server(config)

    logger.info(f"Running web server at {config.host=} {config.port=}")
    sock = socket.socket(family=socket.AF_INET)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((config.host, config.port))

    await server.serve(sockets=[sock])
