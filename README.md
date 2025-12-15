# 🤖 Personal Assistant Bot

> Your intelligent CLI companion for managing contacts and notes with AI-powered natural language understanding

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-500%2B-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen.svg)](tests/)

---

## 🎯 About KeepInMind

**KeepInMind** is a personal CLI assistant designed to streamline contact and note management through an intelligent command-line interface. This project represents a modern approach to personal information management, combining traditional software engineering excellence with cutting-edge AI capabilities.

### 👥 Development Team

This project was developed by a dedicated team of six engineers:

- **Mykyta Kotenko** - Team Lead & Developer
- **Anastasiia Chorna** - Developer
- **Oleksandr Popov** - Developer
- **Hlib Boiko** - Developer
- **Volodymyr Shapovalov** - Developer
- **Anzhela Schults** - Developer

### 🚀 Development Process

Our team followed professional software engineering practices throughout development:

- **Agile Methodology**: Regular sprint meetings and iterative development
- **Project Management**: Task tracking via Trello with clear backlog and sprint boards
- **Version Control**: GitHub flow with pull requests, code reviews, and branch protection
- **Code Quality**: Strict coding standards, type safety, and comprehensive testing
- **Collaboration**: Daily standups, knowledge sharing, and pair programming

### 🎯 Problem & Solution

**The Challenge:**
Modern professionals struggle with scattered contact information across multiple platforms, applications, and devices. Finding a phone number, checking someone's birthday, or locating a specific note often involves searching through emails, messaging apps, and various contact management tools.

**Our Solution:**
KeepInMind provides a unified, intelligent CLI interface that:
- Centralizes all contact and note information in one place
- Offers both traditional command syntax and natural language input
- Integrates with AI assistants via Model Context Protocol (MCP)
- Ensures data privacy by keeping everything local
- Provides instant access without switching between applications

### 💪 Development Challenges

Our team encountered and successfully resolved several significant challenges:

**1. Organizational Coordination**
- Managing parallel development across 6 team members
- Coordinating feature integration without conflicts
- Solution: Implemented strict GitHub flow with protected branches and mandatory code reviews

**2. Data Structure Agreement**
- Aligning on entity models, value objects, and database schema
- Ensuring backward compatibility during schema evolution
- Solution: Adopted Domain-Driven Design (DDD) principles with clear bounded contexts

**3. NLP Integration Complexity**
- Balancing ML model accuracy with performance
- Handling edge cases in natural language understanding
- Solution: Implemented hybrid approach with ML models and rule-based fallback

**4. Cross-Platform Testing**
- Ensuring consistent behavior across operating systems
- Managing different Python environments and dependencies
- Solution: Comprehensive test suite with 500+ tests and CI/CD integration

### 🛠️ Technology Stack

**Core Technologies:**
- **Python 3.10+** with full type safety
- **SQLAlchemy 2.0** for robust data persistence
- **PyTorch 2.0+** for deep learning capabilities
- **Transformers (Hugging Face)** for NLP models
- **FastMCP 2.13.0** for LLM integration

**Architecture:**
- **Domain-Driven Design (DDD)** for business logic clarity
- **Clean Architecture** with 4 distinct layers
- **SOLID principles** throughout codebase
- **Dependency Inversion** for testability

**Quality Assurance:**
- **500+ unit and integration tests**
- **97% code coverage**
- **Type hints** on 100% of codebase
- **Automated linting** with pylint and mypy

### ✨ Key Features Delivered

**Contact Management:**
- Multiple contact fields (name, phone, email, address, birthday)
- Smart search with fuzzy matching
- Data validation with international standards
- Birthday reminders and upcoming events

**Note Organization:**
- Rich text notes with title and content
- Flexible tagging system
- Full-text search across all notes
- Bulk operations for efficiency

**AI-Powered NLP:**
- Natural language command understanding
- Intent classification with 34 supported intents
- Named Entity Recognition (NER) for automatic extraction
- Confidence scoring with intelligent fallback

**MCP Integration:**
- 39 tools exposed to Claude Desktop
- Seamless AI assistant integration
- Context-aware command execution
- Real-time data synchronization

### 📈 What We Accomplished

