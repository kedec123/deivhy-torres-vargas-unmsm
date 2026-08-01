# Google Drive DVC Access

The repository-level remote is configured to the project Drive folder, but no credential is stored in Git. Google may block DVC's shared default OAuth client, so the supported project setup is a **service account** with access only to this folder.

## One-time owner setup

1. In Google Cloud Console, create a project and enable the Google Drive API.
2. Create a service account and download its JSON key. Store the key outside this repository.
3. Share the project DVC Drive folder with the service account email as **Editor**.
4. Keep the key private. Do not email it, add it to GitHub, paste it into a notebook, or put it in `data/`.

## Configure a local clone

With DVC installed, set the local-only credentials. Replace the example path with the private location of the downloaded JSON key.

```powershell
dvc remote modify storage --local gdrive_use_service_account true
dvc remote modify storage --local gdrive_service_account_json_file_path "C:\Users\your-user\secrets\unmsm-endes-dvc.json"
dvc pull
```

For the repository owner, `dvc push` sends the current DVC cache to the shared folder after the same local configuration. The `--local` flag stores the private path in `.dvc/config.local`, which is ignored by Git.

## Verification

After the owner runs `dvc push`, a collaborator can test a clean clone with `dvc pull` and `dvc status`. A successful pull is the required evidence that the remote, permissions, and DVC pointers work together. Until that test succeeds, the Git repository is complete in code and metadata but the remote-data transfer remains pending.
