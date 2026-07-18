from dataclasses import dataclass

@dataclass
class EvennessInput:
    """Input data class for evenness checking"""
    number: int
    magic_string: str
    
    def validate(self) -> bool:
        """Validate input parameters"""
        if not isinstance(self.number, int):
            raise ValueError(f"Number must be an integer, got {type(self.number)}")
        if not isinstance(self.magic_string, str):
            raise ValueError(f"Magic string must be a string, got {type(self.magic_string)}")
        if len(self.magic_string) == 0:
            raise ValueError("Magic string cannot be empty")
        return True
    
@dataclass
class EvennessOutput:
    """Output data class for evenness results"""
    is_even: bool
    computation_steps: list
    magic_string_used: str
    lsb_value: int
    
    def __str__(self):
        return f"Number is {'even' if self.is_even else 'odd'} (LSB: {self.lsb_value})"