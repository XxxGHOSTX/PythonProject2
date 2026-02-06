"""
Comprehensive tests for DefaultValidator and Agent validation logic.

Tests cover:
- Payload size validation
- Reserved keys validation
- JSON-serializable type validation
- String length validation
- Nesting depth validation
- Payload transformation
"""

import sys
from typing import Any, Dict

# Import the classes we need to test
from thalos_coding_agent_core import DefaultValidator, ThalosAgent, Config


class TestDefaultValidator:
    """Test suite for DefaultValidator class."""
    
    def __init__(self):
        self.validator = DefaultValidator()
        self.passed = 0
        self.failed = 0
        
    def run_test(self, test_name: str, test_func):
        """Run a single test and track results."""
        try:
            test_func()
            print(f"✓ {test_name}")
            self.passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            self.failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error - {e}")
            self.failed += 1
    
    def assert_raises(self, exception_type, func, *args, **kwargs):
        """Assert that a function raises a specific exception."""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} but no exception was raised")
        except exception_type:
            pass  # Expected behavior
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__} but got {type(e).__name__}: {e}")
    
    def test_valid_payload(self):
        """Test that valid payloads pass validation."""
        valid_payloads = [
            {"key": "value"},
            {"number": 42, "float": 3.14, "bool": True, "null": None},
            {"list": [1, 2, 3], "tuple": (4, 5, 6)},
            {"nested": {"deep": {"data": "value"}}},
            {"empty": {}},
        ]
        
        for payload in valid_payloads:
            self.validator.validate(payload)
    
    def test_non_dict_payload(self):
        """Test that non-dict payloads are rejected."""
        invalid_payloads = ["string", 123, [1, 2, 3], None, True]
        
        for payload in invalid_payloads:
            self.assert_raises(TypeError, self.validator.validate, payload)
    
    def test_payload_size_limit(self):
        """Test that oversized payloads are rejected."""
        # Create payload with exactly MAX_PAYLOAD_SIZE keys (should pass)
        large_payload = {f"key_{i}": i for i in range(1000)}
        self.validator.validate(large_payload)
        
        # Create payload exceeding MAX_PAYLOAD_SIZE (should fail)
        oversized_payload = {f"key_{i}": i for i in range(1001)}
        self.assert_raises(ValueError, self.validator.validate, oversized_payload)
    
    def test_reserved_keys(self):
        """Test that reserved keys are rejected."""
        reserved_keys = ['_meta', '_internal', '_system']
        
        for key in reserved_keys:
            payload = {key: "value"}
            self.assert_raises(ValueError, self.validator.validate, payload)
        
        # Multiple reserved keys
        payload = {"_meta": "value", "_internal": "value"}
        self.assert_raises(ValueError, self.validator.validate, payload)
        
        # Mixed with valid keys
        payload = {"valid_key": "value", "_meta": "reserved"}
        self.assert_raises(ValueError, self.validator.validate, payload)
    
    def test_json_serializable_types(self):
        """Test that only JSON-serializable types are allowed."""
        # Valid types
        valid_payload = {
            "string": "text",
            "int": 42,
            "float": 3.14,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "tuple": (4, 5, 6),
            "dict": {"nested": "value"}
        }
        self.validator.validate(valid_payload)
        
        # Invalid types
        class CustomClass:
            pass
        
        invalid_payloads = [
            {"custom": CustomClass()},
            {"set": {1, 2, 3}},
            {"bytes": b"data"},
        ]
        
        for payload in invalid_payloads:
            self.assert_raises(ValueError, self.validator.validate, payload)
    
    def test_non_string_keys(self):
        """Test that non-string keys are rejected."""
        # Note: In Python, dict keys can be various types, but we require strings
        # This is a bit tricky to test since dict literals won't accept non-string keys easily
        # We'll create a dict programmatically
        payload = {"valid": "value"}
        payload[123] = "numeric_key"
        self.assert_raises(ValueError, self.validator.validate, payload)
    
    def test_string_length_limit(self):
        """Test that excessively long strings are rejected."""
        # String at limit (should pass)
        max_string = "x" * 100000
        payload = {"key": max_string}
        self.validator.validate(payload)
        
        # String exceeding limit (should fail)
        too_long = "x" * 100001
        payload = {"key": too_long}
        self.assert_raises(ValueError, self.validator.validate, payload)
    
    def test_nesting_depth_limit(self):
        """Test that deeply nested structures are rejected."""
        # Create nested dict at maximum depth (should pass)
        payload = {"level0": {}}
        current = payload["level0"]
        for i in range(1, 10):
            current[f"level{i}"] = {}
            current = current[f"level{i}"]
        self.validator.validate(payload)
        
        # Create nested dict exceeding maximum depth (should fail)
        payload = {"level0": {}}
        current = payload["level0"]
        for i in range(1, 11):
            current[f"level{i}"] = {}
            current = current[f"level{i}"]
        self.assert_raises(ValueError, self.validator.validate, payload)
    
    def test_nested_list_validation(self):
        """Test that nested lists with dicts are validated."""
        # Valid nested structure
        valid_payload = {
            "items": [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"}
            ]
        }
        self.validator.validate(valid_payload)
        
        # Invalid nested structure (non-JSON type in list)
        class CustomClass:
            pass
        
        invalid_payload = {
            "items": [CustomClass()]
        }
        self.assert_raises(ValueError, self.validator.validate, invalid_payload)
    
    def test_nested_dict_validation(self):
        """Test that nested dicts are validated recursively."""
        # Valid deeply nested
        valid_payload = {
            "outer": {
                "middle": {
                    "inner": "value"
                }
            }
        }
        self.validator.validate(valid_payload)
        
        # Invalid nested (reserved key deep inside)
        invalid_payload = {
            "outer": {
                "middle": {
                    "_internal": "reserved"
                }
            }
        }
        self.assert_raises(ValueError, self.validator.validate, invalid_payload)
    
    def run_all_tests(self):
        """Run all test methods."""
        print("\n" + "="*60)
        print("Running DefaultValidator Tests")
        print("="*60 + "\n")
        
        # Get all test methods
        test_methods = [
            ("Valid payload", self.test_valid_payload),
            ("Non-dict payload", self.test_non_dict_payload),
            ("Payload size limit", self.test_payload_size_limit),
            ("Reserved keys", self.test_reserved_keys),
            ("JSON-serializable types", self.test_json_serializable_types),
            ("Non-string keys", self.test_non_string_keys),
            ("String length limit", self.test_string_length_limit),
            ("Nesting depth limit", self.test_nesting_depth_limit),
            ("Nested list validation", self.test_nested_list_validation),
            ("Nested dict validation", self.test_nested_dict_validation),
        ]
        
        for test_name, test_func in test_methods:
            self.run_test(test_name, test_func)
        
        print("\n" + "="*60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("="*60 + "\n")
        
        return self.failed == 0


class TestAgent:
    """Test suite for ThalosAgent class."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name: str, test_func):
        """Run a single test and track results."""
        try:
            test_func()
            print(f"✓ {test_name}")
            self.passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            self.failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error - {e}")
            self.failed += 1
    
    def test_agent_execution(self):
        """Test that agent executes successfully with valid payload."""
        config = Config(mode="test", debug=True)
        agent = ThalosAgent(config)
        
        payload = {"test_key": "test_value"}
        result = agent.execute(payload)
        
        assert result["status"] == "success"
        assert "payload" in result
        assert "metadata" in result
        assert result["metadata"]["mode"] == "test"
        assert result["metadata"]["debug"] is True
        assert result["metadata"]["keys_processed"] == 1
    
    def test_agent_validation_failure(self):
        """Test that agent properly handles validation failures."""
        config = Config(mode="test", debug=True)
        agent = ThalosAgent(config)
        
        # Invalid payload (reserved key)
        payload = {"_meta": "reserved"}
        
        try:
            agent.execute(payload)
            raise AssertionError("Expected ValueError but execution succeeded")
        except ValueError:
            pass  # Expected
    
    def test_transform_payload(self):
        """Test that _transform_payload returns payload unchanged by default."""
        config = Config(mode="test", debug=True)
        agent = ThalosAgent(config)
        
        payload = {"key": "value", "nested": {"data": 123}}
        transformed = agent._transform_payload(payload)
        
        assert transformed == payload
        assert transformed is payload  # Should be same object (no copy)
    
    def run_all_tests(self):
        """Run all test methods."""
        print("\n" + "="*60)
        print("Running Agent Tests")
        print("="*60 + "\n")
        
        test_methods = [
            ("Agent execution", self.test_agent_execution),
            ("Agent validation failure", self.test_agent_validation_failure),
            ("Transform payload", self.test_transform_payload),
        ]
        
        for test_name, test_func in test_methods:
            self.run_test(test_name, test_func)
        
        print("\n" + "="*60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("="*60 + "\n")
        
        return self.failed == 0


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("COMPREHENSIVE VALIDATION TEST SUITE")
    print("="*60)
    
    # Run DefaultValidator tests
    validator_tests = TestDefaultValidator()
    validator_success = validator_tests.run_all_tests()
    
    # Run Agent tests
    agent_tests = TestAgent()
    agent_success = agent_tests.run_all_tests()
    
    # Overall summary
    total_passed = validator_tests.passed + agent_tests.passed
    total_failed = validator_tests.failed + agent_tests.failed
    
    print("="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    print(f"Total tests passed: {total_passed}")
    print(f"Total tests failed: {total_failed}")
    print("="*60)
    
    if validator_success and agent_success:
        print("\n✓ ALL TESTS PASSED!\n")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED!\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
