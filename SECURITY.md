# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of our project seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, report security issues privately by using GitHub's [private vulnerability reporting](https://github.com/kms-engineer/assistant-bot/security/advisories/new) feature.

### What to Include

When reporting a vulnerability, please provide:

- **Description**: Clear explanation of the vulnerability
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Impact**: What an attacker could potentially do
- **Affected versions**: Which versions are affected
- **Suggested fix**: If you have ideas on how to fix it (optional)

### What to Expect

- **Acknowledgment**: We'll acknowledge your report within 48 hours
- **Updates**: We'll keep you informed about our progress
- **Timeline**: We aim to resolve critical issues within 7 days
- **Credit**: We'll credit you in the security advisory (unless you prefer to remain anonymous)

## AI and Code Security

### When Using AI Tools
If you're using AI assistants (like ChatGPT, Claude, GitHub Copilot) to contribute:

- **Don't share sensitive data**: Never paste real contact data, emails, or personal information into AI prompts
- **Review AI-generated code**: Always review and test AI-generated code before committing
- **Input validation**: AI-generated validators should be thoroughly tested for edge cases
- **Security patterns**: Verify that AI suggestions follow security best practices
- **Dependencies**: Check that AI-recommended packages are legitimate and maintained

### Code Review for AI Contributions
When reviewing AI-assisted PRs:

- Verify input validation is comprehensive
- Check for injection vulnerabilities (SQL, command injection)
- Ensure error messages don't leak sensitive information
- Test with malicious inputs and edge cases
- Confirm regex patterns are secure and don't cause ReDoS

## Security Best Practices

When using this project:

### Data Storage
- **Local storage only**: This bot stores all data locally - no cloud sync
- **File permissions**: Ensure your data files have appropriate permissions
- **Sensitive data**: Be cautious about storing sensitive information in contacts or notes

### Database Security
- **SQLite files**: Protect your `.db` files with proper file system permissions
- **Backups**: Keep backups of your data in secure locations
- **Access control**: Don't share your database files publicly

### Running the Application
- **Dependencies**: Keep dependencies updated (`pip install -r requirements.txt --upgrade`)
- **Python version**: Use supported Python versions (3.10+)
- **Isolation**: Consider using virtual environments

## Known Limitations

This is a CLI application designed for personal use:

- **No authentication**: The app doesn't have user authentication (it's single-user)
- **No encryption**: Data is stored in plain text by default
- **Local only**: No network security concerns as it doesn't make external connections

## Security Updates

We'll announce security updates through:
- GitHub Security Advisories
- Release notes
- Repository README

## Scope

This security policy applies to:
- Core application code in the `src/` directory
- Data validation and storage mechanisms
- Dependencies listed in `requirements.txt`

**Out of scope:**
- User-specific configurations
- Third-party integrations or modifications
- Deployment environments

---

Thank you for helping keep our project and users safe!
