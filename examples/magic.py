# fp mss c

import logging
import numpy as np
import kubric as kb
from kubric.simulator import PyBullet
from kubric.renderer import Blender

logging.basicConfig(level="INFO")  # < CRITICAL, ERROR, WARNING, INFO, DEBUG

# arguments

CAMERA_RANGE = [[-10, -10, 1], [10, 10, 3]]

parser = kb.ArgumentParser()
# Configuration for the camera
parser.add_argument("--camera", choices=["clevr", "katr", "random", "linear_movement"], default="clevr")
parser.add_argument("--max_camera_movement", type=float, default=4.0)

parser.add_argument("--no_save_state", dest="save_state", action="store_false")
parser.add_argument("--save_state", dest="save_state", action="store_true")
parser.set_defaults(save_state=True, frame_end=24, frame_rate=12, width=512, height=512)
FLAGS = parser.parse_args()


# --- create scene and attach a renderer and simulator
scene, rng, output_dir, scratch_dir = kb.setup(FLAGS)
simulator = PyBullet(scene, scratch_dir)
renderer = Blender(scene, scratch_dir, use_denoising=True, adaptive_sampling=False)

logging.info("Creating a large gray ceiling...")

# --- populate the scene with objects, lights, cameras
# units = meters for now

# ceiling
ceiling_material = kb.PrincipledBSDFMaterial(color=kb.Color.from_name("gray"),
                                           roughness=1., specular=0.)
scene += kb.Cube(name="ceiling", scale=(7.5, 12.5, 0.01), position=(0, 0, 7.5),
                  material=ceiling_material, 
                # friction=1.0, restitution=0,
                  static=True, background=True)

scene_metadata = {}
dome = kb.assets.utils.add_hdri_dome(hdri_source, scene, background_hdri)
renderer._set_ambient_light_hdri(background_hdri.filename)
scene_metadata["background"] = kb.as_path(background_hdri.filename).stem

# scene += kb.DirectionalLight(name="sun", position=(0, 0, 0), look_at=(0, 0, 5), intensity=0.05)
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
