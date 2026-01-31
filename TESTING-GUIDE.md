# Hermes Testing Guide - User Manual

**Target**: Non-programmer user testing in 5-minute chunks  
**Format**: Checkboxes + observations  
**Goal**: Validate transpiler functionality before business decisions

---

## 🎯 What You're Testing

Hermes is a programming language with cultural skins that transpiles to Python. The default skin is "Sangam" (Tamil-inspired syntax). You write code in Tamil/cultural keywords, Hermes converts it to Python.

**Example:**
```hermes
# Hermes (Sangam skin)
scheme greet(name):
    announce("Hello, " + name)
    abandon "success"
```

**Becomes Python:**
```python
def greet(name):
    print("Hello, " + name)
    return "success"
```

**Core Features to Test:**
1. ✅ `run` - Execute Hermes code directly
2. ✅ `compile` - Transpile Hermes to Python
3. ✅ `check` - Syntax validation without running
4. ✅ Cultural syntax keywords work correctly

---

## 📋 Pre-Test Setup (2 minutes)

### Checkpoint A: Verify Installation

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes
python3 -m hermes --help
```

**Expected Output:**
```
usage: hermes [-h] {run,compile,check,serve-mcp} ...

Hermes thinks through you! Cultural syntax transpiled to Python

positional arguments:
  {run,compile,check,serve-mcp}
    run                 Run a Hermes file
    compile             Transpile to Python
    check               Syntax check only
    serve-mcp           Start MCP server for auto-injection

options:
  -h, --help            show this help message and exit
```

**✅ Checklist:**
- [x] `python3 -m hermes --help` works without errors
- [x] You see the 4 commands: run, compile, check, serve-mcp
- [x] You see the tagline "Hermes thinks through you!"

**📝 Notes:**
```
[Add any observations or issues here]




```

---

## 🧪 Test 1: Run Hello World (3 minutes)

### What This Tests
Basic transpilation and execution of a simple Hermes program.

### Commands to Run

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes/examples
python3 -m hermes run hello.herm
```

### Expected Output
```
Hello, World!
Greeting successful!
```

### ✅ Checklist
- [x] Program runs without errors
- [x] Prints "Hello, World!"
- [x] Prints "Greeting successful!"
- [x] Execution is fast (<1 second)

### 📝 Notes - What You Observe
```
Did it print the expected output?




Any errors during execution?




Execution time (fast/slow)?


```

---

## 🧪 Test 2: View Source Files (2 minutes)

### What This Tests
Understanding what Hermes code looks like.

### Commands to Run

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes/examples
cat hello.herm
```

### Expected Content
```hermes
scheme greet():
    announce("Hello, World!")
    abandon "Greeting successful!"

announce(greet())
```

### What Keywords Mean
| Hermes (Sangam) | Python Equivalent | Meaning |
|-----------------|-------------------|---------|
| `scheme` | `def` | Define function |
| `announce` | `print` | Print/output |
| `abandon` | `return` | Return value |
| `aahaan` | `if` | If condition |
| `thats_it` | `else` | Else clause |

### ✅ Checklist
- [x] You can see cultural keywords (scheme, announce, abandon)
- [x] Code is readable even if you don't know Python
- [x] Keywords feel intuitive

### 📝 Notes - What You Think
```
Do the cultural keywords make sense to you?




Is "scheme" intuitive for "define function"?




Is "announce" intuitive for "print"?




Is "abandon" intuitive for "return"?




Would you prefer different keywords? Suggest:




```

---

## 🧪 Test 3: Compile to Python (4 minutes)

### What This Tests
Transpilation process - converting Hermes to Python code.

### Commands to Run

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes/examples
python3 -m hermes compile hello.herm
```

### Expected Output
```python
def greet():
    print("Hello, World!")
    return "Greeting successful!"

print(greet())
```

### ✅ Checklist
- [x] Transpilation succeeds without errors
- [x] Output is valid Python code
- [x] `scheme` → `def` correctly
- [x] `announce` → `print` correctly
- [x] `abandon` → `return` correctly

### 📝 Notes - What You Observe
```
Does the Python output look correct?




Is the transpilation 1:1 accurate?




Any weird artifacts or issues in output?




```

---

## 🧪 Test 4: Test Other Examples (5 minutes)

### What This Tests
More complex Hermes programs with different features.

### Commands to Run

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes/examples

# Test 1: Fibonacci (loops, conditionals)
python3 -m hermes run fibonacci.herm

# Test 2: Classes (object-oriented)
python3 -m hermes run classes.herm

