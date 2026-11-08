import unittest

from poetry_dependency_audit.lock_file_content import LockFileContent
from poetry_dependency_audit.security_audit_request import request_security_audit


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lock_file_content = LockFileContent.from_poetry_file(
            "files/poetry.lock", "files/pyproject.toml"
        )

        self.assertIsNotNone(
            lock_file_content, "Lock file content shouldn't be None"
        )

        self.assertEqual(
            lock_file_content.count,
            12,
            f"12 dependencies expected, found {lock_file_content.count}",
        )

    def test_audit(self):
        lock_file_content = LockFileContent.from_poetry_file(
            "files/poetry.lock", "files/pyproject.toml"
        )

        audit_data = request_security_audit(lock_file_content)

        self.assertEqual(
            audit_data.dependencies,
            12,
            f"12 dependencies expected, found {audit_data.dependencies}",
        )

        self.assertIn("django", audit_data.packages)


if __name__ == "__main__":
    unittest.main()
