# Kurotori Avatar Exporter

## Overview

Kurotori Avatar Exporter is a Blender add-on designed for efficiently exporting avatars (character models) in FBX format. It is tailored for a specific workflow (kurotori workflow) and allows managing multiple export settings (jobs) to perform exports like batch processing.

Requires Blender 4.2.0 or later.

## Key Features

*   **Export Job Management:**
    *   Add, delete, and rename multiple export settings (jobs).
    *   Specify an output directory for each job.
*   **Export Target Configuration:**
    *   Specify the base armature object.
    *   Select multiple mesh objects to include in the export.
    *   Select and list bones to include in the export (only specified bones will be exported with `use_deform=True`).
*   **Export Options:**
    *   Option to reset all shape key values to 0 upon export.
*   **FBX Export Execution:**
    *   Exports FBX files based on the configured settings.
    *   The following options are automatically applied:
        *   Export only visible objects
        *   Object types: Armature, Mesh
        *   Apply Scale: FBX\_SCALE\_ALL
        *   Deform Bones Only
        *   Do not add leaf bones
        *   Do not export animation

## Installation

1.  Open Blender, go to `Edit` > `Preferences` > `Add-ons`.
2.  Click `Get Extensions`, then open the `Repositories` tab.
3.  Click the `[+]` button and select `Add Remote Repository`.
4.  Paste the following URL:
    ```
    https://kurotori4423.github.io/AvatarExporter/index.json
    ```
5.  Click `OK` to add the repository.
6.  Select the added repository and click `Update Extensions` (may not be necessary the first time).
7.  Find "Kurotori Avatar Exporter" (e.g., in the `Community` tab) and click the `Install` button.
8.  After installation, enable the checkbox next to the add-on name.

## Usage

1.  **Show Panel:** Open the 3D Viewport sidebar (N key) and select the "Avatar Exporter" tab.
2.  **Add Job:** Click the `Add Job` button to create a new export job.
3.  **Job Settings:**
    *   Change the job name in the text box next to the job name.
    *   `Output Dir`: Specify the output folder for the FBX file. The filename will be automatically generated based on the job name (`Job Name.fbx`).
    *   `Reset ShapeKey`: If checked, all shape key values of the mesh will be set to 0 upon export.
    *   `Armature`: Select the base armature object for the export.
    *   **Include Bone List:**
        *   Displayed when `Armature` is set.
        *   Select the armature in Pose Mode or Edit Mode, select the bones you want to include, and click the `Set Active Bone` button. The selected bones will be added to the list.
        *   Click the `Clear List` button to empty the list.
        *   Only bones included in the list will be exported as deform bones.
    *   **Export Mesh List:**
        *   Select the mesh objects you want to export in the 3D View and click the `Set Export Mesh` button. The selected meshes will be added to the list.
4.  **Execute Export:**
    *   Once settings are complete, click the `Export` (export icon) button to the right of the job name.
    *   The file will be exported to the specified output directory with the name `Job Name.fbx`.

## License

MIT License

## Author

kurotori4423@gmail.com
