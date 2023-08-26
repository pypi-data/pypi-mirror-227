/*
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
*/

/* ECDH/ECIES/ECDSA Functions - see main program below */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include "ecdh_SECP256K1.h"

/* Calculate a public/private EC GF(p) key pair. W=S.G mod EC(p),
 * where S is the secret key and W is the public key
 * and G is fixed generator.
 * If RNG is NULL then the private key is provided externally in S
 * otherwise it is generated randomly internally */
int ECP_SECP256K1_KEY_PAIR_GENERATE(csprng *RNG,octet* S,octet *W)
{
    BIG_256_28 r,s;
    ECP_SECP256K1 G;
    int res=0;

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);
    if (RNG!=NULL)
    {
        BIG_256_28_randomnum(s,r,RNG);
    }
    else
    {
        BIG_256_28_fromBytes(s,S->val);
        BIG_256_28_mod(s,r);
    }

#ifdef AES_S
    BIG_256_28_mod2m(s,2*AES_S);
#endif

    S->len=EGS_SECP256K1;
    BIG_256_28_toBytes(S->val,s);

    ECP_SECP256K1_mul(&G,s);

    ECP_SECP256K1_toOctet(W,&G,false);  /* To use point compression on public keys, change to true */

    return res;
}

/* Validate public key */
int ECP_SECP256K1_PUBLIC_KEY_VALIDATE(octet *W)
{
    BIG_256_28 q,r,k;
    ECP_SECP256K1 WP;
    int valid,nb;
    int res=0;

    BIG_256_28_rcopy(q,Modulus_SECP256K1);
    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    valid=ECP_SECP256K1_fromOctet(&WP,W);
    if (!valid) res=ECDH_INVALID_PUBLIC_KEY;

    if (res==0)
    {
        /* Check point is not in wrong group */
        nb=BIG_256_28_nbits(q);
        BIG_256_28_one(k);
        BIG_256_28_shl(k,(nb+4)/2);
        BIG_256_28_add(k,q,k);
        BIG_256_28_sdiv(k,r); /* get co-factor */

        while (BIG_256_28_parity(k)==0)
        {
            ECP_SECP256K1_dbl(&WP);
            BIG_256_28_fshr(k,1);
        }

        if (!BIG_256_28_isunity(k)) ECP_SECP256K1_mul(&WP,k);
        if (ECP_SECP256K1_isinf(&WP)) res=ECDH_INVALID_PUBLIC_KEY;
    }

    return res;
}

/* IEEE-1363 Diffie-Hellman online calculation Z=S.WD */
int ECP_SECP256K1_SVDP_DH(octet *S,octet *WD,octet *Z)
{
    BIG_256_28 r,s,wx;
    int valid;
    ECP_SECP256K1 W;
    int res=0;

    BIG_256_28_fromBytes(s,S->val);

    valid=ECP_SECP256K1_fromOctet(&W,WD);

    if (!valid) res=ECDH_ERROR;
    if (res==0)
    {
        BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);
        BIG_256_28_mod(s,r);

        ECP_SECP256K1_mul(&W,s);
        if (ECP_SECP256K1_isinf(&W)) res=ECDH_ERROR;
        else
        {
#if CURVETYPE_SECP256K1!=MONTGOMERY
            ECP_SECP256K1_get(wx,wx,&W);
#else
            ECP_SECP256K1_get(wx,&W);
#endif
            Z->len=MODBYTES_256_28;
            BIG_256_28_toBytes(Z->val,wx);
        }
    }
    return res;
}

#if CURVETYPE_SECP256K1!=MONTGOMERY

