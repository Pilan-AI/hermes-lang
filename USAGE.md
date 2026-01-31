# Hermes Usage Guide

**How to run Hermes in different environments**

---

## 1. Command Line (Recommended)

### Basic Usage
```bash
# Run a Hermes file directly
hermes run script.herm

# Transpile to Python
hermes compile script.herm -o script.py

# Syntax check only
hermes check script.herm
```

### With Debug Output
```bash
# See the transpiled Python code
hermes run script.herm --debug
```

---

## 2. VSCode Integration

### Option A: Run via Integrated Terminal
1. Open your `.herm` file in VSCode
2. Press `` Ctrl+` `` to open integrated terminal
3. Run: `hermes run yourfile.herm`

### Option B: Custom Task (Better)
Create `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Hermes",
      "type": "shell",
      "command": "hermes",
      "args": ["run", "${file}"],
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

**Usage**: Press `Cmd+Shift+B` (Mac) or `Ctrl+Shift+B` (Windows/Linux) to run current file.

### Option C: Keyboard Shortcut
Add to `.vscode/keybindings.json`:
```json
[
  {
    "key": "cmd+shift+r",
    "command": "workbench.action.terminal.sendSequence",
    "args": {
      "text": "hermes run ${file}\n"
    },
    "when": "editorLangId == hermes"
  }
]
```

---

## 3. Jupyter Notebook

### Option A: Transpile Then Run
```python
# In Jupyter cell
import subprocess

# Transpile Hermes to Python
subprocess.run(['hermes', 'compile', 'script.herm', '-o', 'script.py'])

# Import and run the Python output
import script
```

### Option B: Direct Execution
```python
# In Jupyter cell
import subprocess
import sys

# Run Hermes script and capture output
result = subprocess.run(
    ['hermes', 'run', 'script.herm'],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr, file=sys.stderr)
```

### Option C: Magic Command (Advanced)
Create `~/.ipython/profile_default/startup/hermes_magic.py`:
```python
from IPython.core.magic import register_line_magic
import subprocess

@register_line_magic
def hermes(line):
    """Run Hermes code: %hermes script.herm"""
    result = subprocess.run(
        ['hermes', 'run', line.strip()],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

# Delete to avoid name conflicts
del hermes
```

**Usage in Jupyter**:
```python
%hermes script.herm
```

---

## 4. As Python Module (Programmatic)

### Direct Import After Transpilation
```python
# Transpile first
import subprocess
subprocess.run(['hermes', 'compile', 'mycode.herm', '-o', 'mycode.py'])

# Then import
import mycode

# Use it
mycode.my_function()
```

### Inline Transpilation
```python
from hermes.transpiler import transpile

hermes_code = """
scheme greet(name):
    announce("Hello, " + name)
    abandon truth
"""

python_code = transpile(hermes_code)
exec(python_code)
```

---

## 5. Build Systems & CI/CD

### Makefile
```makefile
.PHONY: build test run

build:
	find . -name "*.herm" -exec hermes compile {} -o {}.py \;

test:
	hermes check src/*.herm
	pytest tests/

run:
	hermes run src/main.herm
```

### GitHub Actions
```yaml
name: Hermes CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Hermes
        run: pip install hermes-lang
      
      - name: Check syntax
        run: hermes check src/*.herm
      
      - name: Transpile
        run: |
          for f in src/*.herm; do
            hermes compile "$f" -o "${f%.herm}.py"
          done
      
      - name: Run tests
        run: pytest tests/
```

---

## 6. Package/Distribution

### Include Transpiled Python
For distribution, transpile to Python and ship both:

```
my-package/
├── pyproject.toml
├── src/
│   ├── original.herm       # Source code
│   └── original.py         # Transpiled (for users without Hermes)
└── README.md
```

**pyproject.toml**:
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "1.0.0"
dependencies = []  # No Hermes dependency for end users

[project.optional-dependencies]
dev = ["hermes-lang>=0.1.0"]  # Only for developers
```

**Build script** (`build.py`):
```python
import subprocess
from pathlib import Path

for herm_file in Path("src").glob("**/*.herm"):
    py_file = herm_file.with_suffix(".py")
    subprocess.run(["hermes", "compile", str(herm_file), "-o", str(py_file)])
