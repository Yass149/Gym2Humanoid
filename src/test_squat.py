import math
import time

import mujoco
import mujoco.viewer

model = mujoco.MjModel.from_xml_path("models/humanoid.xml")
data = mujoco.MjData(model)

start_time = time.time()

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        t = time.time() - start_time

        amount = (math.sin(t * 2 - math.pi / 2) + 1) / 2

        pelvis = -0.30 * amount
        hip = -0.8 * amount
        knee = 1.5 * amount
        ankle = -0.7 * amount

        data.ctrl[:] = [
            pelvis,
            hip,
            knee,
            ankle,
            hip,
            knee,
            ankle,
        ]

        mujoco.mj_step(model, data)
        viewer.sync()

        time.sleep(model.opt.timestep)