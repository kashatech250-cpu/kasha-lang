# 🌍 KashaLang

<p align="center">
  <img src="https://raw.githubusercontent.com/kashalang/kashalang/main/assets/logo.png" alt="KashaLang Logo" width="200">
</p>

<p align="center">
  <strong>The African-Inspired Programming Language</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#examples">Examples</a> •
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg" alt="Platform">
</p>

---

## 🎯 Vision

**KashaLang** is an African-inspired programming language designed to:

- 🌍 **Celebrate African culture** through language and naming
- 🎓 **Be beginner-friendly** with simple, readable syntax
- ⚡ **Be powerful** for real-world applications
- 🌐 **Support multilingual programming** (Kinyarwanda, Swahili, English)
- 🚀 **Enable rapid development** of web, mobile, and automation tools

> **"Kasha"** means "to build" or "to create" in several African languages. With KashaLang, we build the future of African tech together!

---

## ✨ Features

### 📝 African-Inspired Syntax

```kasha
# Hello World in KashaLang
vuga "Muraho, Afurika!"
vuga "Hello, World!"

# Variables
shyiramo izina = "Kasha"
shyiramo imyaka = 5

# Functions
fata greet(name)
    subiza "Muraho, " + name + "!"

# Conditions
niba imyaka >= 18
    vuga "Mukuru"  # Adult
nanone
    vuga "Umuto"   # Child

# Loops
kugeza i from 0 to 10
    vuga i
```

### 🛠️ Complete Toolchain

| Feature | Command | Description |
|---------|---------|-------------|
| **Run** | `kasha run file.kasha` | Execute programs |
| **Init** | `kasha init my-app` | Create new projects |
| **Install** | `kasha install package` | Manage packages |
| **REPL** | `kasha repl` | Interactive shell |
| **Export** | `kasha export web file.kasha` | Generate web apps |

### 📦 Rich Standard Library

- **Math**: `sqrt`, `pow`, `sin`, `cos`, `factorial`, `fibonacci`
- **String**: `split`, `join`, `replace`, `upper`, `lower`
- **List**: `sort`, `reverse`, `map`, `filter`, `reduce`
- **I/O**: `print`, `input`, `file` operations

### 🌐 Web Export

Convert KashaLang programs to HTML/CSS/JS:

```bash
kasha export web myapp.kasha --output ./dist
```

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning)

### Method 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/kashalang/kashalang.git
cd kashalang

# Add to PATH (Linux/macOS)
export PATH=$PATH:$(pwd)

# Add to PATH (Windows PowerShell)
$env:PATH += ";$(Get-Location)"

# Verify installation
kasha version
```

### Method 2: Direct Download

```bash
# Download the latest release
curl -L https://github.com/kashalang/kashalang/releases/latest/download/kashalang.zip -o kashalang.zip
unzip kashalang.zip
cd kashalang
```

### Method 3: pip (Coming Soon)

```bash
pip install kashalang
```

---

## 🚀 Quick Start

### 1. Create Your First Program

```bash
kasha new hello.kasha
```

This creates:

```kasha
# Muraho! Welcome to KashaLang
vuga "Muraho, Afurika!"
vuga "Welcome to KashaLang"

shyiramo izina = "Developer"
vuga "Hello,", izina
```

### 2. Run It

```bash
kasha run hello.kasha
```

Output:
```
Muraho, Afurika!
Welcome to KashaLang
Hello, Developer
```

### 3. Create a Project

```bash
kasha init my-awesome-app --template web --git
cd my-awesome-app
kasha run main.kasha
```

### 4. Interactive Shell (REPL)

```bash
$ kasha repl

╔══════════════════════════════════════════════════════════════╗
║   ██╗  ██╗ █████╗ ███████╗██╗  ██╗ █████╗ ██╗      ██████╗   ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ║
║              🌍 The African Programming Language 🌍           ║
╚══════════════════════════════════════════════════════════════╝

🖥️  KashaLang Interactive Shell (REPL)
   Type 'reka' to exit, 'ubwoko' for help

kasha> shyiramo x = 10
kasha> vuga x * 2
20
```

---

## 📚 Documentation

- [📖 Full Documentation](docs/README.md)
- [🎓 Language Reference](docs/LANGUAGE.md)
- [🛠️ CLI Reference](docs/CLI.md)
- [📦 Standard Library](docs/STDLIB.md)
- [🌐 Web Development](docs/WEB.md)

---

## 💡 Examples

### Hello World

```kasha
vuga "Muraho, Afurika!"
```

### Variables and Math

```kasha
shyiramo radius = 5
shyiramo pi = 3.14159
shyiramo area = pi * radius ** 2

vuga "Circle area:", area
```

### Functions

```kasha
fata factorial(n)
    niba n <= 1
        subiza 1
    subiza n * factorial(n - 1)