/* IEEE ECDSA Signature, C and D are signature on F using private key S */
int ECP_SECP256K1_SP_DSA(int sha,csprng *RNG,octet *K,octet *S,octet *F,octet *C,octet *D)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_256_28 r,s,f,c,d,u,vx,w;
    ECP_SECP256K1 G,V;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    BIG_256_28_fromBytes(s,S->val);

    int hlen=H.len;
    if (H.len>MODBYTES_256_28) hlen=MODBYTES_256_28;
    BIG_256_28_fromBytesLen(f,H.val,hlen);

    if (RNG!=NULL)
    {
        do
        {
            BIG_256_28_randomnum(u,r,RNG);
            BIG_256_28_randomnum(w,r,RNG); /* side channel masking */

#ifdef AES_S
            BIG_256_28_mod2m(u,2*AES_S);
#endif
            ECP_SECP256K1_copy(&V,&G);
            ECP_SECP256K1_mul(&V,u);

            ECP_SECP256K1_get(vx,vx,&V);

            BIG_256_28_copy(c,vx);
            BIG_256_28_mod(c,r);
            if (BIG_256_28_iszilch(c)) continue;

            BIG_256_28_modmul(u,u,w,r);

            BIG_256_28_invmodp(u,u,r);
            BIG_256_28_modmul(d,s,c,r);

            BIG_256_28_add(d,f,d);

            BIG_256_28_modmul(d,d,w,r);

            BIG_256_28_modmul(d,u,d,r);
        }
        while (BIG_256_28_iszilch(d));
    }
    else
    {
        BIG_256_28_fromBytes(u,K->val);
        BIG_256_28_mod(u,r);

#ifdef AES_S
        BIG_256_28_mod2m(u,2*AES_S);
#endif
        ECP_SECP256K1_copy(&V,&G);
        ECP_SECP256K1_mul(&V,u);

        ECP_SECP256K1_get(vx,vx,&V);

        BIG_256_28_copy(c,vx);
        BIG_256_28_mod(c,r);
        if (BIG_256_28_iszilch(c)) return ECDH_ERROR;


        BIG_256_28_invmodp(u,u,r);
        BIG_256_28_modmul(d,s,c,r);

        BIG_256_28_add(d,f,d);

        BIG_256_28_modmul(d,u,d,r);
        if (BIG_256_28_iszilch(d)) return ECDH_ERROR;
    }

    C->len=D->len=EGS_SECP256K1;

    BIG_256_28_toBytes(C->val,c);
    BIG_256_28_toBytes(D->val,d);

    return 0;
}

/* RFC6979 Section 3 https://www.rfc-editor.org/rfc/rfc6979 */
/* IEEE ECDSA Deterministic Signature, C and D are signature on F using private key S.
octU is the deterministic parameter k in the RFC6979.*/
int ECP_SECP256K1_SP_DSA_DET(int sha,octet *S,octet *F,octet *C,octet *D, octet *octU)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_256_28 r,s,f,c,d,u,vx,vy,w;
    ECP_SECP256K1 G,V;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);
    
    int rBytes = (BIG_256_28_nbits(r) + 7)/8;

    char temp[rBytes], vec[sha], k[sha], ch[rBytes], conc[sha + 1 + (2*rBytes)];

    octet octS = {rBytes, sizeof(temp), temp};
    OCT_copy(&octS, S);
    OCT_pad(&octS, rBytes);

    BIG_256_28_fromBytes(s, octS.val);

    int hlen=H.len;
    if (H.len>MODBYTES_256_28) hlen=MODBYTES_256_28;
// f correspond to bits2int(H(m)) mod q in the paper
    BIG_256_28_fromBytesLen(f,H.val,hlen);
    
// VEC = V in the paper
    octet VEC = {0, sizeof(vec), vec};
    OCT_jbyte(&VEC, 1, H.len);

    octet K = {0, sizeof(k), k};
    OCT_jint(&K, 0, H.len);

//octH = bits2octet(h1) in the paper
    octet octH = {rBytes, sizeof(ch), ch};
    BIG_256_28_toBytes(octH.val, f);
    OCT_pad(&octH, rBytes);

    octet CONC = {VEC.len, sizeof(conc), conc};
    
    OCT_copy(&CONC, &VEC);
    OCT_jbyte(&CONC, 0, 1);
    OCT_joctet(&CONC, &octS);
    OCT_joctet(&CONC, &octH);

    AMCL_(HMAC)(sha, &CONC, &K, sha, &K);

    AMCL_(HMAC)(sha, &VEC, &K, sha, &VEC);

    OCT_clear(&CONC);

    OCT_copy(&CONC, &VEC);
    OCT_jbyte(&CONC, 1, 1);
    OCT_joctet(&CONC, &octS);
    OCT_joctet(&CONC,&octH);

    AMCL_(HMAC)(sha,&CONC,&K, sha, &K);
    AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);

    char check_k;

    do {
        char t[2*rBytes];
        octet T = {VEC.len,sizeof(t), t};
        AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
        OCT_copy(&T, &VEC);

        while (T.len < rBytes) {
            AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
            OCT_joctet(&T,&VEC);
        }

        BIG_256_28_fromBytesLen(u, T.val, rBytes); //u = k in the paper

        ECP_SECP256K1_copy(&V,&G);
        ECP_SECP256K1_mul(&V,u);
        ECP_SECP256K1_get(vx,vy, &V);
        BIG_256_28_copy(c,vx);
        BIG_256_28_mod(c,r);

        check_k = BIG_256_28_iszilch(u) || BIG_256_28_comp(u, r) >= 0 || BIG_256_28_iszilch(c);
        if(check_k){
            octet CONC2 = {0, sizeof(t),t};
            OCT_copy(&CONC2, &VEC);
            OCT_jbyte(&CONC2, 0, 1);
            AMCL_(HMAC)(sha,&CONC2,&K, sha, &K);
            AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
        }

    } while(check_k);
    
    if(octU){
        octU->len = rBytes;
        BIG_256_28_toBytes(octU->val, u);  
    }
    BIG_256_28_invmodp(u,u,r);
    BIG_256_28_modmul(d,s,c,r);

    BIG_256_28_add(d,f,d);

    BIG_256_28_modmul(d,u,d,r);
    if (BIG_256_28_iszilch(d)) return ECDH_ERROR;

    C->len=D->len=EGS_SECP256K1;

    BIG_256_28_toBytes(C->val,c);
    BIG_256_28_toBytes(D->val,d);

    return 0;
}

