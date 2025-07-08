# 🧊 幽影掷点 (PhantomRoll)

**Stealth Telegram Dice Automation System (PROLL 8879)**  
Ultra-low-latency, production-grade Telegram dice controller built with **C++**, **Java**, and **Python**, featuring **TDLib integration**, **socket control**, and **GUI automation**.

---

## 📌 Features

- 🔐 **TDLib-based session management**
- 🎲 **Dice emoji sender with stealth delete**
- 🧠 **Python controller for advanced dice logic**
- 🪟 **Java GUI with socket communication**
- ⚡ **Low-latency, high-performance architecture**
- 🧩 Modular: Easily extendable (Go, Rust, etc.)
- ✅ Cross-platform: Windows, Linux, macOS (partial)

---

## 📁 Project Structure

```bash
phantomroll/
├── core/                  # Core modules
│   ├── cplusplus/         # C++ TDLib engine
│   ├── go/                # Optional concurrency module (Go)
│   ├── rust/              # Secure deletion (Rust)
│   └── session/           # Session config files
├── controller/            # Python controller logic
│   └── python/
├── ui/                    # User interfaces
│   ├── java/              # Java GUI app
│   └── resources/         # GUI icons
├── dashboard/             # Optional web dashboard (Flask + JS)
├── config/                # JSON/YAML configuration files
├── logs/                  # Runtime logs
├── tools/                 # Helper scripts
├── installer/             # Installer packaging
└── phantomroll.py         # Main Python entry (optional)
