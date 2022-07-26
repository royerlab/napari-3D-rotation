"""
This script creates a rotating 3D UMAP in napari viewer and record it as a video.
This is the script that was used to generate these videos:
https://twitter.com/loicaroyer/status/1551583552042455040?s=20&t=BBsuuAr8VVToiWaAs-ooaQ
https://twitter.com/loicaroyer/status/1551583560649256960?s=20&t=BBsuuAr8VVToiWaAs-ooaQ
for the publication in Nature Methods of cytoself:
https://www.nature.com/articles/s41592-022-01541-z
"""
from os.path import join
import napari
import numpy as np
import seaborn as sns
from napari_animation import Animation

# Load data
data_name = 'umap3D_coordinates'
umap3d_data = np.load(join('data', data_name + '.npy'))
umap_lab = np.load(join('data', 'label.npy'), allow_pickle=True)

# Make a color matrix for uniorg
greys = np.array(sns.color_palette('Greys', 100)[9] + (0.25,)).reshape(1, -1)
uniq_uniorg = np.unique(umap_lab[:, 0])
lab_color = np.zeros((len(umap_lab), 4))
cmap = sns.color_palette("hls", len(uniq_uniorg) - 1)
i = 0
for fmly in uniq_uniorg:
    if fmly == 'others':
        c = greys
    else:
        c = np.array(cmap[i] + (1,)).reshape(1, -1)
        i += 1
    ind = umap_lab[:, 0] == fmly
    lab_color[ind] = c


import matplotlib.pyplot as plt

plt.style.use('dark_background')
fig, ax = plt.subplots(1)
legendFig = plt.figure(figsize=(1.8, 2.4))
plist = []
i = 0
leg_names = []
for fmly in uniq_uniorg:
    fmly = fmly.replace('_', ' ')
    if fmly != 'others':
        plist.append(
            ax.scatter(i, i, c=np.array(cmap[i] + (1,)).reshape(1, -1), s=40, label=uniq_uniorg[i])
        )
        i += 1
        leg_names.append(fmly)
plist.append(
    ax.scatter(
        i + 1, i + 1, c=np.array(sns.color_palette('Greys', 100)[9] + (1,)).reshape(1, -1), s=40, label='others'
    )
)
leg_names.append('others')
legendFig.legend(plist, leg_names, loc='center', frameon=False)
legendFig.savefig('legend_uniorg_transparent.png', dpi=300, transparent=True)


viewer = napari.view_points(
    umap3d_data,
    scale=(100,) * 3,
    shading='spherical',
    size=0.06,
    name='umap3d_nb1000',
    edge_width=0,
    opacity=0.9,
    face_color=lab_color,
    ndisplay=3,
)
viewer.window.resize(1300, 1000)



# Record animation
animation = Animation(viewer)
viewer.dims.ndisplay = 3

fps = 60
nb_steps = 3*fps
viewer.reset_view()
original_zoom = viewer.camera.zoom

angle = 0
# viewer.camera.zoom = 0.1
# viewer.camera.angles = (0.0, angle, 90.0)
# animation.capture_keyframe()

viewer.camera.zoom = 0.6
for i in range(2):
    viewer.camera.angles = (0.0, angle, 90.0)
    animation.capture_keyframe(steps=nb_steps)
    angle += 180

animation.animate(f'3d_umap.gif', canvas_only=True, fps=fps)