**Technical Achievements:**
- ✅ **15,000+ lines** of production-quality code
- ✅ **97% test coverage** with comprehensive test suite
- ✅ **34 NLP intents** with high accuracy
- ✅ **4-layer architecture** following Clean Architecture principles
- ✅ **Type-safe codebase** with mypy validation
- ✅ **Zero critical bugs** in production

**Team Benefits:**
- 🎓 **Skill Development**: Gained expertise in ML, NLP, DDD, and Clean Architecture
- 🤝 **Collaboration**: Strengthened teamwork through code reviews and pair programming
- 📚 **Best Practices**: Established patterns for testing, documentation, and code quality
- 🔧 **Tools Mastery**: Proficiency in modern Python ecosystem and ML frameworks

### 🔮 Future Development

Our roadmap includes exciting enhancements:

- 💬 **Telegram Bot** integration for mobile convenience
- 🔄 **Cloud Sync** (optional) for multi-device access
- 📱 **Mobile App** for iOS and Android
- 🤖 **LLM Integration** for advanced natural language features
- 🔍 **Semantic Search** using embeddings
- 📊 **Analytics Dashboard** for usage insights
- 🔐 **End-to-end Encryption** for cloud features
- 🌍 **Multi-language Support** (Spanish, French, German, etc.)
- 🔗 **Third-party Integrations** (Google Contacts, Outlook, etc.)
- 🎙️ **Voice Commands** via speech recognition
- 🧠 **Smart Suggestions** based on usage patterns

### 🏆 Project Impact

KeepInMind demonstrates that personal productivity tools can be:
- **Powerful** without being bloated
- **Intelligent** without sacrificing privacy
- **Professional** without enterprise complexity
- **Extensible** without technical debt

Our team proved that by combining solid engineering principles with modern AI capabilities, we can create tools that genuinely improve daily workflows while maintaining the highest standards of code quality.

---

## 📋 Table of Contents

