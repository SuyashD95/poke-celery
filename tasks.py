from typing import Any, NotRequired, Optional, TypedDict, cast

import requests

import celery_conf


class APIError(TypedDict):
    """A dictionary used for specifying possible errors in APIResponse dictionary."""

    reason: str
    status: NotRequired[int]


class APIResponse(TypedDict):
    """A dictionary used for specifying response from APIs."""

    ok: bool
    data: dict[str, Any] | APIError


class PokemonSummary(TypedDict):
    """A dictionary containing following details about pokemon: name, base XP & primary type."""

    name: str
    base_xp: int
    primary_type: str


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


@celery_conf.app.task
def extract_pokemon_summary(api_response: APIResponse) -> Optional[PokemonSummary]:
    """This task extracts the name, primary type and base XP from the provided API response.

    Parameters
    ----------
    api_response: JSON response received from API.

    Returns
    -------
    A dictionary containing name, type and base experience of a pokemon whose data
    was provided.
    """
    if api_response["ok"]:
        json_data = cast(dict[str, Any], api_response["data"])
        return {
            "name": json_data["name"],
            "base_xp": json_data["base_experience"],
            "primary_type": json_data["types"][0]["type"]["name"],
        }
