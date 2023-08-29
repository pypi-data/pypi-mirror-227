# make this directory a package
import unittest

import grokcore.content.tests.test_container
import grokcore.content.tests.test_container_event
import grokcore.content.tests.test_orderedcontainer
import grokcore.content.tests.test_verify_containers


def collect_tests():
    """Combine all test suites to have one entry point."""
    return unittest.TestSuite((
        grokcore.content.tests.test_container.test_suite(),
        grokcore.content.tests.test_container_event.test_suite(),
        grokcore.content.tests.test_orderedcontainer.test_suite(),
        grokcore.content.tests.test_verify_containers.test_suite(),
    ))
