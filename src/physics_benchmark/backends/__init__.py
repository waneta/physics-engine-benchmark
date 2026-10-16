"""Optional engines are imported only when selected, in independent environments."""

ENGINES = ("mujoco-cpu", "mujoco-warp", "genesis", "physx")


def load_backend(engine):
    from importlib import import_module

    modules = {"mujoco-warp": "warp", "genesis": "genesis", "physx": "physx"}
    if engine not in modules:
        raise ValueError(f"Unknown optional engine: {engine}")
    return import_module(f"physics_benchmark.backends.{modules[engine]}")
