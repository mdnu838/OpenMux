# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## 🚨 Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them privately by:

1. **Email**: mdnu08@gmail.com
2. **GitHub Security Advisories**: Use the "Security" tab in this repository

### What to Include

When reporting a vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact and severity
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Proof of Concept**: Code or example demonstrating the vulnerability
- **Suggested Fix**: If you have one (optional)
- **Environment**: 
  - OpenMux version
  - Python version
  - Operating system

### What to Expect

- **Response Time**: We aim to respond within 48 hours
- **Updates**: Regular updates on the status of your report
- **Disclosure**: Coordinated disclosure after patch is available
- **Credit**: Recognition in release notes (if desired)

## 🛡️ Security Best Practices

### For Users

1. **Never commit API keys**:
   ```bash
   # Always use .env file
   cp .env.example .env
   # Edit .env with your keys
   # .env is already in .gitignore
   ```

2. **Keep dependencies updated**:
   ```bash
   uv pip install --upgrade openmux
   ```

3. **Use environment variables**:
   ```python
   import os
   api_key = os.getenv("OPENROUTER_API_KEY")  # Good
   api_key = "sk-123456"  # Bad - never hardcode!
   ```

4. **Validate inputs**:
   ```python
   from openmux import Orchestrator
   
   # Validate user input before processing
   if len(user_query) > 10000:
       raise ValueError("Query too long")
   
   orchestrator.process(user_query)
   ```

5. **Review permissions**:
   - Only grant necessary API permissions
   - Use read-only tokens when possible
   - Rotate API keys regularly

### For Contributors

1. **Never commit secrets**:
   - API keys
   - Passwords
   - Tokens
   - Private keys
   - Certificates

2. **Use `.env` for local development**:
   ```bash
   # .env is already in .gitignore
   # Use .env.example as template
   ```

3. **Review dependencies**:
   ```bash
   # Check for known vulnerabilities
   uv pip freeze | safety check --stdin
   ```

4. **Run security checks**:
   ```bash
   # Static security analysis
   bandit -r openmux/ -ll
   ```

5. **Follow secure coding practices**:
   - Validate all inputs
   - Use parameterized queries
   - Avoid eval() and exec()
   - Handle errors gracefully
   - Log security events

## 🔍 Security Scanning

### Automated Scans

Our CI/CD pipeline includes:

- **Bandit**: Static security analysis
- **Safety**: Dependency vulnerability checks
- **CodeQL**: Advanced code analysis (coming soon)

### Manual Review

- All PRs reviewed for security issues
- Regular dependency audits
- Periodic security assessments

## 📜 Known Security Considerations

### API Key Storage

- **Risk**: API keys in `.env` file
- **Mitigation**: `.env` is in `.gitignore`, documented extensively
- **Recommendation**: Use system keyring for production

### External API Calls

- **Risk**: Data sent to external APIs
- **Mitigation**: HTTPS only, documented data flow
- **Recommendation**: Review provider privacy policies

### Dependency Security

- **Risk**: Vulnerabilities in dependencies
- **Mitigation**: Regular updates, automated scanning
- **Recommendation**: Keep dependencies up-to-date

## 🔐 Encryption

- All API communications use HTTPS/TLS
- API keys transmitted securely
- No local storage of sensitive data

## 📋 Security Checklist

### Before Committing

- [ ] No API keys or secrets in code
- [ ] `.env` file not tracked
- [ ] No sensitive data in logs
- [ ] Input validation implemented
- [ ] Error messages don't leak info

### Before Deploying

- [ ] All dependencies updated
- [ ] Security scan passed
- [ ] API keys rotated
- [ ] HTTPS enforced
- [ ] Logging configured

## 🆘 Security Incident Response

If a security incident occurs:

1. **Contain**: Stop the immediate threat
2. **Assess**: Determine scope and impact
3. **Notify**: Inform affected users
4. **Fix**: Deploy patches quickly
5. **Learn**: Update practices

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)

## 📞 Contact

For security concerns, contact:
- **GitHub Security**: Use "Security" tab
- **Email**: mdnu08@gmail.com

---

**Last Updated**: November 9, 2025
