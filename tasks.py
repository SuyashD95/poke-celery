from dataclasses import dataclass

import requests

import celery_conf

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


@celery_conf.app.task
def get_pokemon_details(name: str):
    """This task fetches information about specified pokemon from
    the PokeAPI service.

    Parameters
    ----------
    name: Name of the pokemon.

    Returns
    -------
    A dictionary containing two keys: "ok" to denote whether request
    has been successful in fetching data and "data" containing the
    JSON response returned from the API.
    """
    try:
        api_response = requests.get(f"{POKEAPI_BASE_URL}/pokemon/{name}")
    except requests.RequestException as exc:
        return {"ok": False, "data": {"reason": exc}}

    if api_response.status_code == 200:
        return {"ok": True, "data": api_response.json()}
    else:
        return {
            "ok": False,
            "data": {"reason": "failed", "status": api_response.status_code},
        }
