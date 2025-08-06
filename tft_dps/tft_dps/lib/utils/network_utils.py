import gzip
from io import BytesIO
from typing import TYPE_CHECKING

from bitarray import bitarray
from bitarray.util import ba2int

from tft_dps.lib.web.job_worker import SimulateRequest

if TYPE_CHECKING:
    from tft_dps.lib.web.app_worker import AppWorkerContext


def bytesToIntBe(bs: bytearray):
    return int.from_bytes(bs, "big")


def unpack_sim_id_array(data: bytearray) -> dict:
    ID_COUNT_BYTES = 2
    ID_BYTES = 5

    byteOffset = 0

    def take(n: int):
        nonlocal byteOffset

        d = data[byteOffset : byteOffset + n]
        assert len(d) == n

        byteOffset += n
        return d

    numIds = bytesToIntBe(take(ID_COUNT_BYTES))

    period = bytesToIntBe(take(1)) / 8

    ids = []
    for idx in range(0, numIds):
        id = bitarray(take(ID_BYTES))
        ids.append(id)

    return dict(ids=ids, period=period)


def unpack_sim_id(id: bitarray, trait_bits_by_unit: dict[int, list[int]]) -> dict:
    try:
        unit_index = ba2int(id[0:7])
        stars = ba2int(id[7:9])
        item_indices = [ba2int(id[9:15]), ba2int(id[15:21]), ba2int(id[21:27])]

        rem = id[27:40]
        bits_per_trait = trait_bits_by_unit[unit_index]
        traits = []
        for n in bits_per_trait:
            assert len(rem) >= n
            traits.append(ba2int(rem[-n:]))
            rem = rem[:-n]

        return dict(
            unit=unit_index,
            stars=stars,
            items=item_indices,
            traits=traits,
        )

    except:
        print(id)
        raise


def sim_id_to_sim_request(id: bitarray, context: "AppWorkerContext"):
    raw = unpack_sim_id(bitarray(id), context.trait_bits_by_unit_index)

    id_unit = context.unit_info_by_index[raw["unit"]]["info"]["id"]
    items = [
        context.item_info_by_index[itemId]["id"]
        for itemId in raw["items"]
        if itemId > 0
    ]
    traits = context.unit_info[id_unit]["info"]["traits"]

    req = SimulateRequest(
        type="simulate_request",
        id_unit=id_unit,
        stars=raw["stars"],
        items=items,
        traits={trait: tier for trait, tier in zip(traits, raw["traits"])},
    )
    return req


def decompress_gzip(d: bytes, max_bytes: int, chunk_size=1024):
    file = gzip.open(BytesIO(d))

    result = bytearray()
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break

        result.extend(chunk)
        if len(result) > max_bytes:
            raise Exception()

    return result
