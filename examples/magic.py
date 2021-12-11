# fp mss c

import logging
import numpy as np
import kubric as kb
from kubric.renderer.blender import Blender as KubricBlender
from kubric.core import traits as ktl

logging.basicConfig(level="INFO")  # < CRITICAL, ERROR, WARNING, INFO, DEBUG

# --- create scene and attach a renderer and simulator
scene = kb.Scene(resolution=(512, 512))
scene.frame_end = 2   # < numbers of frames to render
scene.frame_rate = 24  # < rendering framerate
# scene.step_rate = 240  # < simulation framerate
renderer = KubricBlender(scene)

# --- populate the scene with objects, lights, cameras
# units = meters for now

# ceiling
material = kb.FlatMaterial()
scene += kb.Cube(name="ceiling", scale=(7.5, 12.5, 0.01), position=(0, 0, 7.5))
scene += kb.DirectionalLight(name="sun", position=(0, 0, 0), look_at=(0, 0, 5), intensity=0.05)
scene.camera = kb.PerspectiveCamera(name="camera", look_at=(0, 0, 7.5), position=(0, 0, 0), focal_length=8)

# emitter grid
rng = np.random.default_rng()
for x in range(-2,3,2):
  for y in range(-4,5,2):
    material = kb.PrincipledBSDFMaterial(emission=kb.random_hue_color(rng=rng))
    sphere = kb.Sphere(scale=0.1, position=(x,y,7.0), material=material)
    scene += sphere

# --- renders the output
kb.as_path("output_mss").mkdir(exist_ok=True)
renderer.save_state("output_mss/mss.blend")
frames_dict = renderer.render()
kb.write_image_dict(frames_dict, "output_mss")
