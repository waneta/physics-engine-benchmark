import importlib.util
import os
import sys

print("UID", os.getuid(), "Python", sys.version, flush=True)
for name in ["numpy", "mujoco", "matplotlib", "omni"]:
    print(name, bool(importlib.util.find_spec(name)), flush=True)
from isaacsim import SimulationApp

app = SimulationApp(
    {"headless": True, "hide_ui": True, "disable_viewport_updates": True, "width": 64, "height": 64}
)
print("ISAAC_PHYSX_READY", flush=True)
app.close()
