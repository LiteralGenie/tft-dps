import gzip
from io import BytesIO

from bitarray import bitarray
from bitarray.util import ba2int


def bytesToIntBe(bs: bytearray):
    return int.from_bytes(bs, "big")


def decodePackedIdArray(data: bytearray) -> list[bitarray]:
    ID_COUNT_BYTES = 2
    ID_SIZE_BYTES = 1

    byteOffset = 0

    def take(n: int):
        nonlocal byteOffset

        d = data[byteOffset : byteOffset + n]
        assert len(d) == n

        byteOffset += n
        return d

    numIds = bytesToIntBe(take(ID_COUNT_BYTES))

    ids = []
    for idx in range(0, numIds):
        idLength = bytesToIntBe(take(ID_SIZE_BYTES))
        idBytes = take(idLength)
        id = bitarray(idBytes)
        ids.append(id)

    return ids


def decodePackedId(id: bitarray, trait_bits_by_unit: dict[int, list[int]]) -> dict:
    try:
        bit_offset = 0

        def take(n: int):
            nonlocal bit_offset
            d = id[bit_offset : bit_offset + n]
            bit_offset += n
            return d

        unit = ba2int(take(7))
        stars = ba2int(take(2))
        items = [ba2int(take(6)), ba2int(take(6)), ba2int(take(6))]

        num_trait_bits = trait_bits_by_unit[unit]
        # rem_bits = len(id) - bit_offset
        # assert rem_bits == sum(num_trait_bits), (rem_bits, sum(num_trait_bits), id)
        traits = [ba2int(take(n)) for n in num_trait_bits]

        print(
            dict(
                unit=unit,
                stars=stars,
                items=items,
                traits=traits,
            )
        )

        return dict(
            unit=unit,
            stars=stars,
            items=items,
            traits=traits,
        )
    except:
        print(id)
        raise


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
