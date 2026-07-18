import pytest
import random
from evenness_input import EvennessInput
from evenness_output import EvennessOutput
from evenness_calculator import EvennessCalculator


class TestEvennessCalculator:
    """Pytest test suite for the Evenness Calculator"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixture that runs before each test"""
        self.calculator = EvennessCalculator()
        self.test_strings = ["test", "hello", "python", "bit", "magic", "complex"]
    
    @pytest.mark.parametrize("num_tests", [10])
    def test_random_evenness(self, num_tests):
        """Test evenness calculation with random numbers"""
        for i in range(num_tests):
            test_num = random.randint(-1000, 1000)
            test_str = random.choice(self.test_strings)
            expected_even = test_num % 2 == 0
            
            input_data = EvennessInput(number=test_num, magic_string=test_str)
            output = self.calculator.calculate(input_data)
            
            assert output.is_even == expected_even, \
                f"Test {i+1} FAILED: Number={test_num}, String='{test_str}', " \
                f"Expected even={expected_even}, Got={output.is_even}"
    
    @pytest.mark.parametrize("number,magic_string,expected_even", [
        (0, "zero", True),
        (1, "one", False),
        (-2, "negative", True),
        (-1, "neg_one", False),
        (42, "answer", True),
        (1000000, "big", True),
        (7, "seven", False),
        (-100, "neg_hundred", True),
        (2**31, "max_int", True),
        (2**31 - 1, "max_int_odd", False),
    ])
    def test_specific_numbers(self, number, magic_string, expected_even):
        """Test evenness calculation with specific edge cases"""
        input_data = EvennessInput(number=number, magic_string=magic_string)
        output = self.calculator.calculate(input_data)
        
        assert output.is_even == expected_even, \
            f"FAILED: Number={number}, String='{magic_string}', " \
            f"Expected even={expected_even}, Got={output.is_even}"
    
    def test_zero_evenness(self):
        """Test that zero is correctly identified as even"""
        input_data = EvennessInput(number=0, magic_string="zero_test")
        output = self.calculator.calculate(input_data)
        
        assert output.is_even == True, "Zero should be even"
        assert output.lsb_value == 0, "LSB of zero should be 0"
    
    def test_negative_even_numbers(self):
        """Test negative even numbers"""
        for num in [-2, -4, -10, -100]:
            input_data = EvennessInput(number=num, magic_string="negative_even")
            output = self.calculator.calculate(input_data)
            assert output.is_even == True, f"{num} should be even"
    
    def test_negative_odd_numbers(self):
        """Test negative odd numbers"""
        for num in [-1, -3, -7, -99]:
            input_data = EvennessInput(number=num, magic_string="negative_odd")
            output = self.calculator.calculate(input_data)
            assert output.is_even == False, f"{num} should be odd"
    
    def test_large_even_numbers(self):
        """Test large even numbers"""
        large_evens = [10**6, 2**20, 10**9 + 2]
        for num in large_evens:
            input_data = EvennessInput(number=num, magic_string="large_even")
            output = self.calculator.calculate(input_data)
            assert output.is_even == True, f"{num} should be even"
    
    def test_large_odd_numbers(self):
        """Test large odd numbers"""
        large_odds = [10**6 + 1, 2**20 - 1, 10**9 + 3]
        for num in large_odds:
            input_data = EvennessInput(number=num, magic_string="large_odd")
            output = self.calculator.calculate(input_data)
            assert output.is_even == False, f"{num} should be odd"
    
    def test_output_structure(self):
        """Test that the output has all required fields"""
        input_data = EvennessInput(number=42, magic_string="test")
        output = self.calculator.calculate(input_data)
        
        assert hasattr(output, 'is_even'), "Output should have 'is_even' attribute"
        assert hasattr(output, 'computation_steps'), "Output should have 'computation_steps' attribute"
        assert hasattr(output, 'magic_string_used'), "Output should have 'magic_string_used' attribute"
        assert hasattr(output, 'lsb_value'), "Output should have 'lsb_value' attribute"
        
        assert isinstance(output.is_even, bool), "is_even should be boolean"
        assert isinstance(output.computation_steps, list), "computation_steps should be list"
        assert isinstance(output.lsb_value, int), "lsb_value should be integer"
        assert output.lsb_value in [0, 1], "lsb_value should be 0 or 1"
    
    def test_computation_steps_not_empty(self):
        """Test that computation steps are generated"""
        input_data = EvennessInput(number=42, magic_string="test")
        output = self.calculator.calculate(input_data)
        
        assert len(output.computation_steps) > 0, "Computation steps should not be empty"
    
    def test_magic_string_preserved(self):
        """Test that the magic string is preserved in output"""
        test_string = "hello_world"
        input_data = EvennessInput(number=42, magic_string=test_string)
        output = self.calculator.calculate(input_data)
        
        assert output.magic_string_used == test_string, \
            f"Magic string should be '{test_string}', got '{output.magic_string_used}'"
    
    def test_different_strings_same_result(self):
        """Test that different strings give the same evenness result for the same number"""
        test_num = 42
        expected_even = True
        
        for test_str in self.test_strings:
            input_data = EvennessInput(number=test_num, magic_string=test_str)
            output = self.calculator.calculate(input_data)
            assert output.is_even == expected_even, \
                f"String '{test_str}' changed the result for number {test_num}"


