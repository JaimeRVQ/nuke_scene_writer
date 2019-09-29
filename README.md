# Nuke scene writer

A widget (Qtwidget) that looks through the whole Nuke scene and retrieves all ScanlineRender, RayRender and Write nodes. It then lets the user customize them before writing, without changing any of their original settings.

### Recommended way to launch
Install the module to your desired location and run:
```
from nuke_scene_writer import scene_writerUI
sr = scene_writerUI.SceneWriter()
```

### Look of the widget
![widget](https://user-images.githubusercontent.com/43014805/57075378-e9a9ad80-6ce6-11e9-9967-80c220ac7017.JPG)

This module has been tested successfully in **Nuke 11.1v1**
***

For more info: www.jaimervq.com