vuga "5! =", factorial(5)  # 120
```

### Loops

```kasha
# While loop
shyiramo i = 0
igihe i < 5
    vuga "Count:", i
    i = i + 1

# For loop
kugeza j from 0 to 5
    vuga "Number:", j

# For-in loop
shyiramo fruits = ["apple", "banana", "cherry"]
subiramo fruit in fruits
    vuga fruit
```

### Lists and Dictionaries

```kasha
# Lists
shyiramo numbers = [1, 2, 3, 4, 5]
ongera(numbers, 6)
vuga numbers  # [1, 2, 3, 4, 5, 6]

# Dictionaries
shyiramo person = {
    "name": "Kasha",
    "country": "Rwanda"
}
vuga person["name"]  # Kasha
```

See more examples in the [`/examples`](examples/) directory!

---

## 🌍 Language Keywords

KashaLang supports multilingual keywords:

| Kinyarwanda | Swahili | English | Purpose |
|-------------|---------|---------|---------|
| `vuga` | `sema` | `print` | Output |
| `shyiramo` | `weka` | `let` | Variable |
| `niba` | `kama` | `if` | Condition |
| `nanone` | `vinginevyo` | `else` | Alternative |
| `subiramo` | `rudia` | `loop` | Loop |
| `fata` | `chukua` | `fn` | Function |
| `subiza` | `rudisha` | `return` | Return |

---

## 🏗️ Project Structure

```
kashalang/
├── core/               # Core interpreter
│   ├── lexer.py        # Tokenizer
│   ├── parser.py       # AST parser
│   ├── interpreter.py  # Code executor
│   ├── ast_nodes.py    # AST definitions
│   └── errors.py       # Error handling
├── cli/                # Command line interface
│   ├── main.py         # CLI entry point
│   ├── project_init.py # Project creation
│   ├── package_manager.py
│   └── exporter.py     # Web export
├── stdlib/             # Standard library
│   ├── math.kasha
│   ├── string.kasha
│   └── list.kasha
├── examples/           # Example programs
│   ├── basics/
│   ├── algorithms/
│   └── web/
├── docs/               # Documentation
├── tests/              # Test suite
├── README.md
├── LICENSE
└── kasha               # CLI script
```

---

## 🤝 Contributing

We welcome contributions from everyone! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Areas for Contribution

- 🌍 **Language Support**: Add more African language keywords
- 📚 **Documentation**: Improve docs and tutorials
- 🧪 **Testing**: Add test cases
- 📦 **Packages**: Build libraries
- 🎨 **Design**: Create logos and branding
- 🌐 **Website**: Improve the web presence

---

## 📜 Roadmap

### Phase 1: MVP (Current) ✅
- [x] Core interpreter (lexer, parser, interpreter)
- [x] Basic data types (numbers, strings, booleans)
- [x] Variables and operators
- [x] Conditions and loops
- [x] Functions
- [x] Lists and dictionaries
- [x] CLI tool
- [x] Standard library

### Phase 2: Ecosystem (In Progress) 🚧
- [ ] Package manager enhancements
- [ ] More standard library modules
- [ ] IDE support (VS Code extension)
- [ ] Syntax highlighting
- [ ] Linter and formatter

### Phase 3: Advanced Features 🔮
- [ ] Classes and objects
- [ ] Modules and imports
- [ ] File I/O
- [ ] Network operations
- [ ] Database connectivity
- [ ] Web framework

### Phase 4: Platform Expansion 🚀
- [ ] Mobile app generation
- [ ] Desktop applications
- [ ] WebAssembly target
- [ ] Cloud deployment
- [ ] AI/ML integration

---

## 🏆 Acknowledgments

KashaLang is inspired by:
- **Python** - For simplicity and readability
- **JavaScript** - For expressiveness
- **African languages** - For cultural identity
- **The African tech community** - For the vision

Special thanks to all contributors and supporters!

---

## 📄 License

KashaLang is released under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 KashaLang Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 📞 Contact

- 🌐 **Website**: [https://kashalang.dev](https://kashalang.dev)
- 🐦 **Twitter**: [@kashalang](https://twitter.com/kashalang)
- 💬 **Discord**: [Join our community](https://discord.gg/kashalang)
- 📧 **Email**: hello@kashalang.dev
- 🐙 **GitHub**: [github.com/kashalang/kashalang](https://github.com/kashalang/kashalang)

---

<p align="center">
  <strong>Made with 🌍 love for Africa</strong>
</p>

<p align="center">
  <em>"Coding in the language of our ancestors, building for the future."</em>
</p>

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=kashalang/kashalang&type=Date)](https://star-history.com/#kashalang/kashalang&Date)

---

<p align="center">
  <a href="https://github.com/kashalang/kashalang">
    <img src="https://img.shields.io/github/stars/kashalang/kashalang?style=social" alt="GitHub stars">
  </a>
</p>