/* RFC6979 ECDSA DETERMINISTIC Signature as above, without hash on input (assume as already hashed) */
int ECP_SECP256K1_SP_DSA_DET_NOHASH(int sha, octet *S,octet *H,octet *C,octet *D, int *y_parity)
// substituted F with H in args
{
    BIG_256_28 r,s,f,c,d,u,vx,vy;
    ECP_SECP256K1 G,V;

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    int rBytes = (BIG_256_28_nbits(r) + 7)/8;

    char temp[rBytes], vec[sha], k[sha], ch[rBytes], conc[sha + 1 + (2*rBytes)];

    octet octS = {rBytes, sizeof(temp), temp};
    OCT_copy(&octS, S);
    OCT_pad(&octS, rBytes);

    BIG_256_28_fromBytes(s, octS.val);

    int hlen=H->len;
    if (H->len>MODBYTES_256_28) hlen=MODBYTES_256_28;
    BIG_256_28_fromBytesLen(f,H->val,hlen);

// VEC = V in the paper
    octet VEC = {0, sizeof(vec), vec};
    OCT_jbyte(&VEC, 1, H->len);

    octet K = {0, sizeof(k), k};
    OCT_jint(&K, 0, H->len);

//octH = bits2octet(h1) in the paper
    octet octH = {rBytes, sizeof(ch), ch};
    BIG_256_28_toBytes(octH.val, f);
    OCT_pad(&octH, rBytes);

    octet CONC = {VEC.len, sizeof(conc), conc};
    
    OCT_copy(&CONC, &VEC);
    OCT_jbyte(&CONC, 0, 1);
    OCT_joctet(&CONC, &octS);
    OCT_joctet(&CONC, &octH);

    AMCL_(HMAC)(sha, &CONC, &K, sha, &K);

    AMCL_(HMAC)(sha, &VEC, &K, sha, &VEC);

    OCT_clear(&CONC);

    OCT_copy(&CONC, &VEC);
    OCT_jbyte(&CONC, 1, 1);
    OCT_joctet(&CONC, &octS);
    OCT_joctet(&CONC,&octH);

    AMCL_(HMAC)(sha,&CONC,&K, sha, &K);
    AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);

    char check_k;

    do {
        char t[2*rBytes];
        octet T = {VEC.len,sizeof(t), t};
        AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
        OCT_copy(&T, &VEC);

        while (T.len < rBytes) {
            AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
            OCT_joctet(&T,&VEC);
        }

        BIG_256_28_fromBytesLen(u, T.val, rBytes); //u = k in the paper

        ECP_SECP256K1_copy(&V,&G);
        ECP_SECP256K1_mul(&V,u);
        ECP_SECP256K1_get(vx,vy, &V);
        BIG_256_28_copy(c,vx);
        BIG_256_28_mod(c,r);

        check_k = BIG_256_28_iszilch(u) || BIG_256_28_comp(u, r) >= 0 || BIG_256_28_iszilch(c);
        if(check_k){
            octet CONC2 = {0, sizeof(t),t};
            OCT_copy(&CONC2, &VEC);
            OCT_jbyte(&CONC2, 0, 1);
            AMCL_(HMAC)(sha,&CONC2,&K, sha, &K);
            AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
        }

    } while(check_k);
    
    BIG_256_28_invmodp(u,u,r);
    BIG_256_28_modmul(d,s,c,r);

    BIG_256_28_add(d,f,d);

    BIG_256_28_modmul(d,u,d,r);
    if (BIG_256_28_iszilch(d)) return ECDH_ERROR;

    if(y_parity) {
      *y_parity = BIG_256_28_parity(vy);
    }

    C->len=D->len=EGS_SECP256K1;

    BIG_256_28_toBytes(C->val,c);
    BIG_256_28_toBytes(D->val,d);

    return 0;
}

