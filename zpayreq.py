import sys
import re
from decimal import Decimal, InvalidOperation

# Zcash address prefixes for validation
# Transparent: t1, t3
# Shielded: Sapling (zs1), Unified (u1)
TRANSPARENT_PREFIXES = ("t1", "t3")
SHIELDED_PREFIXES = ("zs1", "u1")

def validate_address(address: str) -> str:
    if not address or not isinstance(address, str):
        raise ValueError("INVALID_ADDRESS")
    
    addr = address.strip()
    
    if addr.startswith(TRANSPARENT_PREFIXES):
        raise ValueError("TRANSPARENT_NOT_ALLOWED")
    
    if not addr.startswith(SHIELDED_PREFIXES):
        raise ValueError("INVALID_ADDRESS")
        
    # Corrected bech32/bech32m character set validation regex
    if not re.match(r"^(zs1|u1)[0-9a-z]{30,}$", addr, re.IGNORECASE):
        raise ValueError("INVALID_ADDRESS")
        
    return addr

def validate_amount(amount_str: str) -> Decimal:
    try:
        amount = Decimal(str(amount_str))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("INVALID_AMOUNT")

    if amount.is_nan() or amount.is_infinite():
        raise ValueError("INVALID_AMOUNT")

    if amount <= Decimal("0"):
        raise ValueError("INVALID_AMOUNT")

    # Check Zcash decimal precision (maximum 8 decimal places / Zats)
    normalized = amount.normalize()
    exponent = normalized.as_tuple().exponent
    if isinstance(exponent, int) and exponent < -8:
        raise ValueError("EXCESS_PRECISION")

    return amount

def generate_zip321_uri(address: str, amount: Decimal) -> str:
    # ZIP-321 Payment Request URI format
    # Canonical format without unnecessary trailing zeroes
    formatted_amount = f"{amount:f}".rstrip('0').rstrip('.') if '.' in f"{amount:f}" else f"{amount:f}"
    return f"zcash:{address}?amount={formatted_amount}"

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Error: ERR_INVALID_ARGS\n")
        sys.exit(1)

    address_input = sys.argv[1]
    amount_input = sys.argv[2]

    try:
        addr = validate_address(address_input)
        amt = validate_amount(amount_input)
        uri = generate_zip321_uri(addr, amt)
        print(uri)
        sys.exit(0)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()