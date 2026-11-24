# Lab 4 - ElGamal (team)

Implementation of the ElGamal public-key cryptosystem in Python.

## Structure

```
Lab4-Echipa-ElGamal/
├── step1_key_generation/
│   └── key_generation.py   # generate_keys(bits) -> (public_key, private_key)
├── step2_encryption/
│   └── encryption.py       # encrypt(message, public_key) -> (c1, c2)
├── step3_decryption/
│   └── decryption.py       # decrypt(ciphertext, private_key, public_key) -> message
└── main.py                 # runs the full flow: keygen -> encrypt -> decrypt
```

## Interfaces

| Value        | Format                                          |
|--------------|-------------------------------------------------|
| public_key   | `(p, g, h)` with `h = g^x mod p`                |
| private_key  | `x`, integer, `1 <= x <= p - 2`                 |
| message      | integer, `0 <= message < p`                     |
| ciphertext   | `(c1, c2)` = `(g^k mod p, message * h^k mod p)` |

## Team split

| Part                    | Owner     |
|-------------------------|-----------|
| Step 1 - key generation | Lupse     |
| Step 2 - encryption     | Lupse     |
| Step 3 - decryption     | colleague |
| main.py                 | colleague |

## Run

```
python main.py
```