/* IEEE ECDSA Signature as above, without hash on input (assume as already hashed) */
int ECP_SECP256K1_SP_DSA_NOHASH(int sha,csprng *RNG,octet *K,octet *S,octet *H,octet *C,octet *D, int *y_parity)
// substituted F with H in args
{
    BIG_256_28 r,s,f,c,d,u,vx,vy,w;
    ECP_SECP256K1 G,V;

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    BIG_256_28_fromBytes(s,S->val);

    int hlen=H->len;
    if (H->len>MODBYTES_256_28) hlen=MODBYTES_256_28;
    BIG_256_28_fromBytesLen(f,H->val,hlen);

    if (RNG!=NULL)
    {
        do
        {
            BIG_256_28_randomnum(u,r,RNG);
            BIG_256_28_randomnum(w,r,RNG); /* side channel masking */

#ifdef AES_S
            BIG_256_28_mod2m(u,2*AES_S);
#endif
            ECP_SECP256K1_copy(&V,&G);
            ECP_SECP256K1_mul(&V,u);

            ECP_SECP256K1_get(vx,vy,&V);
            BIG_256_28_copy(c,vx);
            BIG_256_28_mod(c,r);
            if (BIG_256_28_iszilch(c)) continue;

            BIG_256_28_modmul(u,u,w,r);

            BIG_256_28_invmodp(u,u,r);
            BIG_256_28_modmul(d,s,c,r);

            BIG_256_28_add(d,f,d);

            BIG_256_28_modmul(d,d,w,r);

            BIG_256_28_modmul(d,u,d,r);
        }
        while (BIG_256_28_iszilch(d));
    }
    else
    {
        BIG_256_28_fromBytes(u,K->val);
        BIG_256_28_mod(u,r);

#ifdef AES_S
        BIG_256_28_mod2m(u,2*AES_S);
#endif
        ECP_SECP256K1_copy(&V,&G);
        ECP_SECP256K1_mul(&V,u);

        ECP_SECP256K1_get(vx,vy,&V);
        BIG_256_28_copy(c,vx);
        BIG_256_28_mod(c,r);
        if (BIG_256_28_iszilch(c)) return ECDH_ERROR;


        BIG_256_28_invmodp(u,u,r);
        BIG_256_28_modmul(d,s,c,r);

        BIG_256_28_add(d,f,d);

        BIG_256_28_modmul(d,u,d,r);
        if (BIG_256_28_iszilch(d)) return ECDH_ERROR;
    }
    if(y_parity) {
      *y_parity = BIG_256_28_parity(vy);
    }

    C->len=D->len=EGS_SECP256K1;

    BIG_256_28_toBytes(C->val,c);
    BIG_256_28_toBytes(D->val,d);

    return 0;
}

/* IEEE1363 ECDSA Signature Verification. Signature C and D on F is verified using public key W */
int ECP_SECP256K1_VP_DSA_NOHASH(int sha,octet *W,octet *H, octet *C,octet *D)
// substituted F with H in args
{

    BIG_256_28 r,f,c,d,h2;
    int res=0;
    ECP_SECP256K1 G,WP;
    int valid, clen, dlen;

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    if(C->len > MODBYTES_256_28) {
	OCT_shl(C,C->len-MODBYTES_256_28);
	clen = MODBYTES_256_28;
    }
    else clen = C->len;
    
    if(D->len > MODBYTES_256_28) {
	OCT_shl(D,D->len-MODBYTES_256_28);
	dlen = MODBYTES_256_28;
    }
    else dlen = D->len;

    BIG_256_28_fromBytesLen(c,C->val,clen);
    BIG_256_28_fromBytesLen(d,D->val,dlen);

    int hlen=H->len;
    if (hlen>MODBYTES_256_28) hlen=MODBYTES_256_28;

    BIG_256_28_fromBytesLen(f,H->val,hlen);

    //BIG_fromBytes(f,H->val);

    if (BIG_256_28_iszilch(c) || BIG_256_28_comp(c,r)>=0 || BIG_256_28_iszilch(d) || BIG_256_28_comp(d,r)>=0)
        res=ECDH_INVALID;

    if (res==0)
    {
        BIG_256_28_invmodp(d,d,r);
        BIG_256_28_modmul(f,f,d,r);
        BIG_256_28_modmul(h2,c,d,r);

        valid=ECP_SECP256K1_fromOctet(&WP,W);

        if (!valid) res=ECDH_ERROR;
        else
        {
            ECP_SECP256K1_mul2(&WP,&G,h2,f);

            if (ECP_SECP256K1_isinf(&WP)) res=ECDH_INVALID;
            else
            {
                ECP_SECP256K1_get(d,d,&WP);
                BIG_256_28_mod(d,r);
                if (BIG_256_28_comp(d,c)!=0) res=ECDH_INVALID;
            }
        }
    }

    return res;
}

