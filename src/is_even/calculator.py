from is_even.bit_manipulation import (
    BitwiseStringTransformer,
    EvennessBitExtractor,
)
from is_even.evenness_IO import (
    EvennessInput,
    EvennessOutput,
)


class EvennessCalculator:
    """Main calculator class that orchestrates the evenness computation"""
    
    def __init__(self):
        self.transformer = None
        self.extractor = None
        self.computation_steps = []
    
    def calculate(self, input_data: EvennessInput) -> EvennessOutput:
        """Calculate if a number is even using the magic string"""
        # Validate input
        input_data.validate()
        self.computation_steps = []
        
        # Step 1: Transform the string to bits
        self.transformer = BitwiseStringTransformer(input_data)
        transformed_bits = self.transformer.transform_string_to_bits()
        self.computation_steps.extend(self.transformer.get_log())
        
        # Step 2: Extract LSB using the transformed bits
        self.extractor = EvennessBitExtractor(input_data.number, transformed_bits)
        lsb_value = self.extractor.extract_lsb_using_string_bits()
        self.computation_steps.extend(self.extractor.get_log())
        
        # Step 3: Determine evenness
        is_even = lsb_value == 0
        self.computation_steps.append(f"Final determination: LSB={lsb_value}, Is Even={is_even}")
        
        return EvennessOutput(
            is_even=is_even,
            computation_steps=self.computation_steps,
            magic_string_used=input_data.magic_string,
            lsb_value=lsb_value
        )
