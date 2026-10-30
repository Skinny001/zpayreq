import pytest
import subprocess
import sys
from zpayreq import validate_address, validate_amount, generate_zip321_uri

# Valid Shielded Addresses (Sapling & Unified)
VALID_SAPLING = "zs1z7rejlpsa98s23uk9x3p28tw8y23ak4m29244re27s"
VALID_UNIFIED = "u1q8x9...sampleunifiedaddressstr..."

def test_happy_path():
    addr = validate_address(VALID_SAPLING)
    amt = validate_amount("1.5")
    uri = generate_zip321_uri(addr, amt)
    assert uri == f"zcash:{VALID_SAPLING}?amount=1.5"

def test_transparent_address_rejected():
    with pytest.raises(ValueError, match="TRANSPARENT_NOT_ALLOWED"):
        validate_address("t1M4BzbBmy3858w392842")

def test_invalid_address_format():
    with pytest.raises(ValueError, match="INVALID_ADDRESS"):
        validate_address("invalid_address_str")

def test_invalid_amount_zero_or_negative():
    with pytest.raises(ValueError, match="INVALID_AMOUNT"):
        validate_amount("0")
    with pytest.raises(ValueError, match="INVALID_AMOUNT"):
        validate_amount("-5.0")

def test_invalid_amount_nan():
    with pytest.raises(ValueError, match="INVALID_AMOUNT"):
        validate_amount("NaN")

def test_excess_precision():
    with pytest.raises(ValueError, match="EXCESS_PRECISION"):
        validate_amount("0.000000001") # 9 decimal places