# Setting Up the Environment with Conda

This guide explains how to set up your development environment using Conda and the provided `environment.yaml` file. Conda is a package manager that simplifies the management of dependencies and virtual environments.

## Prerequisites

Before proceeding, ensure you have the following installed:

1. **Conda**: Install either [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/).
2. **Git** (optional): Required if you need to clone this repository.

## Steps to Set Up the Environment

### 1. Clone the Repository (Optional)

If this project is in a Git repository, clone it using the following command:

```bash
git clone https://github.com/simeonensing/times_series_segmentation_tool.git
cd <repository-folder>
```

### 2. Locate the `environment.yaml` File

Ensure the `environment.yaml` file is in the root directory of the project. This file contains all the dependencies and configurations needed for the environment.

### 3. Create the Conda Environment

Run the following command to create the environment:

```bash
conda env create -f environment.yaml
```

This command reads the `environment.yaml` file and installs the required dependencies into a new environment.

### 4. Activate the Environment

Once the environment is created, activate it using:

```bash
conda activate <environment-name>
```

Replace `<environment-name>` with the name specified in the `name` field of the `environment.yaml` file. You can also find the environment name in the `environment.yaml` file under the `name` key.

### 5. Verify the Installation

Check that the required dependencies are installed by running:

```bash
conda list
```

You can also run any specific commands or scripts to ensure the setup is complete (e.g., `python --version` or `pytest` for running tests).

### 6. Deactivating the Environment

To deactivate the environment after use, run:

```bash
conda deactivate
```

## Updating the Environment

If the `environment.yaml` file changes (e.g., new dependencies are added), update your environment with:

```bash
conda env update -f environment.yaml --prune
```

The `--prune` flag removes dependencies that are no longer required.

## Removing the Environment

If you no longer need the environment, remove it with:

```bash
conda remove --name <environment-name> --all
```

Replace `<environment-name>` with the name of the environment you want to delete.

## Common Issues

1. **"Environment already exists" Error**:
   - If the environment already exists, you can remove it first using:
     ```bash
     conda remove --name <environment-name> --all
     ```

2. **Package Conflicts**:
   - Ensure your `environment.yaml` specifies compatible versions of packages. Refer to the documentation of individual packages for compatibility details.

## Example `environment.yaml`

Here is an example of what the `environment.yaml` file might look like:

```yaml
name: my_project_env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy
  - pandas
  - matplotlib
  - scipy
  - scikit-learn
  - pip:
      - some-python-package
```

## Additional Resources

- [Conda Documentation](https://docs.conda.io/en/latest/)
- [Managing Conda Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

