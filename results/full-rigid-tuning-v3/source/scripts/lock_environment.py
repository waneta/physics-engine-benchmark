"""Freeze only the installed dependency closure of the selected benchmark backend."""

import argparse
import importlib.metadata
from collections import deque

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("engine", choices=("warp", "genesis", "newton"))
args = parser.parse_args()
roots = (
    ["physics-engine-benchmark", "mujoco-warp", "warp-lang"]
    if args.engine == "warp"
    else ["physics-engine-benchmark", "genesis-world", "torch"]
)
if args.engine == "newton":
    roots = ["physics-engine-benchmark", "newton", "mujoco-warp", "warp-lang", "scipy"]
pending = deque((name, frozenset()) for name in roots)
visited, installed = set(), {}
while pending:
    name, extras = pending.popleft()
    name = canonicalize_name(name)
    if (name, extras) in visited:
        continue
    visited.add((name, extras))
    distribution = importlib.metadata.distribution(name)
    installed[name] = distribution.version
    for spec in distribution.requires or []:
        requirement = Requirement(spec)
        if requirement.marker and not any(
            requirement.marker.evaluate({"extra": extra}) for extra in ("", *extras)
        ):
            continue
        found = importlib.metadata.version(requirement.name)
        if requirement.specifier and not requirement.specifier.contains(found, prereleases=True):
            raise RuntimeError(f"Incompatible installed dependency: {requirement}; found {found}")
        pending.append((requirement.name, frozenset(requirement.extras)))
print("# Installed dependency closure; Linux x86_64 / Python 3.11.")
print("# Regenerate with the selected backend environment and scripts/lock_environment.py.")
print("-e .")
for name, version in sorted(installed.items()):
    if name != "physics-engine-benchmark":
        print(f"{name}=={version}")
