from src.evenness_IO import (
    EvennessInput,
)

class BitwiseStringTransformer:
    """Transforms strings into bit patterns for evenness computation"""
    
    def __init__(self, input_data: EvennessInput):
        self.input_data = input_data
        self.transformed_bits = []
        self._transformation_log = []
    
    def transform_string_to_bits(self) -> list:
        """Convert string characters to their ordinal bit patterns"""
        self._transformation_log.append(f"Transforming string: '{self.input_data.magic_string}'")
        
        for idx, char in enumerate(self.input_data.magic_string):
            ordinal_value = ord(char)
            bit_pattern = self._int_to_bit_list(ordinal_value)
            self.transformed_bits.extend(bit_pattern)
            self._transformation_log.append(
                f"  Char '{char}' (idx {idx}): ord={ordinal_value}, bits={bit_pattern}"
            )
        
        self._transformation_log.append(f"Total transformed bits: {len(self.transformed_bits)}")
        return self.transformed_bits
    
    @staticmethod
    def _int_to_bit_list(value: int, bits: int = 8) -> list:
        """Convert integer to list of bits"""
        return [(value >> i) & 1 for i in range(bits - 1, -1, -1)]
    
    def get_log(self) -> list:
        return self._transformation_log


class EvennessBitExtractor:
    """Extracts and combines bits to determine evenness"""
    
    def __init__(self, number: int, transformed_bits: list):
        self.number = number
        self.transformed_bits = transformed_bits
        self._extraction_log = []
    
    def extract_lsb_using_string_bits(self) -> int:
        """Use transformed string bits to extract the LSB of the number"""
        self._extraction_log.append(f"Number to check: {self.number}")
        self._extraction_log.append(f"Number binary: {bin(self.number)}")
        
        # Get the actual LSB of the number
        actual_lsb = self.number & 1
        self._extraction_log.append(f"Actual LSB: {actual_lsb}")
        
        # Use the string bits to create a mask
        if len(self.transformed_bits) > 0:
            # Create a complex mask using the string bits
            mask = self._create_mask_from_string_bits()
            self._extraction_log.append(f"Generated mask from string: {mask} (binary: {bin(mask)})")
            
            # Apply the mask in a complicated way
            masked_value = self.number & mask
            self._extraction_log.append(f"Masked value: {masked_value} (binary: {bin(masked_value)})")
            
            # Extract LSB through the masked value
            extracted_lsb = masked_value & 1
            self._extraction_log.append(f"Extracted LSB through mask: {extracted_lsb}")
        else:
            extracted_lsb = actual_lsb
        
        return extracted_lsb
    
    def _create_mask_from_string_bits(self) -> int:
        """Create a mask from string bits that preserves the LSB"""
        # Use the first 8 bits (or fewer) to create a mask
        bits_to_use = self.transformed_bits[:min(8, len(self.transformed_bits))]
        
        # Ensure the LSB is always 1 in the mask so we can extract it
        mask = 0
        for i, bit in enumerate(reversed(bits_to_use)):
            if i == 0:  # LSB position
                mask |= 1  # Always set LSB to 1
            else:
                mask |= (bit << i)
        
        return mask
    
    def get_log(self) -> list:
        return self._extraction_log
