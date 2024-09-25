# Code Dependencies for Prefect Flows

This package serves as a **utility module** for sharing common code across various Prefect flows in your project. The goal is to centralize frequently used functions, classes, and business logic, ensuring consistency and reusability throughout your workflows.

## Purpose

This module is designed to hold:
- **Commonly used functions and classes**: Reusable code components that can be invoked across different Prefect flows.
- **Shared utilities**: Tools, helpers, and configuration code that support your workflow executions.
- **Business logic**: Core business functionalities that are essential for multiple flows in your application.

## How to Use

To use this package in your Prefect flows, simply import the required utilities or logic where necessary.

### Example Structure

```bash
├── code_dependencies/
│   ├── __init__.py
│   ├── utils.py        # Example utilities
│   ├── business_logic.py  # Core business logic
│   └── common_classes.py  # Frequently used classes
```

### Example Code

Here's a brief example of what this module might look like:

```python
# utils.py
def common_function(x):
    return x * 2

# business_logic.py
def process_data(data):
    # Your business logic here
    return transformed_data

# common_classes.py
class Config:
    def __init__(self, setting):
        self.setting = setting
```

Replace the above code with your own commonly used functions, utilities, and business logic that are shared between flows.

## Usage in Flows

To integrate this module into your Prefect flows:

```python
from code_dependencies.utils import common_function
from code_dependencies.business_logic import process_data

@flow
def my_flow(data):
    result = common_function(data)
    processed = process_data(result)
    return processed
```

## Contribution Guidelines

- Place reusable functions, classes, and business logic here for easy sharing across flows.
- Ensure that any new utility or logic added to this module is well-documented.
- Test utilities before integrating them into critical flows.
