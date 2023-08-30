# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

import json
import os
from pathlib import Path
import shutil
from typing import Union

from ansys.optislang.core import Optislang
from ansys.optislang.core.nodes import System
from ansys.solutions.{{ cookiecutter.__solution_name_slug }}.model.optislang.install import get_available_optislang_installations


def dump_project_state(project_file: Path, project_state_file: Path) -> None:
    """Start PyOptiSLang and dump project state file."""

    versions = get_available_optislang_installations()
    if len(versions) == 0:
        raise Exception("To run PyOptiSLang, you must have access to a licensed copy of optiSLang. The first supported version of optiSLang is 2023 R1.")

    working_directory = project_file.parent
    temporary_directory = working_directory / "extract_project_tree.tmp"

    if not os.path.exists(temporary_directory):
        os.makedirs(temporary_directory)
    else:
        shutil.rmtree(temporary_directory)
        os.makedirs(temporary_directory)

    shutil.copy(project_file, temporary_directory / project_file.name)

    osl = Optislang(
        project_path=temporary_directory / project_file.name,
        loglevel="INFO",
        reset=True,
        shutdown_on_finished=True,
        dump_project_state=project_state_file,
        ini_timeout=300,
    )

    osl.dispose()

    if not project_state_file.exists():
        raise Exception("The project state file has not been generated.")

    shutil.rmtree(temporary_directory)


def get_project_tree(project_state_file: Path) -> dict:
    """Read the project tree of an optiSLang project."""

    with open(Path(project_state_file).absolute()) as f:
        response = json.load(f)

    # Initialize project tree with default steps.
    project_tree = [
        {
            "key": "problem_setup_step",
            "text": "Problem Setup",
            "depth": 0,
            "uid": None,
            "type": None,
            "kind": None,
            "is_root": False,
        },
    ]

    root_system = response["projects"][0]["system"]

    # Declare root.
    project_tree.extend(
        [
            {
                "key": f'{root_system["name"].lower()}_{root_system["uid"]}',
                "text": f'{root_system["name"]} (root)',
                "depth": 0,
                "uid": root_system["uid"],
                "type": root_system["type"],
                "kind": root_system["kind"],
                "is_root": True,
            },
        ]
    )

    # Declare nodes.
    for node in root_system["nodes"]:
        depth = 1
        project_tree.append(
            {
                "key": f'{node["name"].lower()}_{node["uid"]}',
                "text": node["name"],
                "depth": depth,
                "uid": node["uid"],
                "type": node["type"],
                "kind": node["kind"],
                "is_root": False,
            }
        )
        if "nodes" in node.keys():
            project_tree.extend(_get_node_tree(node["nodes"], depth=depth))

    return {"project_tree": project_tree}


def _get_node_tree(data: Union[list, dict], depth: int = 1) -> list:

    if isinstance(data, dict):
        node_tree = []
        depth += 1
        node_tree.append(
            {
                "key": f'{data["name"].lower()}_{data["uid"]}',
                "text": data["name"],
                "depth": depth,
                "uid": data["uid"],
                "type": data["type"],
                "kind": data["kind"],
                "is_root": False,
            }
        )
        if "nodes" in data.keys():
            node_tree.extend(_get_node_tree(item, depth=1))
        return node_tree
    elif isinstance(data, list):
        node_tree = []
        for item in data:
            node_tree.extend(_get_node_tree(item, depth=depth))
        return node_tree


def get_step_list(project_tree: dict) -> list:
    """Return a list of steps to feed the AnsysDashTreeview component."""

    return project_tree["project_tree"]


def get_node_list(project_tree: dict) -> list:
    """Return the list of nodes in the optiSLang project file."""

    return [
        node_info
        for node_info in project_tree["project_tree"]
        if node_info["key"] not in ["problem_setup_step"]
    ]


def get_node_by_uid(osl: Optislang, actor_uid: str):
    """Get node by walking throughout the root system recursively."""

    def recursive_search(nodes, actor_uid):

        for node in nodes:
            if node.uid == actor_uid:
                return node
            if isinstance(node, System):
                result = recursive_search(node.get_nodes(), actor_uid)
                if result:
                    return result

    for node in osl.project.root_system.get_nodes():
        if node.uid == actor_uid:
            return node
        if isinstance(node, System):
            result = recursive_search(node.get_nodes(), actor_uid)
            if result:
                return result


def get_node_hids(osl: Optislang, actor_uid: str) -> list:
    """Return the hirearchical ID (hid) of the actor."""

    actor_states = osl.get_osl_server().get_actor_states(actor_uid)

    if "states" in actor_states.keys():
        if len(actor_states["states"]):
            return [state["hid"] for state in actor_states["states"]]
    else:
        return []
