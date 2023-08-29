import os, json, nibabel
import numpy as np
from threebrainpy.core import *
from threebrainpy.utils import *
from threebrainpy.templates import *
from threebrainpy.utils.temps import ensure_temporary_directory
from threebrainpy.utils.service import start_service
config_path="/Users/dipterix/Downloads/[rave-export]custom_3d_viewer-viewer/lib/threebrain_data-0/config_06f5470c28161afc90097abff28d0990.json"
config_path="/Users/dipterix/Downloads/[rave-export]custom_3d_viewer-viewer/lib/threebrain_data-0/config_multiple.json"
config_path="/var/folders/bs/n0q8wqv931g89ppshhgp2m2m0000gn/T/threebrainpy/test/lib/threebrain_data-0/config.json"
with open(config_path) as f:
    config = json.load(f)

# print(os.getcwd())
# mat = core.Mat44([1,0,0,0,0,0,-1,0,0,-1,0,0,0,0,0,1])
# print(mat)
# print(mat.to_json())
# brain = Brain("test", "/Users/dipterix/rave_data/raw_dir/PCC/rave-imaging/fs")
brain = Brain("test", "/Users/dipterix/rave_data/raw_dir/DemoSubject/rave-imaging/fs")
self = brain
# group = geom.GeomWrapper(brain=brain, name="gp")
# print(group)
# print(json.dumps(group, cls=utils.GeomEncoder, indent=4))
# templates.init_skeleton(dry_run = True)

config['groups'][0]
self.add_slice(slice_prefix = "brain.finalsurfs")
# self._groups['Volume - T1 (test)']._cached_items
self.add_surfaces(surface_type = "pial")
self.add_volume(volume_prefix = "aparc+aseg", is_continuous=False)
e = self.add_electrode_contact(number = 1, label = "LP", position = [20, 20, 20])

# e.get_position(space = "mni305", world = True)
self.add_electrodes("/Users/dipterix/rave_data/data_dir/demo/DemoSubject/rave/meta/electrodes.csv")
self.set_electrode_values("/Users/dipterix/rave_data/data_dir/demo/DemoSubject/rave/meta/electrodes.csv")
self.render(port = 12306)
# e = self.electrode_contacts[1]
# e.to_dict()

# volume = self._volumes['aparc_aseg']
# volume

# json.loads(json.dumps(self._groups, cls=GeomEncoder))

# print(self.storage.name)

# config['groups'][1]

# self.to_dict()

# input()
# contact = brain._electrode_contacts[1]
# self=brain._electrode_cmaps["LabelPrefix"]
# self.generate_colors()
# self.to_dict()