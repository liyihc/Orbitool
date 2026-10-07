# Workspace & Options

## Workspace

Almost all data lives in a workspace: an HDF5 file with the `.Orbitool`
extension. The **Workspace** menu has:

- **Load**, **Save**, **Save as**
- **Load config from workspace**, **Save config to workspace**

Workspaces are versioned. Loading a workspace written by an older Orbitool may
run a one-time migration; a workspace newer than your build will refuse to open.

### Saving large files

When processing large files, save the workspace to disk early to save memory:
**Workspace → Save as**. Until you click save, changes are written only to a
`*.orbt-temp` file; deleting it does not affect your original files.

## Options

**Settings** (the **Orbitool** menu) collects configuration that can be exported
with **Save config to workspace**:

- all checkbox, spin-box, text-box and radio-box states;
- formula settings — element minimum/maximum counts, charge, ppm;
- the ions used in the calibration stage;
- the mass list.

The **General** settings tab also holds the interface theme — **Follow system**,
**Light** or **Dark**.

**Load config from workspace** imports configuration from another workspace
file. The config can also be saved as an `.Orbitool` workspace and reloaded —
loading it restores all related widgets.
