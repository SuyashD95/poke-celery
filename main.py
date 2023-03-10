"""The main file responsible for running invoking the tasks and the
workflows around them.
"""
from celery import chain
from celery.result import AsyncResult

import tasks


def print_pokemon_summary(name: str):
    """Prints summarized information about the given pokemon.

    Parameters
    ----------
    name: Name of pokemon
    """
    pokemon_summary_flow = chain(
        tasks.get_pokemon_details.s(name) | tasks.extract_pokemon_summary.s()
    )
    task_result: AsyncResult = pokemon_summary_flow()

    while not task_result.ready():
        print("Task series is still in progress")
    print("The series of tasks are now completed.")

    task_data = task_result.get()
    if task_data:
        print(
            f"My name is {task_data['name'].title()} and I am a "
            f"{task_data['primary_type'].upper()} type Pokemon. My base XP is "
            f"{task_data['base_xp']}."
        )
    else:
        print(f"Cannot retrive information about {name}.")


if __name__ == "__main__":
    print_pokemon_summary("pikachu")
