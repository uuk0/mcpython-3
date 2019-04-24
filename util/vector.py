"""
functions around vectors
"""


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    if not position: return None
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return x, y, z


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    if not position: return
    x, y, z = normalize(position)
    x, y, z = x // 16, y // 16, z // 16
    return x, z


def relativise(position, chunk, check=True):
    if check and sectorize(position) != chunk:
        raise ValueError("can't relativise an position to an chunk where the position is not in")
    return position[0] - (chunk[0] * 16), position[1], position[2] - (chunk[1] * 16)


def relativise_in_chunk(position):
    return relativise(position, sectorize(position), check=False)


def unrelative_position(position, chunk):
    return position[0] + chunk[0] * 16, position[1], position[2] + chunk[1] * 16

