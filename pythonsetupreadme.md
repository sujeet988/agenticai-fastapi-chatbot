# Hello Python

A simple Python project demonstrating how to set up and run a Python application.

## Prerequisites

- Python 3.10 or later

## Create Project

```bash
mkdir HelloPython
cd HelloPython
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Run Application

```bash
python main.py
```

Expected Output:

```text
Hello, Python!
```

## Install Dependencies

```bash
pip install requests
```

## Save Dependencies

```bash
pip freeze > requirements.txt
```

## Install Dependencies from File

```bash
pip install -r requirements.txt
```

## Project Structure

```text
HelloPython/
│
├── venv/
├── main.py
├── requirements.txt
└── README.md
```

## Author

Created as a sample Python starter project.