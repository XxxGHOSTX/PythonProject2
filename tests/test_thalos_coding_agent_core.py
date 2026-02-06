"""
Tests for thalos_coding_agent_core.py code generation features.

This test suite validates the enhanced validation functionality added in PR #1:
- Generated code contains reserved keys validation
- Generated code contains payload size validation  
- Generated code contains value types validation
- Generated code contains nesting depth validation
- Generated code contains transform payload functionality
- Python comment syntax (# not //) in generated code
"""

import pytest
from thalos_coding_agent_core import (
    ThalosCodingAgentCore,
    GenerationMode,
    CodeRequest,
    CodeArtifact
)


class TestCodeGeneration:
    """Test suite for code generation with PR #1 enhancements."""
    
    def test_generated_code_has_reserved_keys_validation(self):
        """Test that generated code includes RESERVED_KEYS constant."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "RESERVED_KEYS" in artifact.code
        assert "'_meta'" in artifact.code or '"_meta"' in artifact.code
        assert "'_internal'" in artifact.code or '"_internal"' in artifact.code
        assert "'_system'" in artifact.code or '"_system"' in artifact.code
    
    def test_generated_code_has_payload_size_validation(self):
        """Test that generated code includes MAX_PAYLOAD_SIZE constant and validation."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "MAX_PAYLOAD_SIZE" in artifact.code
        assert "_validate_payload_size" in artifact.code
    
    def test_generated_code_has_string_length_validation(self):
        """Test that generated code includes MAX_STRING_LENGTH constant."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "MAX_STRING_LENGTH" in artifact.code
    
    def test_generated_code_has_nesting_depth_validation(self):
        """Test that generated code includes MAX_NESTING_DEPTH constant and validation."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "MAX_NESTING_DEPTH" in artifact.code
        assert "_validate_nesting_depth" in artifact.code
    
    def test_generated_code_has_value_types_validation(self):
        """Test that generated code includes value type validation."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "_validate_value_types" in artifact.code
        assert "JSON_TYPES" in artifact.code or "JSON-serializable" in artifact.code
    
    def test_generated_code_has_transform_payload_method(self):
        """Test that generated code includes _transform_payload helper method."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "_transform_payload" in artifact.code
    
    def test_generated_code_has_improved_process_method(self):
        """Test that generated code has enhanced _process method with metadata."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        # Check for metadata structure in result
        assert '"metadata"' in artifact.code or "'metadata'" in artifact.code
        assert "keys_processed" in artifact.code
    
    def test_generated_code_uses_python_comments_not_cpp(self):
        """Test that generated code uses Python # comments, not // comments."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        # Should have Python comments - check for domain-specific text which has comments
        assert "domain-specific" in artifact.code.lower()
        
        # Should have many # comments (Python style)
        assert artifact.code.count('#') > 10
        
        # Should NOT have C++/JavaScript style comments in Python code
        # Note: We're checking the actual code, not string literals
        lines = artifact.code.split('\n')
        for line in lines:
            stripped = line.strip()
            # Skip empty lines and triple-quoted strings
            if not stripped or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            # If line starts with //, it's wrong (but we need to exclude URLs and such)
            if stripped.startswith('//') and not 'http://' in line and not 'https://' in line:
                pytest.fail(f"Found C++ style comment in Python code: {line}")
    
    def test_generated_code_has_reserved_keys_check_method(self):
        """Test that generated code includes _validate_reserved_keys method."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a module with validation",
            mode=GenerationMode.FULL_APPLICATION,
            language="python",
            complexity=5,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert "_validate_reserved_keys" in artifact.code
    
    def test_code_artifact_structure(self):
        """Test that generated artifact has all required fields."""
        agent = ThalosCodingAgentCore()
        request = CodeRequest(
            query="Create a simple function",
            mode=GenerationMode.FUNCTION,
            language="python",
            complexity=3,
            attached_files=[]
        )
        
        artifact = agent.generate(request)
        
        assert isinstance(artifact, CodeArtifact)
        assert isinstance(artifact.code, str)
        assert isinstance(artifact.tests, str)
        assert isinstance(artifact.documentation, str)
        assert isinstance(artifact.complexity_analysis, str)
        assert len(artifact.code) > 0


class TestAgentCore:
    """Test suite for ThalosCodingAgentCore basic functionality."""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        agent = ThalosCodingAgentCore()
        assert agent.version == "8.0"
    
    def test_generate_code_wrapper(self):
        """Test the generate_code wrapper method."""
        agent = ThalosCodingAgentCore()
        
        result = agent.generate_code(
            query="Create a validation function",
            language="python",
            complexity=5
        )
        
        assert "code" in result
        assert "language" in result
        assert "complexity" in result
    
    def test_different_generation_modes(self):
        """Test that different modes generate appropriate code."""
        agent = ThalosCodingAgentCore()
        
        modes = [
            GenerationMode.FUNCTION,
            GenerationMode.CLASS,
            GenerationMode.API,
            GenerationMode.FULL_APPLICATION
        ]
        
        for mode in modes:
            request = CodeRequest(
                query="Create test code",
                mode=mode,
                language="python",
                complexity=5,
                attached_files=[]
            )
            
            artifact = agent.generate(request)
            assert len(artifact.code) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
