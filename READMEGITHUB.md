# Python Project Setup

This repository contains a simple Python project with Azure DevOps Git integration.

---

## Prerequisites

* Python 3.x
* Git
* Visual Studio Code (Recommended)

---

## Project Setup

### Create Virtual Environment

```bash
python -m venv venvtest
```

### Activate Virtual Environment

#### Linux/macOS

```bash
source venvtest/bin/activate
```

#### Windows

```cmd
venvtest\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Update Requirements File

```bash
pip freeze > requirements.txt
```

---

## Run Application

```bash
python test.py
```

---

# Azure DevOps Git Setup

Initialize Git repository:

```bash
git init
```

Add Azure DevOps remote:

```bash
git remote add origin https://sujeetkumar2010@dev.azure.com/sujeetkumar2010/DsaWebApp/_git/pythonlangchaindemo
```

Verify remote:

```bash
git remote -v
```

Add files:

```bash
git add .
```

Commit changes:

```bash
git commit -m "initial commit"
```

Push code:

```bash
git push -u origin --all
```

---

## Additional Git Commands

Remove existing remote:

```bash
git remote remove origin
```

Pull latest changes:

```bash
git pull origin main
```

Switch to main branch:

```bash
git checkout main
```

Push to main branch:

```bash
git push -u origin main
```

---

# Recommended Git Workflow

Navigate to the project root folder:

```bash
cd <project-root>
```

Initialize repository:

```bash
git init
```

Add Azure DevOps remote:

```bash
git remote add origin https://dev.azure.com/sujeetkumar2010/DsaWebApp/_git/McpServerAndClient
```

Pull latest code:

```bash
git pull origin main
```

Switch to main branch:

```bash
git checkout main
```

Stage changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "initial commit"
```

Push code:

```bash
git push -u origin --all
```

---

## Project Structure

```text
project-root/
│
├── test.py
├── requirements.txt
├── README.md
├── .gitignore
└── venvtest/
```

---

## Author

Sujeet Kumar

Azure | .NET | Python | AI Engineering