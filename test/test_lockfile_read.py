import unittest

from js_dependency_audit.lock_file_content import LockFileContent
from js_dependency_audit.security_audit_request import request_security_audit


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lock_file_content = LockFileContent.from_yarn_file("files/yarn.lock")

        self.assertIsNotNone(
            lock_file_content, "Lock file content shouldn't be None"
        )  # add assertion here

        audit_data = request_security_audit(lock_file_content)

        self.assertEqual(
            audit_data.metadata.dependencies,
            401,
            f"401 dependencies expected, found {audit_data.metadata.dependencies}",
        )


if __name__ == "__main__":
    unittest.main()
