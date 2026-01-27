# Hermes

### The messenger god who translates between worlds

> Your cultural syntax → Python. Seamlessly.

---

## What is Hermes?

A programming language with **swappable cultural skins**. Write code in syntax inspired by comedy, cinema, memes - it all transpiles to Python.

```bash
# Run with Vadivelu skin (default)
hermes run hello.hm

# Run with Monty Python skin
hermes run hello.hm --skin monty

# See available skins
hermes skins
```

## Why Hermes?

**Hermes** (Ἑρμῆς) - Greek god who:
- Translates between mortals and gods
- Guides souls between worlds
- Messenger of meaning

Just like this language translates your cultural syntax into universal Python.

## Example (Vaigai Skin - Vadivelu)

```hermes
scheme greet(name):
    announce("Hello, " + name)
    abandon truth

aahaan greet("world"):
    announce("Success!")
thats_it:
    announce("Something went wrong")
```

Transpiles to:

```python
def greet(name):
    print("Hello, " + name)
    return True

if greet("world"):
    print("Success!")
else:
    print("Something went wrong")
```

## Available Skins

| Skin | Culture | Status |
|------|---------|--------|
| vaigai | Tamil Cinema (Vadivelu) | Default |
| monty | British Comedy (Monty Python) | Coming |
| memes | Internet Culture | Coming |
| Community contributions welcome |

## Install

```bash
# Homebrew
brew install 0xraghu/tap/hermes

# PyPI
pip install hermes-lang

# From source
git clone https://github.com/0xRaghu/hermes-lang
cd hermes-lang && pip install -e .
```

## Philosophy

- **Tamil roots, global wings** - Cultural origin, universal access
- **Comedy meets code** - Programming should be memorable
- **Skins, not forks** - One engine, infinite expressions

---

**[GitHub](https://github.com/0xRaghu/hermes-lang)** · **[X](https://twitter.com/Pilan_AI)**

*Pay what you want: Bitcoin accepted*
