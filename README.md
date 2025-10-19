# Personal Assistant Bot 🤖

Your go-to CLI companion for managing contacts and notes without the bloat. Built with Python and clean architecture because we actually care about maintainable code.

## Why This Exists

Managing contacts shouldn't require opening 5 browser tabs. This CLI tool gets the job done fast, stores everything locally, and doesn't send your data to some random cloud server. Plus, it's actually fun to use.

## What It Does

### Contact Management 📇
- Store contacts with names, multiple phone numbers, emails, addresses, and birthdays
- Smart search that actually works (fuzzy matching included)
- Birthday reminders so you don't forget important dates
- Proper validation because nobody wants "12345" as a phone number

### Notes 📝
- Quick note creation with simple commands
- Edit and delete notes by ID
- Everything persists automatically - no "are you sure you want to save?" nonsense

### Storage Options 💾
Choose your storage backend:
- **SQLite** (default) - reliable and fast
- **JSON** - human-readable if you want to peek at your data
- **Pickle** - because sometimes you just need to serialize Python objects

## Quick Start

### Requirements
- Python 3.10+
- SQLAlchemy 2.0.4

### Installation

```bash
# Clone it
git clone https://github.com/kms-engineer/assistant-bot.git
cd assistant-bot

# Install dependencies
pip install -r requirements.txt

# Run it
python3 -m src.presentation.cli.main
```

That's it. No Docker, no Kubernetes, no 47-step setup process.

## How to Use

### Contacts
```bash
# Add someone
add Oksana 1234567890

# Add more info
add-birthday Oksana 15.03.1990
add-email Oksana oksana@example.com
add-address Oksana 123 Main Street, City

# Update stuff
change Oksana 1234567890 0987654321
edit-email Oksana oksana@example.com

# Find people
phone Oksana                  # Get Oksana's numbers
search oksana                 # Fuzzy search
birthdays 7                   # Upcoming birthdays
```

### Notes
```bash
add-note Remember to buy groceries
show-notes
edit-note 1 Buy groceries and cook dinner
delete-note 1
```

### Storage
```bash
save my_contacts.db          # Manual save
load my_contacts.db          # Load from file
```

## Validation (Because We Care About Data Quality)

**Names**
- 2-50 characters
- Letters, spaces, hyphens only
- International chars supported (José, María, etc.)

**Phone Numbers**
- Exactly 10 digits
- Auto-normalized (we strip the formatting for you)

**Addresses**
- 5-200 characters
- Letters, numbers, and basic punctuation
- Actually has to contain something meaningful

**Email**
- Standard format validation
- No, "test@test" won't work

## Architecture

Built with Domain-Driven Design because we're not savages:

```
src/
├── domain/              # Business logic lives here
├── application/         # Use cases and commands
├── infrastructure/      # Storage and external stuff
└── presentation/        # CLI interface
```

Clean separation of concerns, type hints everywhere, and validators that actually validate. You know, the basics.

## Tech Stack

- Python 3.10+
- SQLAlchemy for database stuff
- Zero frontend frameworks (it's a CLI, remember?)
- Pure Python - no unnecessary dependencies

## Contributing

PRs welcome! Just keep it clean, write tests, and don't break the architecture. We're trying to build something maintainable here.

## License

Apache 2.0 - Do whatever you want with it, just don't blame us if something breaks.

---

Built by developers who believe code should be clean, simple, and actually work. No enterprise bloat, no buzzwords, just solid engineering.