```

---

## 7. REPL / Interactive Mode

Currently Hermes doesn't have a REPL. Workarounds:

### Option A: Use Python REPL After Transpilation
```bash
hermes compile script.herm -o script.py
python3 -i script.py  # Interactive mode with preloaded code
```

### Option B: Quick Feedback Loop
```bash
# Create test.herm, edit, run in loop
watch -n 2 "hermes run test.herm"
```

---

## 8. IDE Support Roadmap

### Current Status
- ✅ Command line works everywhere
- ✅ VSCode tasks (manual setup)
- ⚠️ No syntax highlighting (yet)
- ⚠️ No autocomplete (yet)

### Future (Help Wanted!)
- [ ] VSCode extension (`.herm` syntax highlighting)
- [ ] Language Server Protocol (LSP) for autocomplete
- [ ] Jupyter kernel (native `%%hermes` magic)
- [ ] PyCharm plugin

---

## 9. Debugging Hermes Code

### Check Transpiled Output
```bash
hermes run script.herm --debug
```

### Step Through Python
```bash
# Transpile to Python
hermes compile script.herm -o script.py

# Debug Python with pdb
python3 -m pdb script.py
```

### Common Issues

| Error | Solution |
|-------|----------|
| `SyntaxError: invalid syntax` | Run `hermes check script.herm` first |
| `NameError: name 'X' is not defined` | Check for typos in keywords (`scheme` vs `def`) |
| Transpilation fails | Check Hermes syntax (not Python syntax) |

---

## 10. Editor Setup Tips

### VSCode `.herm` File Association
Add to `settings.json`:
```json
{
  "files.associations": {
    "*.herm": "python"  // Temporary: use Python syntax highlighting
  }
}
```

### Vim
Add to `.vimrc`:
```vim
au BufRead,BufNewFile *.herm set filetype=python
```

### Emacs
Add to `.emacs`:
```elisp
(add-to-list 'auto-mode-alist '("\\.herm\\'" . python-mode))
```

---

## 11. Performance Tips

### Transpile Once, Run Many
```bash
# BAD: Transpiles every time
for i in {1..100}; do hermes run script.herm; done

# GOOD: Transpile once
hermes compile script.herm -o script.py
for i in {1..100}; do python3 script.py; done
```

### Cache Transpiled Files
```python
import os
import subprocess
from pathlib import Path

def run_hermes(herm_file):
    py_file = Path(herm_file).with_suffix('.py')
    
    # Only transpile if .herm is newer than .py
    if not py_file.exists() or os.path.getmtime(herm_file) > os.path.getmtime(py_file):
        subprocess.run(['hermes', 'compile', herm_file, '-o', str(py_file)])
    
    # Run cached Python
    subprocess.run(['python3', str(py_file)])
```

---

## 12. Examples

### Quick Start
```bash
# Create hello.herm
cat > hello.herm << 'EOF'
scheme greet(name):
    announce("Hello, " + name + "!")
    abandon truth

greet("World")
EOF

# Run it
hermes run hello.herm
```

### With VSCode Task
1. Save above as `hello.herm`
2. Set up task (see section 2)
3. Press `Cmd+Shift+B`
4. Output appears in integrated terminal

### In Jupyter
```python
# Cell 1: Write Hermes code
%%writefile script.herm
scheme calculate(x, y):
    result = x + y
    announce("Result: " + str(result))
    abandon result

calculate(5, 10)

# Cell 2: Run it
!hermes run script.herm
```

---

## Need Help?

- **GitHub Issues**: https://github.com/Pilan-AI/hermes-lang/issues
- **Discussions**: https://github.com/Pilan-AI/hermes-lang/discussions
- **X/Twitter**: [@pilan_ai](https://x.com/pilan_ai)

---

**Pro Tip**: Hermes transpiles to Python, so anything Python can do, Hermes can do. Just import Python libraries normally!

```hermes
scheme main():
    import numpy as np
    
    data = np.array([1, 2, 3, 4, 5])
    announce("Mean: " + str(np.mean(data)))
    
main()
```
