"""The main file responsible for running invoking the tasks and the
workflows around them.
"""
from math import ceil
from time import sleep, time

from celery import chain, group
from celery.result import AsyncResult, GroupResult

import tasks


def print_pokemon_summaries_using_group(names: list[str]):
    """Print summarized information about the given pokemon
    specified in the list.

    Parameters
    ----------
    names: A list of pokemons.
    """
    pkmn_summary_result: GroupResult = group(
        [tasks.stringify_pokemon_summary.s(name=name) for name in names]
    ).apply_async()

    while not pkmn_summary_result.ready():
        print("Task to get all pokemon summaries is still in progress.")
        print(
            f"Currently, {pkmn_summary_result.completed_count()} out of {len(names)} tasks are completed.\n"
        )
        sleep(1)

    failed = 0
    for index, result in enumerate(pkmn_summary_result.join()):
        print(f"Pokemon Name: {names[index]}")
        if result:
            print(f"  {result}")
        else:
            print("  No information was found.")
            failed += 1
    print(
        f"\nSummary: total = {len(names)}, succeeded = {len(names) - failed}, failed = {failed}"
    )


def print_pokemon_summaries_using_chunked_groups(
    names: list[str], concurrency_count: int = 3
):
    """Print summarized information about the given pokemon
    specified in the list.

    NOTE: We split the list into N chunks which are executed in parallel
    using the group primitive.

    Parameters
    ----------
    names: A list of pokemons.
    concurrency_count: Number of threads/cores to be used. If using prefork worker, then
    it is recommended that concurrency_count should be utmost be equivalent to num of cores - 1.
    Exceeding this limit may lead to worker getting deadlocked.
    """
    chunks = ceil(len(names) / concurrency_count)

    pkmn_summary_result: GroupResult = group(
        tasks.stringify_pokemon_summary.chunks(zip(names), chunks)
    ).apply_async()

    while not pkmn_summary_result.ready():
        print("Task to get all pokemon summaries is still in progress.")
        print(
            f"Currently, {pkmn_summary_result.completed_count()} out of {len(names)} tasks are completed.\n"
        )
        sleep(1)

    failed = 0
    for index, result in enumerate(pkmn_summary_result.join()):
        print(f"Pokemon Name: {names[index]}")
        if result:
            print(f"  {result}")
        else:
            print("  No information was found.")
            failed += 1
    print(
        f"\nSummary: total = {len(names)}, succeeded = {len(names) - failed}, failed = {failed}"
    )


def print_pokemon_summaries_using_map(names: list[str]):
    """Print summarized information about specified pokemons.

    NOTE: This function will use map primitive and thus will
    be executed sequentially.

    Parameters
    ----------
    names: List of pokemon names.
    """
    pkmn_summary_result: AsyncResult = tasks.stringify_pokemon_summary.map(
        names
    ).apply_async()

    while not pkmn_summary_result.ready():
        print("Task to get pokemon summaries is still in progress.")
        sleep(1)

    failed = 0
    for index, result in enumerate(pkmn_summary_result.get()):
        print(f"Pokemon Name: {names[index]}")
        if result:
            print(f"  {result}")
        else:
            print("  No information was found.")
            failed += 1
    print(
        f"\nSummary: total = {len(names)}, succeeded = {len(names) - failed}, failed = {failed}"
    )


def print_pokemon_summaries_using_starmap(names: list[str]):
    """Print summarized information about specified pokemons.

    NOTE: This function will use starmap primitive and thus will
    be executed sequentially.

    Parameters
    ----------
    names: List of pokemon names.
    """
    pkmn_summary_result: AsyncResult = tasks.stringify_pokemon_summary.starmap(
        zip(names)
    ).apply_async()

    while not pkmn_summary_result.ready():
        print("Task to get pokemon summaries is still in progress.")
        sleep(1)

    failed = 0
    for index, result in enumerate(pkmn_summary_result.get()):
        print(f"Pokemon Name: {names[index]}")
        if result:
            print(f"  {result}")
        else:
            print("  No information was found.")
            failed += 1
    print(
        f"\nSummary: total = {len(names)}, succeeded = {len(names) - failed}, failed = {failed}"
    )


if __name__ == "__main__":
    pokemons = [
        "pikachu",
        "charizard",
        "lucario",
        "gengar",
        "dragonite",
        "sceptile",
        "psyduck",
        "blaziken",
        "blastoise",
        "onyx",
        "piplup",
        "mr-mime",
    ]

    start_time = time()
    print_pokemon_summaries_using_group(pokemons)
    end_time = time()
    print(f"Execution time (group): {end_time - start_time}")

    start_time = time()
    print_pokemon_summaries_using_map(pokemons)
    end_time = time()
    print(f"Execution time (map): {end_time - start_time}")

    start_time = time()
    print_pokemon_summaries_using_starmap(pokemons)
    end_time = time()
    print(f"Execution time (starmap): {end_time - start_time}")

    start_time = time()
    print_pokemon_summaries_using_chunked_groups(pokemons)
    end_time = time()
    print(f"Execution time (chunked groups): {end_time - start_time}")
