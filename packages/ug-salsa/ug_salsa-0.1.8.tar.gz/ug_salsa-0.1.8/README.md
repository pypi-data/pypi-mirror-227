# SALSA - System Analytics Library for Substrate Analysis

SALSA is a Python package designed to allow for modular, customizable analyses of different substrates/optics data to be outputted as plots and reports. It includes functionalities for data objects, visualization, and metric aggregation with substrates. This document provides instructions for installing SALSA along with its dependencies.

## Installation

Before you proceed with the installation of SALSA, ensure that you have Python 3.8 or later installed on your system.

### Step 1: Install SALSA

Open your terminal or command prompt and execute the following command to install SALSA using pip:

```bash
pip install -i https://test.pypi.org/simple/ salsa
```

### Dependencies
SALSA's dependencies are listed in the pyproject.toml file under the [tool.poetry.dependencies] section, and are automatically installed upon installation of SALSA. For reference, here are SALSA's utilized packages:

- numpy
- pandas
- scipy
- plotly
- requests
- tqdm
- matplotlib
- fastparquet
- boto3

### Usage
After installing SALSA, you can start using the library in your substrate analyses.
```python
import salsa
```

#### Example 1: Bead Density WaferPlot
In this example, we will create a bead density waferplot to be outputted in a report.
1. Make the routine
```python
routine = salsa.Routine()
```

2. Load the data
```python
runID = “123456_1”
data = salsa.RefBeadData(runID)
data.load()
```
3. Add the analysis to the routine, then run

```python
routine.append(salsa.PlotBeadDensity(data))
routine.run()
```

### Contact

For any inquiries or support related to SALSA, you can reach out to:

- William Huang: william.huang@ultimagen.com
- Jerry Quan: jerry.quan@ultimagen.com