import pytest
from hypothesis import given, strategies as st
from hypothesis import assume

from is_even.evenness_IO import EvennessInput
from is_even.calculator import EvennessCalculator
from is_even.bit_manipulation import BitwiseStringTransformer, EvennessBitExtractor

@given(
    number=st.integers(),
    magic_string=st.text(min_size=1)
)
def test_evenness_input_validate_valid(number, magic_string):
    """Valid inputs should pass validation without exception."""
    inp = EvennessInput(number=number, magic_string=magic_string)
    assert inp.validate() is True

@given(
    number=st.integers(),
    magic_string=st.text(min_size=0)
)
def test_evenness_input_validate_empty_string_raises(number, magic_string):
    """Empty magic string should raise ValueError."""
    inp = EvennessInput(number=number, magic_string=magic_string)
    if magic_string == "":
        with pytest.raises(ValueError, match="Magic string cannot be empty"):
            inp.validate()
    else:
        assert inp.validate() is True

@given(
    number=st.one_of(st.none(), st.floats(), st.booleans(), st.text()),
    magic_string=st.text(min_size=1)
)
def test_evenness_input_validate_invalid_number_raises(number, magic_string):
    """Non‑integer number should raise ValueError."""
    assume(not isinstance(number, int))
    inp = EvennessInput(number=number, magic_string=magic_string)
    with pytest.raises(ValueError, match="Number must be an integer"):
        inp.validate()

@given(
    number=st.integers(),
    magic_string=st.one_of(st.none(), st.integers(), st.floats(), st.booleans())
)
def test_evenness_input_validate_invalid_string_raises(number, magic_string):
    """Non‑string magic_string should raise ValueError."""
    assume(not isinstance(magic_string, str))
    inp = EvennessInput(number=number, magic_string=magic_string)
    with pytest.raises(ValueError, match="Magic string must be a string"):
        inp.validate()

@given(
    number=st.integers(),
    magic_string=st.text(min_size=1)
)
def test_bitwise_string_transformer_output_length(number, magic_string):
    inp = EvennessInput(number, magic_string)
    transformer = BitwiseStringTransformer(inp)
    bits = transformer.transform_string_to_bits()
    assert len(bits) == 32 * len(magic_string)
    assert all(b in (0, 1) for b in bits)


@given(
    number=st.integers(),
    magic_string=st.text(min_size=1)
)
def test_bitwise_string_transformer_correct_conversion(number, magic_string):
    inp = EvennessInput(number, magic_string)
    transformer = BitwiseStringTransformer(inp)
    bits = transformer.transform_string_to_bits()
    chunk_size = 32 
    chunks = [bits[i:i+chunk_size] for i in range(0, len(bits), chunk_size)]
    for idx, chunk in enumerate(chunks):
        ordinal = int("".join(str(b) for b in chunk), 2)
        assert ordinal == ord(magic_string[idx])

@given(
    number=st.integers(),
    magic_string=st.text(min_size=1)
)
def test_evenness_bit_extractor_lsb_always_correct(number, magic_string):
    """
    The extractor should always return the actual LSB of the number,
    regardless of the string bits (because the mask forces LSB=1).
    """
    inp = EvennessInput(number, magic_string)
    transformer = BitwiseStringTransformer(inp)
    bits = transformer.transform_string_to_bits()
    extractor = EvennessBitExtractor(number, bits)
    lsb = extractor.extract_lsb_using_string_bits()
    assert lsb == (number & 1)


@given(number=st.integers())
def test_evenness_bit_extractor_empty_bits_fallback(number):
    """When transformed_bits is empty, fallback to actual LSB."""
    extractor = EvennessBitExtractor(number, [])
    lsb = extractor.extract_lsb_using_string_bits()
    assert lsb == (number & 1)


@given(
    number=st.integers(),
    magic_string=st.text(min_size=1)
)
def test_evenness_calculator_correct_evenness(number, magic_string):
    """The calculator should produce the correct evenness result."""
    inp = EvennessInput(number, magic_string)
    calc = EvennessCalculator()
    output = calc.calculate(inp)
    assert output.is_even == (number % 2 == 0)
    assert output.magic_string_used == magic_string
    assert output.lsb_value == (number & 1)
    assert isinstance(output.computation_steps, list)
    assert len(output.computation_steps) > 0


@given(number=st.integers(), magic_string=st.text(min_size=1))
def test_evenness_calculator_steps_contain_expected_messages(number, magic_string):
    """Check that the computation steps include key phrases."""
    inp = EvennessInput(number, magic_string)
    calc = EvennessCalculator()
    output = calc.calculate(inp)
    steps = " ".join(output.computation_steps)
    assert "Transforming string" in steps
    assert "Number to check" in steps
    assert "Final determination" in steps