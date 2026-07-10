#ifndef NLCA_REFERENCE_H
#define NLCA_REFERENCE_H
#include <stdint.h>
#define NLCA_BLOCK_SIZE 16
#define NLCA_ROUNDS 5
void nlca_expand_key(const uint8_t key[16], uint8_t round_keys[NLCA_ROUNDS][16]);
void nlca_encrypt_block(const uint8_t plaintext[16], const uint8_t key[16], uint8_t ciphertext[16]);
void nlca_decrypt_block(const uint8_t ciphertext[16], const uint8_t key[16], uint8_t plaintext[16]);
#endif