/* IEEE1363 ECDSA Signature Verification. Signature C and D on F is verified using public key W */
int ECP_SECP256K1_VP_DSA(int sha,octet *W,octet *F, octet *C,octet *D)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_256_28 r,f,c,d,h2;
    int res=0;
    ECP_SECP256K1 G,WP;
    int valid, clen, dlen;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_SECP256K1_generator(&G);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);

    if(C->len > MODBYTES_256_28) {
	OCT_shl(C,C->len-MODBYTES_256_28);
	clen = MODBYTES_256_28;
    }
    else clen = C->len;
    
    if(D->len > MODBYTES_256_28) {
	OCT_shl(D,D->len-MODBYTES_256_28);
	dlen = MODBYTES_256_28;
    }
    else dlen = D->len;

    BIG_256_28_fromBytesLen(c,C->val,clen);
    BIG_256_28_fromBytesLen(d,D->val,dlen);

    int hlen=H.len;
    if (hlen>MODBYTES_256_28) hlen=MODBYTES_256_28;

    BIG_256_28_fromBytesLen(f,H.val,hlen);

    //BIG_fromBytes(f,H.val);

    if (BIG_256_28_iszilch(c) || BIG_256_28_comp(c,r)>=0 || BIG_256_28_iszilch(d) || BIG_256_28_comp(d,r)>=0)
        res=ECDH_INVALID;

    if (res==0)
    {
        BIG_256_28_invmodp(d,d,r);
        BIG_256_28_modmul(f,f,d,r);
        BIG_256_28_modmul(h2,c,d,r);

        valid=ECP_SECP256K1_fromOctet(&WP,W);

        if (!valid) res=ECDH_ERROR;
        else
        {
            ECP_SECP256K1_mul2(&WP,&G,h2,f);

            if (ECP_SECP256K1_isinf(&WP)) res=ECDH_INVALID;
            else
            {
                ECP_SECP256K1_get(d,d,&WP);
                BIG_256_28_mod(d,r);
                if (BIG_256_28_comp(d,c)!=0) res=ECDH_INVALID;
            }
        }
    }

    return res;
}

/* From the ephemeral public key (x,y) of a signature (C,D) on H the hash of the message
   recover the public key PK that verifies the singature, if it exists */
int ECP_SECP256K1_PUBLIC_KEY_RECOVERY(octet *X, int y_parity, octet *H, octet *C, octet *D, octet *PK)
{
    BIG_256_28 x, c, d, h, r;
    ECP_SECP256K1 P, G_neg;
    int xlen, clen, dlen, hlen;

    if(X->len > MODBYTES_256_28) {
	OCT_shl(X,X->len-MODBYTES_256_28);
	xlen = MODBYTES_256_28;
    }
    else xlen = X->len;
    BIG_256_28_fromBytesLen(x,X->val,xlen);

    if (!ECP_SECP256K1_setx(&P,x,y_parity)) return -1;

    if(C->len > MODBYTES_256_28) {
	OCT_shl(C,C->len-MODBYTES_256_28);
	clen = MODBYTES_256_28;
    }
    else clen = C->len;
    BIG_256_28_fromBytesLen(c,C->val, clen);

    if(D->len > MODBYTES_256_28) {
	OCT_shl(D,D->len-MODBYTES_256_28);
	dlen = MODBYTES_256_28;
    }
    else dlen = D->len;
    BIG_256_28_fromBytesLen(d,D->val, dlen);

    hlen=H->len;
    if (hlen>MODBYTES_256_28) hlen=MODBYTES_256_28;
    BIG_256_28_fromBytesLen(h,H->val,hlen);

    ECP_SECP256K1_generator(&G_neg);
    ECP_SECP256K1_neg(&G_neg);

    ECP_SECP256K1_mul2(&P,&G_neg,d,h);

    BIG_256_28_rcopy(r,CURVE_Order_SECP256K1);
    BIG_256_28_invmodp(c,c,r);
    ECP_SECP256K1_mul(&P,c);

    ECP_SECP256K1_toOctet(PK,&P,false); //uncompressed public key
    return ECP_SECP256K1_PUBLIC_KEY_VALIDATE(PK);
}

