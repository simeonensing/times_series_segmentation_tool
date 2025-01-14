# MindAble Biosignal Time Series Segmentation Software

## Overview

This software is designed for **segmenting biosignal time series data into intervals, then labelling said intervals**. It supports the following file formats:

- `.fif`
- `.edf`
- `.bdf`
- `.gdf`
- `.set`

### Key Features
- Segmentation of time series data into intervals.
- Labeling cropped intervals.

---

## Installation

### Prerequisites

Ensure you have the following installed:

1. **Conda**: Install either [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/).
2. **Git** (optional): Required if you want to clone this repository instead of downloading the ZIP.

---

### Setup Instructions

#### 1. Download the Repository

- **Option A: Clone the Repository**

  - **Conda Terminal (Windows)**:  
    We recommend using the **Conda terminal** (Anaconda Prompt or Miniconda Prompt) on Windows for managing environments and running Conda commands.
    ```bash
    git clone https://github.com/simeonensing/times_series_segmentation_tool.git
    cd times_series_segmentation_tool
    ```

  - **Bash/Unix-like Terminals (Linux/macOS)**:
    ```bash
    git clone https://github.com/simeonensing/times_series_segmentation_tool.git
    cd times_series_segmentation_tool
    ```

  - **PowerShell (Windows)**:
    ```powershell
    git clone https://github.com/simeonensing/times_series_segmentation_tool.git
    Set-Location -Path times_series_segmentation_tool
    ```

- **Option B: Download as ZIP**

  1. Download the ZIP file from GitHub.
  2. Extract the ZIP file to a directory of your choice.
  3. Open a terminal and navigate to the extracted folder:
  
     - **Conda Terminal (Windows)**:
       ```bash
       cd path\to\extracted\folder
       ```

     - **Bash/Unix-like Terminals (Linux/macOS)**:
       ```bash
       cd path/to/extracted/folder
       ```

     - **PowerShell (Windows)**:
       ```powershell
       Set-Location -Path "path\to\extracted\folder"
       ```

#### 2. Create the Conda Environment

1. Ensure the `environment.yml` file is in the root directory.
2. Create the environment:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the environment:
   - **Conda Terminal (Windows)**:
     ```bash
     conda activate segmentation_tool_env
     ```
   - **Bash/Unix-like Terminals (Linux/macOS)**:
     ```bash
     conda activate segmentation_tool_env
     ```
   - **PowerShell (Windows)**:
     ```powershell
     conda activate segmentation_tool_env
     ```

4. Verify installation by listing installed packages:
   ```bash
   conda list
   ```

---

## Usage

### Running the Software

1. Activate the Conda environment (if not already activated):

   - **Conda Terminal (Windows)**:
     ```bash
     conda activate segmentation_tool_env
     ```

   - **Bash/Unix-like Terminals (Linux/macOS)**:
     ```bash
     conda activate segmentation_tool_env
     ```

   - **PowerShell (Windows)**:
     ```powershell
     conda activate segmentation_tool_env
     ```

2. Run the main script:
   ```bash
   python main.py 
   ```

---

## Updating the Environment

If new dependencies are added to the `environment.yml` file, update your environment:
```bash
conda env update -f environment.yml --prune
```

---

## Troubleshooting

### Common Issues

1. **Environment Already Exists**:  
   Remove the existing environment:
   ```bash
   conda remove --name <environment-name> --all
   ```

---

## Additional Resources

- [Conda Documentation](https://docs.conda.io/en/latest/)
- [Managing Conda Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
