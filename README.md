<div align="center">

# hermes-lang

### Hermes thinks through you!

> Your cultural syntax → Python. Seamlessly.

</div>

---

## What is Hermes?

A programming language with **swappable cultural skins**. Write code in syntax inspired by comedy, cinema, memes — it all transpiles to Python.

```bash
# Run a Hermes file
hermes run hello.herm

# Transpile to Python
hermes compile hello.herm -o hello.py

# Syntax check
hermes check hello.herm
```

## Why Hermes?

**Hermes** (Ἑρμῆς) — Greek god who:
- Translates between mortals and gods
- Guides souls between worlds
- Messenger of meaning

Just like this language translates your cultural syntax into universal Python.

## Example (Sangam Skin)

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
| sangam | Tamil Cinema (Vadivelu) | Default |
| monty | British Comedy (Monty Python) | Coming |
| memes | Internet Culture | Coming |
| Community contributions welcome |

## Install

```bash
# Homebrew (recommended)
brew install hermes-lang

# From source
git clone https://github.com/Pilan-AI/hermes-lang
cd hermes-lang && pip install -e .
```

## Philosophy

- **Tamil roots, global wings** — Cultural origin, universal access
- **Comedy meets code** — Programming should be memorable
- **Skins, not forks** — One engine, infinite expressions

---

## License

hermes-lang is dual-licensed:

- **AGPL v3** — Free for open source and personal use
- **Commercial License** — For proprietary/enterprise use

---

<div align="center">

**[GitHub](https://github.com/Pilan-AI/hermes-lang)** · **[X](https://x.com/Pilan_AI)**

*Pay what you want: Bitcoin accepted*

</div>
