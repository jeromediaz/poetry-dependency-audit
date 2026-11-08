# POETRY-DEPENDENCY-AUDIT

[![PyPI - License](https://img.shields.io/pypi/l/poetry-dependency-audit)](https://pypi.org/project/poetry-dependency-audit/)
[![PyPI - Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fjeromediaz%2Fpoetry-dependency-audit%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://pypi.org/project/poetry-dependency-audit/)
[![PyPI - Version](https://img.shields.io/pypi/v/poetry-dependency-audit)](https://pypi.org/project/poetry-dependency-audit/)

A library to help perform a security audit check using a poetry lock file.

Not intended to be used as a standalone tool, but as part of a system
periodically checking for vulnerabilities.

## Usage

```python
from poetry_dependency_audit.lock_file_content import LockFileContent
from poetry_dependency_audit.security_audit_request import request_security_audit

lock_file_content = LockFileContent.from_poetry_file("poetry.lock", "pyproject.toml")
audit_data = request_security_audit(lock_file_content)

print(f"{audit_data.dependencies} dependencies audited")
for name, vulnerabilities in audit_data.vulnerable_packages.items():
    for vulnerability in vulnerabilities:
        print(f"{name}: {vulnerability.id} - {vulnerability.summary}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jeromediaz/poetry-dependency-audit/blob/main/LICENSE) file for details.
