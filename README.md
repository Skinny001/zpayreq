# zpayreq CLI

`zpayreq` is a Python command-line utility for validating Zcash recipient addresses and payment amounts to generate ZIP-321 compliant Payment Request URIs.

---

## Contract & Specification

- **Input Format:** `zpayreq <address> <amount>`
- **Happy Path:** Outputs a canonical ZIP-321 payment request URI (`zcash:<address>?amount=<amount>`) to `stdout` and exits with code `0`.
- **Failure Handling:** Rejects invalid inputs by writing specific error codes to `stderr` and exiting with code `1`.

---

## Error Classes & Failure Codes

| Failure Class | Error Code | Cause / Trigger Condition |
| :--- | :--- | :--- |
| **Invalid CLI Arguments** | `ERR_INVALID_ARGS` | Executed without both required `<address>` and `<amount>` arguments. |
| **Invalid Address Format** | `INVALID_ADDRESS` | Address fails structural requirements, is empty/malformed, or uses an unknown prefix. |
| **Transparent Address Rejected** | `TRANSPARENT_NOT_ALLOWED` | Recipient address uses a transparent prefix (`t1` or `t3`). Shielded address (`zs1` or `u1`) required. |
| **Invalid Amount** | `INVALID_AMOUNT` | Amount is zero, negative, non-numeric (`NaN`, `Inf`), or missing. |
| **Excess Precision** | `EXCESS_PRECISION` | Amount exceeds the maximum Zcash precision limit of 8 decimal places (1 Zatoshi). |

---

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/Skinny001/zpayreq.git](https://github.com/Skinny001/zpayreq.git)
cd zpayreq

python3 -m venv venv
source venv/bin/activate
pip install pytest pytest-cov