class TestEvennessInputValidation:
    """Test suite for input validation"""
    
    def test_valid_input(self):
        """Test that valid input passes validation"""
        input_data = EvennessInput(number=42, magic_string="test")
        assert input_data.validate() == True
    
    def test_invalid_number_type(self):
        """Test that non-integer number raises ValueError"""
        input_data = EvennessInput(number="42", magic_string="test")
        with pytest.raises(ValueError, match="Number must be an integer"):
            input_data.validate()
    
    def test_invalid_string_type(self):
        """Test that non-string magic_string raises ValueError"""
        input_data = EvennessInput(number=42, magic_string=123)
        with pytest.raises(ValueError, match="Magic string must be a string"):
            input_data.validate()
    
    def test_empty_magic_string(self):
        """Test that empty magic_string raises ValueError"""
        input_data = EvennessInput(number=42, magic_string="")
        with pytest.raises(ValueError, match="Magic string cannot be empty"):
            input_data.validate()
    
    def test_float_number(self):
        """Test that float number raises ValueError"""
        input_data = EvennessInput(number=42.0, magic_string="test")
        with pytest.raises(ValueError, match="Number must be an integer"):
            input_data.validate()


class TestEvennessOutput:
    """Test suite for output formatting"""
    
    def setup_method(self):
        self.calculator = EvennessCalculator()
    
    def test_output_string_even(self):
        """Test string representation for even number"""
        input_data = EvennessInput(number=42, magic_string="test")
        output = self.calculator.calculate(input_data)
        output_str = str(output)
        
        assert "even" in output_str.lower(), "Output string should contain 'even'"
        assert "LSB: 0" in output_str, "Output string should show LSB=0"
    
    def test_output_string_odd(self):
        """Test string representation for odd number"""
        input_data = EvennessInput(number=43, magic_string="test")
        output = self.calculator.calculate(input_data)
        output_str = str(output)
        
        assert "odd" in output_str.lower(), "Output string should contain 'odd'"
        assert "LSB: 1" in output_str, "Output string should show LSB=1"


# Optional: For running detailed step output in verbose mode
@pytest.mark.skip(reason="Only run manually for debugging")
class TestDetailedOutput:
    """Manual test class for viewing detailed computation steps"""
    
    def setup_method(self):
        self.calculator = EvennessCalculator()
    
    def test_detailed_steps_even(self):
        """Print detailed steps for an even number"""
        input_data = EvennessInput(number=42, magic_string="hello")
        output = self.calculator.calculate(input_data)
        
        print("\nDetailed steps for even number:")
        for step in output.computation_steps:
            print(f"  {step}")
        print(f"\nResult: {output}")
    
    def test_detailed_steps_odd(self):
        """Print detailed steps for an odd number"""
        input_data = EvennessInput(number=17, magic_string="world")
        output = self.calculator.calculate(input_data)
        
        print("\nDetailed steps for odd number:")
        for step in output.computation_steps:
            print(f"  {step}")
        print(f"\nResult: {output}")