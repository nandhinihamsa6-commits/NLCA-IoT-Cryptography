# NLCA Algorithm Specification

## Classification

NLCA is specified in this repository as a 128-bit substitution–permutation network. It is not described as a Feistel network because the implemented state transition does not use the defining Feistel relation.

## State and bit numbering

A block is sixteen bytes. Bytes are ordered from index 0 to 15. Within each byte, bit 0 of the global state denotes the most significant bit of byte 0.

## Round transformation

For round `r`, the state is transformed as:

1. `X = state XOR round_key[r]`
2. Apply the fixed 4-bit S-box independently to all 32 nibbles.
3. Apply the fixed 128-bit bit permutation.
4. Apply the reversible round-indexed diffusion layer.

Decryption applies the inverse operations in reverse order.

## 128-bit permutation extension

The manuscript reports a sixteen-entry mapping. This repository makes the extension explicit:

`Pi(16g + i) = 16g + pi(i)`

for group `g = 0..7` and local bit index `i = 0..15`. The permutation is therefore applied independently to each of eight contiguous 16-bit slices.

## S-box

`[E,4,D,1,2,F,B,8,3,A,6,C,5,9,0,7]`

## Key schedule

For each round:

1. Rotate the 128-bit key state left by the published round rotation.
2. Apply the S-box to every nibble.
3. Apply the full 128-bit permutation.
4. Apply the deterministic 16-bit f-function to each word and XOR the results into the key state.
5. XOR the explicit 128-bit round constant.

Round keys are deterministic and round-separated. They are not claimed to be statistically independent.

## f-function

For a 16-bit word `w = L || R`:

- `A = P_TABLE[L]`
- `B = Q_TABLE[R]`
- output high byte = `A XOR B`
- output low byte = `P_TABLE[R] XOR Q_TABLE[L]`

All tables are fixed in `nlca/constants.py`.

## Security interpretation

The specification enables independent implementation and testing. It does not establish formal security. DDT, LAT, avalanche and reduced-round results must be interpreted as empirical evidence.
