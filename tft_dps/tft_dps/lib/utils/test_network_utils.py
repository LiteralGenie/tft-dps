from bitarray import bitarray

from tft_dps.lib.utils.network_utils import unpack_sim_id


def test_unpacking():
    id = bitarray("0001001_11_010110_010110_010110_0000000000_010")
    unpacked = unpack_sim_id(id, {9: [3]})

    assert unpacked["unit"] == 9
    assert unpacked["stars"] == 3
    assert unpacked["items"] == [22, 22, 22]
    assert unpacked["traits"] == [2]
