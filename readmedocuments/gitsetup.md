# First Time Git Check-in (Local to GitHub)

## 1. Verify Git Installation

```bash
git --version
```

Example:

```text
git version 2.50.1.windows.1
```

---

## 2. Initialize Git Repository

```bash
git init
```

Verify:

```bash
git status
```

You should see:

```text
On branch master

No commits yet
```

---

## 3. Create .gitignore

Create a `.gitignore` file:

```gitignore
venv/
__pycache__/
*.pyc
.vscode/
.env
```

---

## 4. Check Current Files

```bash
git status
```

Review the files that will be added.

---

## 5. Stage Files

```bash
git add .
```

Verify staged files:

```bash
git status
```

You should see:

```text
Changes to be committed:
    new file: README.md
    new file: main.py
    new file: .gitignore
```

Ensure that `venv` files are NOT listed.

---

## 6. Create Initial Commit

```bash
git commit -m "Initial commit"
```

Verify commit:

```bash
git log --oneline
```

Example:

```text
a1b2c3d Initial commit
```

---

## 7. Check Current Branch

```bash
git branch
```

Example:

```text
* master
```

or

```text
* main
```

---

## 8. Rename Branch to Main (Recommended)

```bash
git branch -M main
```

Verify:

```bash
git branch
```

Expected:

```text
* main
```

---

## 9. Add GitHub Remote Repository

```bash
git remote add origin https://github.com/<username>/<repository-name>.git
```

Example:

```bash
git remote add origin https://github.com/sujeet988/Agents-Series.git
```

---

## 10. Verify Remote Configuration

```bash
git remote -v
```

Expected:

```text
origin  https://github.com/sujeet988/Agents-Series.git (fetch)
origin  https://github.com/sujeet988/Agents-Series.git (push)
```

---

## 11. Push Code to GitHub

```bash
git push -u origin main
```

The `-u` option sets the upstream branch so future pushes only require:

```bash
git push
```

---

## 12. Verify on GitHub

Refresh your GitHub repository page and verify:

- README.md
- .gitignore
- main.py
- requirements.txt

are visible.

---

## Troubleshooting

### Check Current Branch

```bash
git branch
```

### Check Remote

```bash
git remote -v
```

### Check Commit History

```bash
git log --oneline
```

### Check Working Directory Status

```bash
git status
```

### Check Which Files Are Tracked

```bash
git ls-files
```

---

## Daily Workflow

After the initial setup:

```bash
git status
git add .
git commit -m "Added new feature"
git push
```