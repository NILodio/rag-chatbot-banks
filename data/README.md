# Data Directory
This folder contains all the datasets required for the project, including training, validation, and testing data. If you're using DVC (Data Version Control), it will track and manage the datasets stored here.

## Structure
- Training Data: Place your training datasets here.
- Validation Data: Use this section for validation sets.
- Test Data: Store testing datasets here.

### DVC Integration
If you're managing datasets with DVC, ensure that this folder is linked to the DVC pipeline. The .dvc files should point to this directory.

Key Commands
Add Data to DVC:
```
dvc add ./data
```

Pull Data from DVC:
```
dvc pull
```

Push Data to Remote:
```
dvc push
```

Note: Ensure that the dvc.yaml and .dvc files are correctly set up to track the changes in this folder.