- [About KeepInMind](#-about-keepinmind)
  - [Development Team](#-development-team)
  - [Development Process](#-development-process)
  - [Problem & Solution](#-problem--solution)
  - [Development Challenges](#-development-challenges)
  - [Key Features Delivered](#-key-features-delivered)
  - [What We Accomplished](#-what-we-accomplished)
  - [Future Development](#-future-development)
  - [Project Impact](#-project-impact)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Running Modes](#-running-modes)
  - [Classic Mode](#classic-mode)
  - [NLP Mode](#nlp-mode-ai-powered)
  - [Web UI Mode](#web-ui-mode-gradio)
- [Commands Reference](#-commands-reference)
  - [Using Quotes in Commands](#-using-quotes-in-commands)
- [MCP Integration](#-mcp-integration-claude-desktop)
- [Storage Options](#-storage-options)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)

---

## ✨ Features

### 📇 Contact Management
- **Multiple fields**: Names, phones, emails, addresses, birthdays
- **Smart search**: Fuzzy matching and exact search
- **Birthday reminders**: Track upcoming birthdays
- **Data validation**: International phone numbers, proper email format
- **Bulk operations**: Import/export contacts

### 📝 Notes & Tags
- **Rich notes**: Title and text with full-text search
- **Tag system**: Organize with multiple tags per note
- **Search**: By title, text content, or tags
- **Bulk operations**: Delete by title or tag

### 🤖 AI-Powered NLP
- **Natural language**: "add John with phone 1234567890"
- **Intent recognition**: ML-powered command understanding
- **Entity extraction**: Automatic detection of names, phones, emails
- **Hybrid approach**: ML models + rule-based fallback
- **34 intents**: Comprehensive command recognition

### 🔌 MCP Integration
- **Claude Desktop**: Use bot via AI assistant
- **39 MCP tools**: Full functionality exposed
- **Easy setup**: 3-minute configuration

---

## 🚀 Quick Start

### Prerequisites
```bash
# Required
Python 3.10 or higher
pip (Python package manager)

# Optional (for NLP mode)
8GB RAM (for ML models)
Apple Silicon or CUDA GPU (optional, for acceleration)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/kms-engineer/assistant-bot.git
cd assistant-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the bot (Classic Mode)
python3 -m src.presentation.cli.main

# Or run in NLP Mode (AI-powered)
python3 -m src.presentation.cli.main --nlp
```

### First Steps

```bash
# Add your first contact
add John 1234567890

# Add a birthday
add-birthday John 15.03.1990

# Create a note
add-note "Meeting" "Discuss project timeline"

# Show all contacts
all

# Show help
help
```

---

## 🎮 Running Modes

### Classic Mode

Traditional command-line interface with explicit commands.

**Start:**
```bash
python3 -m src.presentation.cli.main
```

**Usage:**
```bash
# Exact command syntax required
add John 1234567890
add-birthday John 15.03.1990
phone John
```

**Best for:**
- ✅ Fast execution
- ✅ Scripting and automation
- ✅ Low resource usage
- ✅ Offline use (no ML models needed)

---

### NLP Mode (AI-Powered)

Natural language interface powered by machine learning models.

**Start:**
```bash
python3 -m src.presentation.cli.main --nlp
```

**Usage:**
```bash
# Natural language - it understands context!
Add John with phone 1234567890
Set birthday for John 15.03.1990
Show me John's phone
Remove birthday from John
Search notes about meeting
```

**Features:**
- 🤖 Intent classification with DistilBERT
- 🔍 Named Entity Recognition (NER)
- 📊 Confidence scores
- 🔄 Automatic fallback to keyword matching
- 💬 Natural language understanding

**Best for:**
- ✅ Intuitive usage
- ✅ Fewer syntax errors
- ✅ Natural conversation flow
- ✅ Quick commands without memorizing syntax

**Requirements:**
```bash
# Additional dependencies for NLP (included in requirements.txt)
transformers>=4.30.0
torch>=2.0.0
scikit-learn>=1.0.0
```

**First Run:**
The first time you use NLP mode, it will download ML models (~400MB):
```
Downloading intent classifier model...
Downloading NER model...
Models loaded successfully!
```

---

### Web UI Mode (Gradio)

Modern web interface with visual controls and real-time updates.

**Start:**
```bash
python3 -m src.web.gradio_app
# or
python3 src/web/gradio_app.py
```

The interface will be available at http://localhost:7860

**Features:**
- 🌐 **Browser-based interface** with clean, modern design
- 📇 **Contact Management Tab**:
  - Add contacts with name and phone
  - Update email, address, and birthday
  - Search and view all contacts
  - Track upcoming birthdays with configurable date range
  - Delete contacts
- 📝 **Notes Management Tab**:
  - Create notes with optional tags
  - Add/remove tags to organize notes
  - Search by text content or tags
  - View all notes
  - Delete notes by ID
- 🎨 **Customizable Theme** with soft colors and modern styling
- 💾 **Auto-save** - all changes persist to JSON storage
- ✅ **Real-time feedback** with status messages

**Best for:**
- ✅ Visual interface preference
- ✅ Easier contact/note management
- ✅ No command memorization needed
- ✅ Intuitive UI for non-technical users
- ✅ Multi-tab organization

**Requirements:**
```bash
# Included in requirements.txt
gradio==5.49.1
```

**Storage:**
Data is automatically saved to `data/` directory in JSON format and synchronized with CLI modes.

---

## 📚 Commands Reference

### 🏠 General Commands

| Command | Description | Example |
|---------|-------------|---------|
| `hello` | Show greeting | `hello` |
| `help` | Show all commands | `help` |
| `clear` | Clear screen | `clear` |
| `exit` | Exit the bot | `exit` or `close` |

### 👥 Contact Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <name> <phone>` | Add new contact | `add John 1234567890` |
| `all` | Show all contacts | `all` |
| `change <name> <old> <new>` | Update phone | `change John 1234567890 0987654321` |
| `delete-contact <name>` | Delete contact | `delete-contact John` |
| `find <text>` | Exact search | `find John` |
| `phone <name>` | Show phone numbers | `phone John` |
| `remove-phone <name> <phone>` | Remove phone | `remove-phone John 1234567890` |
| `search <text>` | Fuzzy search | `search jo` |

### 📧 Email Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-email <name> <email>` | Add email | `add-email John john@example.com` |
| `edit-email <name> <email>` | Update email | `edit-email John new@example.com` |
| `remove-email <name>` | Remove email | `remove-email John` |

### 🏠 Address Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-address <name> <address>` | Add address | `add-address John "123 Main St"` |
| `edit-address <name> <address>` | Update address | `edit-address John "456 Oak Ave"` |
| `remove-address <name>` | Remove address | `remove-address John` |

### 🎂 Birthday Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-birthday <name> <date>` | Add birthday | `add-birthday John 15.03.1990` |
| `show-birthday <name>` | Show birthday | `show-birthday John` |
| `remove-birthday <name>` | Remove birthday | `remove-birthday John` |
| `birthdays <days>` | Upcoming birthdays | `birthdays 7` |

### 📝 Notes Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-note <title> <text>` | Create note | `add-note "Meeting" "Tomorrow at 3pm"` |
| `show-notes` | Show all notes | `show-notes` |
| `show-notes --sort-by-tag` | Show grouped by tags | `show-notes --sort-by-tag` |
| `show-note <id>` | Show specific note | `show-note a1b2c3d4...` |
| `rename-note <id> <title>` | Rename note | `rename-note a1b2c3d4 "New Title"` |
| `edit-note <id> <text>` | Edit note text | `edit-note a1b2c3d4 "Updated text"` |
| `delete-note <id>` | Delete by ID | `delete-note a1b2c3d4` |
| `delete-note-by-title <title>` | Delete by title | `delete-note-by-title "Meeting"` |
| `delete-note-by-tag <tag>` | Delete by tag | `delete-note-by-tag work` |

### 🏷️ Tag Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-tag <id> <tag>` | Add tag to note | `add-tag a1b2c3d4 work` |
| `remove-tag <id> <tag>` | Remove tag | `remove-tag a1b2c3d4 work` |
| `list-tags` | Show all tags | `list-tags` |

### 🔍 Search Commands

| Command | Description | Example |
|---------|-------------|---------|
| `search-notes <query>` | Search by text | `search-notes meeting` |
| `search-notes-by-title <query>` | Search by title | `search-notes-by-title Project` |
| `search-notes-by-tag <tag>` | Search by tag | `search-notes-by-tag work` |

### 💾 File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `save <filename>` | Save to file | `save my_contacts.db` |
| `load <filename>` | Load from file | `load my_contacts.db` |

---

### 💡 Using Quotes in Commands

You can use quotes (double `"` or single `'`) to pass arguments with spaces:

```bash
# With quotes - spaces are preserved
add-note "Groceries for weekend" "Buy salmon, eggs, oat milk, tomatoes"
search-notes-by-title "My Project"
rename-note abc123 "New Title with Spaces"
edit-note xyz789 "Updated text content"
delete-note-by-title "Old Note"

# Without quotes - only works for single-word arguments
add-note SimpleTitle SimpleText
search-notes-by-title Project
```

**Commands that support quotes:**
- `add-note <title> <text>` - Both title and text can contain spaces
- `search-notes-by-title <query>` - Search for titles with spaces
- `edit-note <id> <text>` - Text can contain spaces
- `rename-note <id> <title>` - New title can contain spaces
- `delete-note-by-title <title>` - Delete notes with spaces in title
- All other commands with text arguments

---

## 🔌 MCP Integration (Claude Desktop)

Connect the bot to Claude Desktop for AI-powered interactions.

### Setup (3 minutes)

**1. Create MCP configuration:**

```bash
# macOS/Linux
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**2. Add configuration:**

```json
{
  "mcpServers": {
    "assistant-bot": {
      "command": "python3",
      "args": ["-m", "src.web.server_stdio"],
      "cwd": "/absolute/path/to/assistant-bot"
    }
  }
}
```

**3. Replace the path:**
```bash
# Get your project path
pwd
# Copy the output and paste it in the config above
```

**4. Restart Claude Desktop**

### Running MCP Server

The MCP server can run in two modes:

**Automatic (via Claude Desktop):**
When you configure Claude Desktop as shown above, it automatically starts the MCP server when needed. No manual action required.

**Manual (for testing):**
You can also run the MCP server manually for testing or development:

```bash
# Run MCP server in stdio mode (for Claude Desktop integration)
python3 -m src.web.server_stdio

# Or run the standalone MCP server
python3 -m src.web.server
```

The server will start and wait for connections. Use Ctrl+C to stop it.

### Using with Claude

Now you can control the bot through Claude:

```
You: "Add a contact named Sarah with phone 555-1234"
Claude: I'll add that contact for you
Result: Contact added successfully

You: "Show all my contacts"
Claude: Here are your contacts: ...

You: "Create a note: Call Sarah tomorrow"
Claude: Note created with ID: ...
```

### Available MCP Tools (39 total)

- All contact management functions
- All note operations
- Search and filtering
- Tag management
- Birthday tracking
---

## 💾 Storage Options

### SQLite (Default)

**Best for**: Most users, reliable and fast

```bash
# Automatically uses SQLite
python3 -m src.presentation.cli.main

# Data saved to: ~/.assistant-bot/data/addressbook.db
```

**Pros:**
- ✅ Fast queries
- ✅ ACID compliance
- ✅ No setup needed
- ✅ Handles large datasets

### JSON

**Best for**: Human-readable data, version control

```python
# Configure in code
from src.infrastructure.storage import JsonStorage
storage = JsonStorage()
```

**Pros:**
- ✅ Easy to read
- ✅ Easy to edit manually
- ✅ Good for git
- ✅ Portable

### Pickle

**Best for**: Python-specific serialization

```python
from src.infrastructure.storage import PickleStorage
storage = PickleStorage()
```

**Pros:**
- ✅ Fast serialization
- ✅ Preserves Python objects
- ✅ Compact size

---

## 💡 Examples

### Complete Workflow

```bash
# Start the bot
python3 -m src.presentation.cli.main --nlp

# Add contacts
Add Alice with phone 5551234567
Add Bob with phone 5559876543

# Add details
Add birthday for Alice 15.05.1992
Add email alice@example.com to Alice
Add address 123 Main St to Bob

# Create notes
Add note "Team Meeting" "Discuss Q4 goals and timeline"
Add note "Shopping" "Buy groceries and office supplies"

# Organize with tags
Add tag <note-id> work
Add tag <note-id> urgent

# Search
Search contacts Alice
Search notes meeting
Show notes tagged work

# Birthday reminders
Show birthdays for next 30 days
```

### Automation Script

```bash
#!/bin/bash
# bulk_import.sh - Import contacts from file

while IFS=',' read -r name phone email birthday; do
  echo "add $name $phone" | python3 -m src.presentation.cli.main
  echo "add-email $name $email" | python3 -m src.presentation.cli.main
  echo "add-birthday $name $birthday" | python3 -m src.presentation.cli.main
done < contacts.csv
```

---

## 🏗️ Architecture

Built with **Domain-Driven Design** and **Clean Architecture**:

```
src/
├── domain/                 # Business Logic Layer
│   ├── entities/          # Contact, Note, Tag
│   ├── value_objects/     # Phone, Email, Birthday, Address
│   └── validators/        # Data validation rules
│
├── application/           # Application Layer
│   ├── services/         # ContactService, NoteService
│   └── commands/         # Command handlers
│
├── infrastructure/        # Infrastructure Layer
│   ├── storage/          # SQLite, JSON, Pickle
│   ├── persistence/      # Data access
│   └── serialization/    # Data serialization
│
└── presentation/         # Presentation Layer
    ├── cli/             # Command-line interface
    ├── nlp/             # NLP pipeline (ML models)
    └── web/             # MCP server

tests/                    # 500+ tests, 97% coverage
├── unit/                # Unit tests
├── integration/         # Integration tests
└── performance/         # Performance tests
```

### Design Principles

- ✅ **SOLID principles**
- ✅ **Dependency Inversion**
- ✅ **Separation of Concerns**
- ✅ **Type Safety** (100% type hints)
- ✅ **Testability** (97% coverage)

---

## 🛠️ Tech Stack

### Core
- **Python 3.10+** - Modern Python with type hints
- **SQLAlchemy 2.0** - ORM and database management
- **Colorama** - Terminal colors and formatting

### NLP & Machine Learning
- **Transformers (Hugging Face)** - ML models infrastructure
- **PyTorch 2.0+** - Deep learning framework
- **DistilBERT** - Intent classification model
- **Custom NER Model** - Entity extraction
- **scikit-learn** - ML utilities and metrics

### Data Validation
- **phonenumbers** - International phone validation
- **email-validator** - RFC-compliant email validation
- **python-dateutil** - Flexible date parsing

### Testing
- **pytest** - Testing framework
- **pytest-cov** - Code coverage
- **unittest.mock** - Test mocking

### Integration
- **FastMCP 2.13.0** - Model Context Protocol server

### Statistics
- 📊 **15,000+ lines** of code
- 🧪 **500+ tests** with 97% coverage
- 🤖 **34 NLP intents** supported
- 🔧 **39 MCP tools** exposed
- 📦 **4 architectural layers**

---

## 🧪 Development

### Run Tests

```bash
# All tests
python3 -m pytest

# With coverage
python3 -m pytest --cov=src --cov-report=html

# Specific test file
python3 -m pytest tests/domain/entities/test_contact.py -v

# NLP tests only
python3 -m pytest tests/presentation/nlp/ -v
```

### Code Quality

```bash
# Type checking
mypy src/

# Linting
pylint src/

# Format code
black src/
```

### Training ML Models

```bash
# Train models
python3 scripts/train_multitask_classifier.py
python3 scripts/train_ner_model.py
```

---

## 📖 Documentation

- [MCP Integration Guide](docs/MCP_INTEGRATION_GUIDE.md) - Claude Desktop setup
- [Architecture Diagram](ARCHITECTURE_DIAGRAM.md) - System design
- [Tech Stack Details](TECH_STACK.md) - Complete technology list
- [Project Summary](PROJECT_SUMMARY.md) - Project overview

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Write tests** for new functionality
4. **Ensure** all tests pass (`pytest`)
5. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
6. **Push** to branch (`git push origin feature/AmazingFeature`)
7. **Open** a Pull Request

### Code Standards
- ✅ Type hints required
- ✅ Tests required (maintain 97%+ coverage)
- ✅ Follow existing architecture
- ✅ Clean code principles
- ✅ Docstrings for public APIs

---

## 📝 Data Validation

### Names
- **Length**: 2-50 characters
- **Characters**: Letters, spaces, hyphens, apostrophes
- **International**: Full Unicode support (José, François, etc.)

### Phone Numbers
- **Format**: 10 digits (US format)
- **Auto-normalized**: Strips formatting automatically
- **Validation**: Uses `phonenumbers` library

### Emails
- **Standard**: RFC 5322 compliant
- **Domain check**: Valid domain structure
- **Library**: `email-validator`

### Birthdays
- **Format**: DD.MM.YYYY
- **Range**: 1900-current year
- **Flexible**: Supports multiple input formats

### Addresses
- **Length**: 5-200 characters
- **Content**: Letters, numbers, punctuation
- **Validation**: Non-empty, meaningful content

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

**You are free to:**
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Sublicense
- ✅ Private use

---

## 🙏 Acknowledgments

Built by developers who believe in:
- 🎯 **Clean code** over clever code
- 📐 **Architecture** over quick hacks
- 🧪 **Testing** over hope
- 📖 **Documentation** over assumptions
- 🤝 **Collaboration** over ego

No enterprise bloat. No buzzwords. Just solid engineering.

---

## 🆘 Troubleshooting

### NLP Mode Issues

**Problem**: Models not loading
```bash
# Solution: Clear cache and re-download
rm -rf ~/.cache/huggingface/
python3 -m src.presentation.cli.main --nlp
```

**Problem**: Out of memory
```bash
# Solution: Use classic mode or increase RAM
python3 -m src.presentation.cli.main  # Classic mode uses <100MB
```

### Database Issues

**Problem**: Database schema errors
```bash
# Solution: Delete old database (data will be lost)
rm ~/.assistant-bot/data/addressbook.db
python3 -m src.presentation.cli.main
```

### MCP Issues

**Problem**: Claude Desktop can't find bot
```bash
# Solution 1: Check path in config
pwd  # Copy this exact path to claude_desktop_config.json

# Solution 2: Use absolute path
"cwd": "/Users/yourname/path/to/assistant-bot"

# Solution 3: Test stdio manually
python3 -m src.web.server_stdio
```

---

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/kms-engineer/assistant-bot/issues)
---

<div align="center">

**⭐ Star us on GitHub if you find this useful!**

[Report Bug](https://github.com/kms-engineer/assistant-bot/issues) · [Request Feature](https://github.com/kms-engineer/assistant-bot/discussions) · [Documentation](docs/)

Made with ❤️ by developers who care about code quality

</div>
