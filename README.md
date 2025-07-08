
# 🧊 幽影掷点 (PhantomRoll)

**Stealth Telegram Dice Automation System (PROLL 8879)**  
Ultra-low-latency, production-grade Telegram dice controller built with **C++**, **Java**, and **Python**, featuring **TDLib integration**, **socket control**, and **GUI automation**.
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
🖥️ Build & Run
🔧 Requirements
CMake ≥ 3.15

g++ or clang (Linux/macOS)

MSVC or MinGW (Windows)

TDLib compiled

Python ≥ 3.10 (for controller)

Java 11+ (for GUI)

⚙️ Compile Core (C++)
🐧 Linux
bash
Copy
Edit
cd phantomroll/core/cplusplus
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
🪟 Windows (MSVC)
Open x64 Native Tools Command Prompt for VS 2019:

cmd
Copy
Edit
cd C:\Users\YourName\phantomroll\core\cplusplus
mkdir build && cd build
cmake .. -G "Visual Studio 16 2019"
cmake --build . --config Release
Or for MinGW:

bash
Copy
Edit
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release ..
mingw32-make
🍎 macOS
bash
Copy
Edit
cd phantomroll/core/cplusplus
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(sysctl -n hw.ncpu)
🧪 Run PhantomRoll
Edit your config: phantomroll/core/session/config.json

Run:

bash
Copy
Edit
cd phantomroll/core/cplusplus/build
./phantomroll  # or phantomroll.exe on Windows
Follow terminal prompts to authenticate and begin automation.

🪟 Java GUI (Optional)
bash
Copy
Edit
cd phantomroll/ui/java
javac PhantomRollUI.java
java PhantomRollUI
GUI sends socket commands to the C++ dice engine on port 8879.

🔌 Python Controller
bash
Copy
Edit
cd phantomroll/controller/python
python main_controller.py
This Python module includes:

🎯 Combo finder

🔄 Socket bridge to GUI or CLI

🧪 Testing stubs (test_login.py, telethon_client.py)

🔒 Configuration Format
phantomroll/core/session/config.json

json
Copy
Edit
{
  "api_id": 123456,
  "api_hash": "your_api_hash",
  "target_chat_id": 987654321,
  "dice_emoji": "🎲",
  "interval_ms": 3000,
  "delete_delay_ms": 100,
  "use_test_dc": false
}
📦 Packaging (Windows EXE)
To build a distributable Windows executable:

bash
Copy
Edit
cd phantomroll/installer
bash build_installer.sh
You can also use phantomroll.spec with PyInstaller for the Python layer.

🧠 Development Goals
✅ Real-time Telegram dice interaction

✅ Ultra-fast delete to avoid message detection

✅ Pluggable logic modules (combo detection, ML, etc.)

⏳ Future: Game-specific logic, Telegram bot mode, stealth client mode

🧠 Research Basis
PhantomRoll was developed as part of a Master's-level research in:

Computer Science (Real-time automation, low-latency C++ systems)

Electrical & Electronics Engineering (protocol design, stealth communication)

Contact: Enock Isaboke (@nyakeriga)

📝 License
MIT License — Use freely with attribution.
Developed by @nyakeriga

yaml
Copy
Edit

</details>

---

#### 2. ✅ Final Git Commit and Push

```bash
cd ~/phantomroll

# Re-initialize if needed (optional)
git init
git remote add origin https://github.com/nyakeriga/telegram-bot-development.git

# Remove embedded git folder (if it exists)
rm -rf phantomroll/.git

# Add and push
git add .
git commit -m "🔄 Final project push: PhantomRoll (C++/Java/Python)"
git branch -M main
git push -u origin main
