import httpx

from .config import settings

url: str


def setup():
    # setup nas url
    global url
    url = "http://" + settings.nas_ip + ":" + \
        settings.nas_port + "/cgi-bin/filemanager/utilRequest.cgi"


def read_folder(path: str):
    """
    Read subfolder inside inward folder
    """
    params = {
        "func": "get_tree",
        "sid": settings.nas_sid,
        "is_iso": 0,
        "node": path
    }
    try:
        r = httpx.get(url, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    assets = []
    for item in response:
        assets.append(item['text'])
    return assets


def read_inward(base_path):
    """
    Read assets inside inward folder
    """
    params = {
        "func": "get_tree",
        "sid": settings.nas_sid,
        "is_iso": 0,
        "node": base_path
    }
    try:
        r = httpx.get(url, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    if isinstance(response, dict):
        raise Exception("No records found")

    assets = []
    for item in response:
        path = base_path + "/" + item['text']
        path_assets = read_folder(path)
        assets += path_assets

    # remove duplicates
    assets = set(assets)
    assets = list(assets)

    return assets


def read_assets(date: str, inward: str):
    """
    Reas assets for specified date and inward
    """

    # initialize
    setup()
    base_path = settings.nas_prefix + "/" + date

    params = {
        "func": "get_tree",
        "sid": settings.nas_sid,
        "is_iso": 0,
        "node": base_path
    }
    try:
        r = httpx.get(url, params=params)
        # print(f"Sending request : {r.url}")
    except httpx.HTTPError as exc:
        raise Exception(
            f"An error occurred while requesting {exc.request.url!r}.")

    response = r.json()
    if isinstance(response, dict):
        raise Exception("No records found")

    # identify inward folder
    for item in response:
        folder = item['text']
        tokens = folder.split("-", 1)
        if tokens[0] == inward:
            base_path = base_path + "/" + folder
            break

    return read_inward(base_path)
