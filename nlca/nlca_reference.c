#include "nlca_reference.h"
#include <string.h>

static const uint8_t SBOX[16] = {14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7};
static const uint8_t INV_SBOX[16] = {14,3,4,8,1,12,10,15,7,13,9,6,11,2,0,5};
static const uint8_t PBOX[128] = {4,12,8,0,9,1,13,5,2,14,6,10,7,15,3,11,20,28,24,16,25,17,29,21,18,30,22,26,23,31,19,27,36,44,40,32,41,33,45,37,34,46,38,42,39,47,35,43,52,60,56,48,57,49,61,53,50,62,54,58,55,63,51,59,68,76,72,64,73,65,77,69,66,78,70,74,71,79,67,75,84,92,88,80,89,81,93,85,82,94,86,90,87,95,83,91,100,108,104,96,105,97,109,101,98,110,102,106,103,111,99,107,116,124,120,112,121,113,125,117,114,126,118,122,119,127,115,123};
static const uint8_t INV_PBOX[128] = {3,5,8,14,0,7,10,12,2,4,11,15,1,6,9,13,19,21,24,30,16,23,26,28,18,20,27,31,17,22,25,29,35,37,40,46,32,39,42,44,34,36,43,47,33,38,41,45,51,53,56,62,48,55,58,60,50,52,59,63,49,54,57,61,67,69,72,78,64,71,74,76,66,68,75,79,65,70,73,77,83,85,88,94,80,87,90,92,82,84,91,95,81,86,89,93,99,101,104,110,96,103,106,108,98,100,107,111,97,102,105,109,115,117,120,126,112,119,122,124,114,116,123,127,113,118,121,125};
static const uint8_t ROT[5] = {13,29,47,61,79};
static const uint8_t RC[5][16] = {
{0x9e,0x37,0x79,0xb9,0x7f,0x4a,0x7c,0x15,0xf3,0x9c,0xc0,0x60,0x5c,0xed,0xc8,0x35},
{0x3c,0x6e,0xf3,0x72,0xfe,0x94,0xf8,0x2b,0xe7,0x39,0x80,0xc0,0xb9,0xdb,0x90,0x6a},
{0xda,0xa6,0x6d,0x2c,0x7d,0xdf,0x74,0x31,0xdb,0xd6,0x41,0xa1,0x15,0xc9,0x64,0x9f},
{0x78,0xdd,0xe6,0xe5,0xfd,0x29,0xf0,0x47,0xcf,0x73,0x01,0x81,0x73,0xb7,0x20,0xd4},
{0x17,0x15,0x60,0x9f,0x7c,0x74,0x6c,0x5d,0xc3,0x0f,0xc1,0xe1,0xd1,0xa5,0xad,0x09}
};

static void sub(uint8_t s[16], const uint8_t box[16]) {
    for (int i=0;i<16;i++) s[i]=(uint8_t)((box[s[i]>>4]<<4)|box[s[i]&15]);
}
static void perm(uint8_t s[16], const uint8_t map[128]) {
    uint8_t out[16]={0};
    for(int src=0;src<128;src++){
        uint8_t bit=(uint8_t)((s[src/8]>>(7-src%8))&1);
        int dst=map[src];
        out[dst/8]|=(uint8_t)(bit<<(7-dst%8));
    }
    memcpy(s,out,16);
}
static void rotl128(uint8_t s[16], int shift) {
    uint8_t out[16]={0};
    for(int i=0;i<128;i++){
        int src=(i+shift)%128;
        uint8_t bit=(uint8_t)((s[src/8]>>(7-src%8))&1);
        out[i/8]|=(uint8_t)(bit<<(7-i%8));
    }
    memcpy(s,out,16);
}
static uint8_t ptab(uint8_t x) { return (uint8_t)((SBOX[x>>4]<<4)|SBOX[x&15]); }
static uint8_t qtab(uint8_t x) { return (uint8_t)(((SBOX[x&15]<<4)|SBOX[x>>4])^0xA5); }
static void fmix(uint8_t s[16]) {
    uint8_t out[16];
    for(int i=0;i<16;i+=2){
        uint8_t l=s[i], r=s[i+1];
        out[i]=(uint8_t)(ptab(l)^qtab(r));
        out[i+1]=(uint8_t)(ptab(r)^qtab(l));
    }
    for(int i=0;i<16;i++) s[i]^=out[i];
}
static void diffuse(uint8_t s[16], int r) {
    static const int rr[7]={1,3,5,7,2,4,6};
    for(int i=1;i<16;i++) s[i]^=s[i-1];
    uint8_t out[16]; int n=rr[r%7];
    for(int i=0;i<16;i++) out[i]=s[(i+n)%16];
    memcpy(s,out,16);
}
static void invdiffuse(uint8_t s[16], int r) {
    static const int rr[7]={1,3,5,7,2,4,6};
    uint8_t out[16]; int n=rr[r%7];
    for(int i=0;i<16;i++) out[(i+n)%16]=s[i];
    memcpy(s,out,16);
    for(int i=15;i>0;i--) s[i]^=s[i-1];
}
void nlca_expand_key(const uint8_t key[16], uint8_t rk[NLCA_ROUNDS][16]) {
    uint8_t s[16]; memcpy(s,key,16);
    for(int r=0;r<NLCA_ROUNDS;r++){
        rotl128(s,ROT[r]); sub(s,SBOX); perm(s,PBOX); fmix(s);
        for(int i=0;i<16;i++) s[i]^=RC[r][i];
        memcpy(rk[r],s,16);
    }
}
void nlca_encrypt_block(const uint8_t pt[16], const uint8_t key[16], uint8_t ct[16]) {
    uint8_t rk[NLCA_ROUNDS][16], s[16]; memcpy(s,pt,16); nlca_expand_key(key,rk);
    for(int r=0;r<NLCA_ROUNDS;r++){ for(int i=0;i<16;i++) s[i]^=rk[r][i]; sub(s,SBOX); perm(s,PBOX); diffuse(s,r); }
    memcpy(ct,s,16);
}
void nlca_decrypt_block(const uint8_t ct[16], const uint8_t key[16], uint8_t pt[16]) {
    uint8_t rk[NLCA_ROUNDS][16], s[16]; memcpy(s,ct,16); nlca_expand_key(key,rk);
    for(int r=NLCA_ROUNDS-1;r>=0;r--){ invdiffuse(s,r); perm(s,INV_PBOX); sub(s,INV_SBOX); for(int i=0;i<16;i++) s[i]^=rk[r][i]; }
    memcpy(pt,s,16);
}