/* IEEE1363 ECIES encryption. Encryption of plaintext M uses public key W and produces ciphertext V,C,T */
void ECP_SECP256K1_ECIES_ENCRYPT(int sha,octet *P1,octet *P2,csprng *RNG,octet *W,octet *M,int tlen,octet *V,octet *C,octet *T)
{

    int i,len;
    char z[EFS_SECP256K1],vz[3*EFS_SECP256K1+1],k[2*AESKEY_SECP256K1],k1[AESKEY_SECP256K1],k2[AESKEY_SECP256K1],l2[8],u[EFS_SECP256K1];
    octet Z= {0,sizeof(z),z};
    octet VZ= {0,sizeof(vz),vz};
    octet K= {0,sizeof(k),k};
    octet K1= {0,sizeof(k1),k1};
    octet K2= {0,sizeof(k2),k2};
    octet L2= {0,sizeof(l2),l2};
    octet U= {0,sizeof(u),u};

    if (ECP_SECP256K1_KEY_PAIR_GENERATE(RNG,&U,V)!=0) return;
    if (ECP_SECP256K1_SVDP_DH(&U,W,&Z)!=0) return;

    OCT_copy(&VZ,V);
    OCT_joctet(&VZ,&Z);

    KDF2(sha,&VZ,P1,2*AESKEY_SECP256K1,&K);

    K1.len=K2.len=AESKEY_SECP256K1;
    for (i=0; i<AESKEY_SECP256K1; i++)
    {
        K1.val[i]=K.val[i];
        K2.val[i]=K.val[AESKEY_SECP256K1+i];
    }

    AES_CBC_IV0_ENCRYPT(&K1,M,C);

    OCT_jint(&L2,P2->len,8);

    len=C->len;
    OCT_joctet(C,P2);
    OCT_joctet(C,&L2);
    AMCL_(HMAC)(sha,C,&K2,tlen,T);
    C->len=len;
}

/* IEEE1363 ECIES decryption. Decryption of ciphertext V,C,T using private key U outputs plaintext M */
int ECP_SECP256K1_ECIES_DECRYPT(int sha,octet *P1,octet *P2,octet *V,octet *C,octet *T,octet *U,octet *M)
{

    int i,len;
    char z[EFS_SECP256K1],vz[3*EFS_SECP256K1+1],k[2*AESKEY_SECP256K1],k1[AESKEY_SECP256K1],k2[AESKEY_SECP256K1],l2[8],tag[32];
    octet Z= {0,sizeof(z),z};
    octet VZ= {0,sizeof(vz),vz};
    octet K= {0,sizeof(k),k};
    octet K1= {0,sizeof(k1),k1};
    octet K2= {0,sizeof(k2),k2};
    octet L2= {0,sizeof(l2),l2};
    octet TAG= {0,sizeof(tag),tag};

    if (ECP_SECP256K1_SVDP_DH(U,V,&Z)!=0) return 0;

    OCT_copy(&VZ,V);
    OCT_joctet(&VZ,&Z);

    KDF2(sha,&VZ,P1,2*AESKEY_SECP256K1,&K);

    K1.len=K2.len=AESKEY_SECP256K1;
    for (i=0; i<AESKEY_SECP256K1; i++)
    {
        K1.val[i]=K.val[i];
        K2.val[i]=K.val[AESKEY_SECP256K1+i];
    }

    if (!AES_CBC_IV0_DECRYPT(&K1,C,M)) return 0;

    OCT_jint(&L2,P2->len,8);

    len=C->len;
    OCT_joctet(C,P2);
    OCT_joctet(C,&L2);
    AMCL_(HMAC)(sha,C,&K2,T->len,&TAG);
    C->len=len;

    if (!OCT_ncomp(T,&TAG,T->len)) return 0;

    return 1;

}

#endif
