# -*- coding: utf-8 -*-
# Environment Check Tool
import sys
import site

if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    # If 'real_prefix' attribute exists or base_prefix is not equal to prefix, it indicates a virtual environment
    print("Current environment is a virtual environment")
else:
    print("Current environment is not a virtual environment")

python_version = sys.version
print("Python version:", python_version)

python_path = sys.executable
print("Python interpreter path:", python_path)

project_python_path = sys.prefix
print("Current project's Python environment path:", project_python_path)

site_packages_path = site.getsitepackages()[1]
print("Third-party packages directory path:", site_packages_path)
