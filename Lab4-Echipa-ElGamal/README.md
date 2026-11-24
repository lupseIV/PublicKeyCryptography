# Lab 4 - ElGamal (team)

Implementation of the ElGamal public-key cryptosystem in Python.

## Structure

```
Lab4-Echipa-ElGamal/
├── step1_key_generation/
│   └── key_generation.py   # generate_keys(bits=256) -> (public_key, private_key)
├── step2_encryption/
│   └── encryption.py       # encrypt(m, public_key) -> (alpha, beta)
├── step3_decryption/
│   └── decryption.py       # decrypt(ciphertext, private_key, public_key) -> m
└── main.py                 # runs the full flow: keygen -> encrypt -> decrypt
```

## Interfaces

| Value        | Format                                                |
|--------------|-------------------------------------------------------|
| public_key   | `(p, g, ga)` with `ga = g^a mod p`                    |
| private_key  | `a`, integer, `2 <= a <= p - 2`                       |
| message      | `m`, integer, `0 <= m < p`                            |
| ciphertext   | `(alpha, beta)` = `(g^k mod p, m * (g^a)^k mod p)`    |
| decryption   | `m = alpha^(-a) * beta mod p`                         |

## Team split

| Part                    | Owner     |
|-------------------------|-----------|
| Step 1 - key generation | Lupse     |
| Step 2 - encryption     | colleague |
| Step 3 - decryption     | Lupse     |
| main.py                 | colleague |

## Run

```
python main.py
```