# Test 3: API Server (more complex)
python3 -m hermes run api_server.herm
```

### Expected Outputs

**fibonacci.herm:**
```
0
1
1
2
3
5
8
13
21
34
```

**classes.herm:**
```
(Should print class-related output)
```

**api_server.herm:**
```
(Should define API routes without errors)
```

### ✅ Checklist
- [x] Fibonacci runs and prints sequence
- [x] Classes example runs without errors
- [ ] API server example runs without errors
- [ ] All examples complete quickly

### 📝 Notes - What You Observe

**Fibonacci:**
```
Did it print the sequence correctly?




```

**Classes:**
```
Did it work?




What did it print?




```

**API Server:**
```
Did it run without errors?




```

**Any failures:**
```
Which examples failed (if any)?





Error messages:




```

---

## 🧪 Test 5: Syntax Checking (3 minutes)

### What This Tests
Validation without execution - check if code is valid before running.

### Commands to Run

```bash
cd /Users/raghu/Projects/PILAN-INTELLIGENCE-PRISM/code/products/hermes/examples

# Check valid syntax
python3 -m hermes check hello.herm

# Create a file with bad syntax
echo "scheme test():" > /tmp/bad.herm
echo "    announce(this is bad" >> /tmp/bad.herm

# Check bad syntax
python3 -m hermes check /tmp/bad.herm
```

### Expected Output

**Valid file:**
```
✓ Syntax OK
```

**Invalid file:**
```
✗ Syntax error at line 2:
    announce(this is bad
                    ^
Expected closing parenthesis
```

### ✅ Checklist
- [x] Valid syntax files pass check
- [x] Invalid syntax files show clear errors
- [x] Error messages are helpful
- [x] Line numbers are accurate

### 📝 Notes - What You Observe
```
Did syntax check work for valid files?




Did it catch errors in invalid files?




Were error messages helpful?




```

---

## 🧪 Test 6: Write Your Own Code (5 minutes)

### What This Tests
Can you actually use Hermes to write something?

### Exercise
Create a simple program that prints your name 3 times.

```bash
cd /tmp

# Create your test file
cat > mytest.herm << 'EOF'
scheme print_name(name):
    announce(name)
    announce(name)
    announce(name)
    abandon "done"

print_name("Raghu")
EOF

# Run it
python3 -m hermes run mytest.herm
```

### Expected Output
```
Raghu
Raghu
Raghu
```

### ✅ Checklist
- [x] Your code runs successfully
- [x] Prints your name 3 times
- [x] No errors

### 📝 Notes - Your Experience
```
Was it easy to write Hermes code?




Did you understand the syntax?




Did you make any mistakes? What were they?




Would you be comfortable writing more complex code?




```

---

## 🧪 Test 7: Edge Cases (3 minutes)

### What This Tests
How Hermes handles errors and unusual inputs.

### Commands to Run

```bash
# Non-existent file
python3 -m hermes run nonexistent.herm

# Empty file
touch /tmp/empty.herm
python3 -m hermes run /tmp/empty.herm

# File with only comments
echo "# Just a comment" > /tmp/comment.herm
python3 -m hermes run /tmp/comment.herm
```

### ✅ Checklist
- [x] Non-existent file shows clear error
- [x] Empty file doesn't crash
- [x] Comment-only file doesn't crash
- [x] Error messages are understandable

### 📝 Notes - What You Observe
```
Did anything crash unexpectedly?




Were error messages helpful?




```

---

## 📊 Final Summary

### Overall Experience (Rate 1-5)

- **Ease of Use**: ____/5 (1 = confusing, 5 = intuitive)
- **Cultural Keywords**: ____/5 (1 = weird, 5 = natural)
- **Usefulness**: ____/5 (1 = pointless, 5 = game-changer)
- **Reliability**: ____/5 (1 = crashes, 5 = rock solid)

### What Worked Well
```
List 3 things that worked smoothly:
1. 
2. 
3. 
```

### What Needs Improvement
```
List 3 things that need fixing:
1. 
2. 
3. 
```

### Would You Actually Use This?
```
Honest answer: Yes / No / Maybe

Why or why not?





```

### Cultural Keywords Feedback
```
Which keywords felt natural:




Which keywords felt weird:




What alternative keywords would you suggest:
- scheme → ____
- announce → ____
- abandon → ____
- aahaan → ____
- thats_it → ____


```

### Business Model Feedback
```
Knowing what you know now, what would you pay for this?

Free / $5/mo / $10/mo / Other: ____

Would you pay more for:
- More cultural skins (Hindi, Spanish, Arabic): ____
- IDE integration (VS Code plugin): ____
- Enterprise license for teams: ____


```

---

## 🚨 Critical Issues (If Any)

```
Did Hermes completely fail to work?
Were there major bugs that prevented testing?
Is there something fundamentally broken?

If yes, describe in detail:





```

---

## 💡 Ideas & Suggestions

```
What features would make Hermes amazing?




What cultural skin would you want next?




Any other thoughts:




```

---

**End of Hermes Testing Guide**

Save this file with your notes and we'll review together!
