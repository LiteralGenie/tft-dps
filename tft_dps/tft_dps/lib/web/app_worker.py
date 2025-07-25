import asyncio
import multiprocessing as mp
import socket
from dataclasses import dataclass

import uvicorn
from uvicorn.config import logger

from tft_dps.lib.constants import PORT


@dataclass
class AppWorkerContext:
    req_queue: mp.Queue
    resp_queue: mp.Queue
    unit_info: dict
    item_info: dict
    trait_info: dict


def run_app_worker(*args, **kwargs):
    asyncio.run(_serve_app(*args, **kwargs))


async def _serve_app(
    req_queue: mp.Queue,
    resp_queue: mp.Queue,
    unit_info: dict,
    item_info: dict,
    trait_info: dict,
):
    __builtins__["APP_WORKER_CONTEXT"] = AppWorkerContext(
        req_queue, resp_queue, unit_info, item_info, trait_info
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
