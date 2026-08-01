# Session 5 Data Entry Point

The project has one canonical data location: the repository-level `data/` directory. It contains the DVC pointer for the original ENDES archives, the derived CSV managed by the DVC pipeline, and the metadata contract used by every script.

This folder is kept only to mirror the Session 5 layout used in the course brief. It deliberately contains no second dataset, no copied CSV, and no duplicate DVC pointer. From the repository root, retrieve the versioned data with:

```powershell
dvc pull
```

Read [`../../data/README.md`](../../data/README.md) for the data contract and [`../../data/DVC_ACCESS.md`](../../data/DVC_ACCESS.md) for the local Google Drive service-account setup.
