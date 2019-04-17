import globals as G


def get_info(modinfo: str) -> str:
    if modinfo.count("|") == 0:
        return "any"
    modversioninfo = modinfo.split("|")[1]
    return modversioninfo


def is_valid(modinfo: str, versioninfo: str) -> bool:
    modc = get_info(modinfo)
    if modc == "any" or modc == versioninfo:
        return True
    return False

