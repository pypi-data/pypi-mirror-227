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

#include "ecdh_BLS381.h"

/* Calculate a public/private EC GF(p) key pair. W=S.G mod EC(p),
 * where S is the secret key and W is the public key
 * and G is fixed generator.
 * If RNG is NULL then the private key is provided externally in S
 * otherwise it is generated randomly internally */
int ECP_BLS381_KEY_PAIR_GENERATE(csprng *RNG,octet* S,octet *W)
{
    BIG_384_29 r,s;
    ECP_BLS381 G;
    int res=0;

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);
    if (RNG!=NULL)
    {
        BIG_384_29_randomnum(s,r,RNG);
    }
    else
    {
        BIG_384_29_fromBytes(s,S->val);
        BIG_384_29_mod(s,r);
    }

#ifdef AES_S
    BIG_384_29_mod2m(s,2*AES_S);
#endif

    S->len=EGS_BLS381;
    BIG_384_29_toBytes(S->val,s);

    ECP_BLS381_mul(&G,s);

    ECP_BLS381_toOctet(W,&G,false);  /* To use point compression on public keys, change to true */

    return res;
}

/* Validate public key */
int ECP_BLS381_PUBLIC_KEY_VALIDATE(octet *W)
{
    BIG_384_29 q,r,k;
    ECP_BLS381 WP;
    int valid,nb;
    int res=0;

    BIG_384_29_rcopy(q,Modulus_BLS381);
    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    valid=ECP_BLS381_fromOctet(&WP,W);
    if (!valid) res=ECDH_INVALID_PUBLIC_KEY;

    if (res==0)
    {
        /* Check point is not in wrong group */
        nb=BIG_384_29_nbits(q);
        BIG_384_29_one(k);
        BIG_384_29_shl(k,(nb+4)/2);
        BIG_384_29_add(k,q,k);
        BIG_384_29_sdiv(k,r); /* get co-factor */

        while (BIG_384_29_parity(k)==0)
        {
            ECP_BLS381_dbl(&WP);
            BIG_384_29_fshr(k,1);
        }

        if (!BIG_384_29_isunity(k)) ECP_BLS381_mul(&WP,k);
        if (ECP_BLS381_isinf(&WP)) res=ECDH_INVALID_PUBLIC_KEY;
    }

    return res;
}

/* IEEE-1363 Diffie-Hellman online calculation Z=S.WD */
int ECP_BLS381_SVDP_DH(octet *S,octet *WD,octet *Z)
{
    BIG_384_29 r,s,wx;
    int valid;
    ECP_BLS381 W;
    int res=0;

    BIG_384_29_fromBytes(s,S->val);

    valid=ECP_BLS381_fromOctet(&W,WD);

    if (!valid) res=ECDH_ERROR;
    if (res==0)
    {
        BIG_384_29_rcopy(r,CURVE_Order_BLS381);
        BIG_384_29_mod(s,r);

        ECP_BLS381_mul(&W,s);
        if (ECP_BLS381_isinf(&W)) res=ECDH_ERROR;
        else
        {
#if CURVETYPE_BLS381!=MONTGOMERY
            ECP_BLS381_get(wx,wx,&W);
#else
            ECP_BLS381_get(wx,&W);
#endif
            Z->len=MODBYTES_384_29;
            BIG_384_29_toBytes(Z->val,wx);
        }
    }
    return res;
}

#if CURVETYPE_BLS381!=MONTGOMERY

/* IEEE ECDSA Signature, C and D are signature on F using private key S */
int ECP_BLS381_SP_DSA(int sha,csprng *RNG,octet *K,octet *S,octet *F,octet *C,octet *D)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_384_29 r,s,f,c,d,u,vx,w;
    ECP_BLS381 G,V;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    BIG_384_29_fromBytes(s,S->val);

    int hlen=H.len;
    if (H.len>MODBYTES_384_29) hlen=MODBYTES_384_29;
    BIG_384_29_fromBytesLen(f,H.val,hlen);

    if (RNG!=NULL)
    {
        do
        {
            BIG_384_29_randomnum(u,r,RNG);
            BIG_384_29_randomnum(w,r,RNG); /* side channel masking */

#ifdef AES_S
            BIG_384_29_mod2m(u,2*AES_S);
#endif
            ECP_BLS381_copy(&V,&G);
            ECP_BLS381_mul(&V,u);

            ECP_BLS381_get(vx,vx,&V);

            BIG_384_29_copy(c,vx);
            BIG_384_29_mod(c,r);
            if (BIG_384_29_iszilch(c)) continue;

            BIG_384_29_modmul(u,u,w,r);

            BIG_384_29_invmodp(u,u,r);
            BIG_384_29_modmul(d,s,c,r);

            BIG_384_29_add(d,f,d);

            BIG_384_29_modmul(d,d,w,r);

            BIG_384_29_modmul(d,u,d,r);
        }
        while (BIG_384_29_iszilch(d));
    }
    else
    {
        BIG_384_29_fromBytes(u,K->val);
        BIG_384_29_mod(u,r);

#ifdef AES_S
        BIG_384_29_mod2m(u,2*AES_S);
#endif
        ECP_BLS381_copy(&V,&G);
        ECP_BLS381_mul(&V,u);

        ECP_BLS381_get(vx,vx,&V);

        BIG_384_29_copy(c,vx);
        BIG_384_29_mod(c,r);
        if (BIG_384_29_iszilch(c)) return ECDH_ERROR;


        BIG_384_29_invmodp(u,u,r);
        BIG_384_29_modmul(d,s,c,r);

        BIG_384_29_add(d,f,d);

        BIG_384_29_modmul(d,u,d,r);
        if (BIG_384_29_iszilch(d)) return ECDH_ERROR;
    }

    C->len=D->len=EGS_BLS381;

    BIG_384_29_toBytes(C->val,c);
    BIG_384_29_toBytes(D->val,d);

    return 0;
}

/* RFC6979 Section 3 https://www.rfc-editor.org/rfc/rfc6979 */
/* IEEE ECDSA Deterministic Signature, C and D are signature on F using private key S.
octU is the deterministic parameter k in the RFC6979.*/
int ECP_BLS381_SP_DSA_DET(int sha,octet *S,octet *F,octet *C,octet *D, octet *octU)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_384_29 r,s,f,c,d,u,vx,vy,w;
    ECP_BLS381 G,V;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);
    
    int rBytes = (BIG_384_29_nbits(r) + 7)/8;

    char temp[rBytes], vec[sha], k[sha], ch[rBytes], conc[sha + 1 + (2*rBytes)];

    octet octS = {rBytes, sizeof(temp), temp};
    OCT_copy(&octS, S);
    OCT_pad(&octS, rBytes);

    BIG_384_29_fromBytes(s, octS.val);

    int hlen=H.len;
    if (H.len>MODBYTES_384_29) hlen=MODBYTES_384_29;
// f correspond to bits2int(H(m)) mod q in the paper
    BIG_384_29_fromBytesLen(f,H.val,hlen);
    
// VEC = V in the paper
    octet VEC = {0, sizeof(vec), vec};
    OCT_jbyte(&VEC, 1, H.len);

    octet K = {0, sizeof(k), k};
    OCT_jint(&K, 0, H.len);

//octH = bits2octet(h1) in the paper
    octet octH = {rBytes, sizeof(ch), ch};
    BIG_384_29_toBytes(octH.val, f);
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

        BIG_384_29_fromBytesLen(u, T.val, rBytes); //u = k in the paper

        ECP_BLS381_copy(&V,&G);
        ECP_BLS381_mul(&V,u);
        ECP_BLS381_get(vx,vy, &V);
        BIG_384_29_copy(c,vx);
        BIG_384_29_mod(c,r);

        check_k = BIG_384_29_iszilch(u) || BIG_384_29_comp(u, r) >= 0 || BIG_384_29_iszilch(c);
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
        BIG_384_29_toBytes(octU->val, u);  
    }
    BIG_384_29_invmodp(u,u,r);
    BIG_384_29_modmul(d,s,c,r);

    BIG_384_29_add(d,f,d);

    BIG_384_29_modmul(d,u,d,r);
    if (BIG_384_29_iszilch(d)) return ECDH_ERROR;

    C->len=D->len=EGS_BLS381;

    BIG_384_29_toBytes(C->val,c);
    BIG_384_29_toBytes(D->val,d);

    return 0;
}

/* RFC6979 ECDSA DETERMINISTIC Signature as above, without hash on input (assume as already hashed) */
int ECP_BLS381_SP_DSA_DET_NOHASH(int sha, octet *S,octet *H,octet *C,octet *D, int *y_parity)
// substituted F with H in args
{
    BIG_384_29 r,s,f,c,d,u,vx,vy;
    ECP_BLS381 G,V;

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    int rBytes = (BIG_384_29_nbits(r) + 7)/8;

    char temp[rBytes], vec[sha], k[sha], ch[rBytes], conc[sha + 1 + (2*rBytes)];

    octet octS = {rBytes, sizeof(temp), temp};
    OCT_copy(&octS, S);
    OCT_pad(&octS, rBytes);

    BIG_384_29_fromBytes(s, octS.val);

    int hlen=H->len;
    if (H->len>MODBYTES_384_29) hlen=MODBYTES_384_29;
    BIG_384_29_fromBytesLen(f,H->val,hlen);

// VEC = V in the paper
    octet VEC = {0, sizeof(vec), vec};
    OCT_jbyte(&VEC, 1, H->len);

    octet K = {0, sizeof(k), k};
    OCT_jint(&K, 0, H->len);

//octH = bits2octet(h1) in the paper
    octet octH = {rBytes, sizeof(ch), ch};
    BIG_384_29_toBytes(octH.val, f);
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

        BIG_384_29_fromBytesLen(u, T.val, rBytes); //u = k in the paper

        ECP_BLS381_copy(&V,&G);
        ECP_BLS381_mul(&V,u);
        ECP_BLS381_get(vx,vy, &V);
        BIG_384_29_copy(c,vx);
        BIG_384_29_mod(c,r);

        check_k = BIG_384_29_iszilch(u) || BIG_384_29_comp(u, r) >= 0 || BIG_384_29_iszilch(c);
        if(check_k){
            octet CONC2 = {0, sizeof(t),t};
            OCT_copy(&CONC2, &VEC);
            OCT_jbyte(&CONC2, 0, 1);
            AMCL_(HMAC)(sha,&CONC2,&K, sha, &K);
            AMCL_(HMAC)(sha,&VEC,&K, sha, &VEC);
        }

    } while(check_k);
    
    BIG_384_29_invmodp(u,u,r);
    BIG_384_29_modmul(d,s,c,r);

    BIG_384_29_add(d,f,d);

    BIG_384_29_modmul(d,u,d,r);
    if (BIG_384_29_iszilch(d)) return ECDH_ERROR;

    if(y_parity) {
      *y_parity = BIG_384_29_parity(vy);
    }

    C->len=D->len=EGS_BLS381;

    BIG_384_29_toBytes(C->val,c);
    BIG_384_29_toBytes(D->val,d);

    return 0;
}

/* IEEE ECDSA Signature as above, without hash on input (assume as already hashed) */
int ECP_BLS381_SP_DSA_NOHASH(int sha,csprng *RNG,octet *K,octet *S,octet *H,octet *C,octet *D, int *y_parity)
// substituted F with H in args
{
    BIG_384_29 r,s,f,c,d,u,vx,vy,w;
    ECP_BLS381 G,V;

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    BIG_384_29_fromBytes(s,S->val);

    int hlen=H->len;
    if (H->len>MODBYTES_384_29) hlen=MODBYTES_384_29;
    BIG_384_29_fromBytesLen(f,H->val,hlen);

    if (RNG!=NULL)
    {
        do
        {
            BIG_384_29_randomnum(u,r,RNG);
            BIG_384_29_randomnum(w,r,RNG); /* side channel masking */

#ifdef AES_S
            BIG_384_29_mod2m(u,2*AES_S);
#endif
            ECP_BLS381_copy(&V,&G);
            ECP_BLS381_mul(&V,u);

            ECP_BLS381_get(vx,vy,&V);
            BIG_384_29_copy(c,vx);
            BIG_384_29_mod(c,r);
            if (BIG_384_29_iszilch(c)) continue;

            BIG_384_29_modmul(u,u,w,r);

            BIG_384_29_invmodp(u,u,r);
            BIG_384_29_modmul(d,s,c,r);

            BIG_384_29_add(d,f,d);

            BIG_384_29_modmul(d,d,w,r);

            BIG_384_29_modmul(d,u,d,r);
        }
        while (BIG_384_29_iszilch(d));
    }
    else
    {
        BIG_384_29_fromBytes(u,K->val);
        BIG_384_29_mod(u,r);

#ifdef AES_S
        BIG_384_29_mod2m(u,2*AES_S);
#endif
        ECP_BLS381_copy(&V,&G);
        ECP_BLS381_mul(&V,u);

        ECP_BLS381_get(vx,vy,&V);
        BIG_384_29_copy(c,vx);
        BIG_384_29_mod(c,r);
        if (BIG_384_29_iszilch(c)) return ECDH_ERROR;


        BIG_384_29_invmodp(u,u,r);
        BIG_384_29_modmul(d,s,c,r);

        BIG_384_29_add(d,f,d);

        BIG_384_29_modmul(d,u,d,r);
        if (BIG_384_29_iszilch(d)) return ECDH_ERROR;
    }
    if(y_parity) {
      *y_parity = BIG_384_29_parity(vy);
    }

    C->len=D->len=EGS_BLS381;

    BIG_384_29_toBytes(C->val,c);
    BIG_384_29_toBytes(D->val,d);

    return 0;
}

/* IEEE1363 ECDSA Signature Verification. Signature C and D on F is verified using public key W */
int ECP_BLS381_VP_DSA_NOHASH(int sha,octet *W,octet *H, octet *C,octet *D)
// substituted F with H in args
{

    BIG_384_29 r,f,c,d,h2;
    int res=0;
    ECP_BLS381 G,WP;
    int valid, clen, dlen;

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    if(C->len > MODBYTES_384_29) {
	OCT_shl(C,C->len-MODBYTES_384_29);
	clen = MODBYTES_384_29;
    }
    else clen = C->len;
    
    if(D->len > MODBYTES_384_29) {
	OCT_shl(D,D->len-MODBYTES_384_29);
	dlen = MODBYTES_384_29;
    }
    else dlen = D->len;

    BIG_384_29_fromBytesLen(c,C->val,clen);
    BIG_384_29_fromBytesLen(d,D->val,dlen);

    int hlen=H->len;
    if (hlen>MODBYTES_384_29) hlen=MODBYTES_384_29;

    BIG_384_29_fromBytesLen(f,H->val,hlen);

    //BIG_fromBytes(f,H->val);

    if (BIG_384_29_iszilch(c) || BIG_384_29_comp(c,r)>=0 || BIG_384_29_iszilch(d) || BIG_384_29_comp(d,r)>=0)
        res=ECDH_INVALID;

    if (res==0)
    {
        BIG_384_29_invmodp(d,d,r);
        BIG_384_29_modmul(f,f,d,r);
        BIG_384_29_modmul(h2,c,d,r);

        valid=ECP_BLS381_fromOctet(&WP,W);

        if (!valid) res=ECDH_ERROR;
        else
        {
            ECP_BLS381_mul2(&WP,&G,h2,f);

            if (ECP_BLS381_isinf(&WP)) res=ECDH_INVALID;
            else
            {
                ECP_BLS381_get(d,d,&WP);
                BIG_384_29_mod(d,r);
                if (BIG_384_29_comp(d,c)!=0) res=ECDH_INVALID;
            }
        }
    }

    return res;
}

/* IEEE1363 ECDSA Signature Verification. Signature C and D on F is verified using public key W */
int ECP_BLS381_VP_DSA(int sha,octet *W,octet *F, octet *C,octet *D)
{
    char h[128];
    octet H= {0,sizeof(h),h};

    BIG_384_29 r,f,c,d,h2;
    int res=0;
    ECP_BLS381 G,WP;
    int valid, clen, dlen;

    ehashit(sha,F,-1,NULL,&H,sha);

    ECP_BLS381_generator(&G);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);

    if(C->len > MODBYTES_384_29) {
	OCT_shl(C,C->len-MODBYTES_384_29);
	clen = MODBYTES_384_29;
    }
    else clen = C->len;
    
    if(D->len > MODBYTES_384_29) {
	OCT_shl(D,D->len-MODBYTES_384_29);
	dlen = MODBYTES_384_29;
    }
    else dlen = D->len;

    BIG_384_29_fromBytesLen(c,C->val,clen);
    BIG_384_29_fromBytesLen(d,D->val,dlen);

    int hlen=H.len;
    if (hlen>MODBYTES_384_29) hlen=MODBYTES_384_29;

    BIG_384_29_fromBytesLen(f,H.val,hlen);

    //BIG_fromBytes(f,H.val);

    if (BIG_384_29_iszilch(c) || BIG_384_29_comp(c,r)>=0 || BIG_384_29_iszilch(d) || BIG_384_29_comp(d,r)>=0)
        res=ECDH_INVALID;

    if (res==0)
    {
        BIG_384_29_invmodp(d,d,r);
        BIG_384_29_modmul(f,f,d,r);
        BIG_384_29_modmul(h2,c,d,r);

        valid=ECP_BLS381_fromOctet(&WP,W);

        if (!valid) res=ECDH_ERROR;
        else
        {
            ECP_BLS381_mul2(&WP,&G,h2,f);

            if (ECP_BLS381_isinf(&WP)) res=ECDH_INVALID;
            else
            {
                ECP_BLS381_get(d,d,&WP);
                BIG_384_29_mod(d,r);
                if (BIG_384_29_comp(d,c)!=0) res=ECDH_INVALID;
            }
        }
    }

    return res;
}

/* From the ephemeral public key (x,y) of a signature (C,D) on H the hash of the message
   recover the public key PK that verifies the singature, if it exists */
int ECP_BLS381_PUBLIC_KEY_RECOVERY(octet *X, int y_parity, octet *H, octet *C, octet *D, octet *PK)
{
    BIG_384_29 x, c, d, h, r;
    ECP_BLS381 P, G_neg;
    int xlen, clen, dlen, hlen;

    if(X->len > MODBYTES_384_29) {
	OCT_shl(X,X->len-MODBYTES_384_29);
	xlen = MODBYTES_384_29;
    }
    else xlen = X->len;
    BIG_384_29_fromBytesLen(x,X->val,xlen);

    if (!ECP_BLS381_setx(&P,x,y_parity)) return -1;

    if(C->len > MODBYTES_384_29) {
	OCT_shl(C,C->len-MODBYTES_384_29);
	clen = MODBYTES_384_29;
    }
    else clen = C->len;
    BIG_384_29_fromBytesLen(c,C->val, clen);

    if(D->len > MODBYTES_384_29) {
	OCT_shl(D,D->len-MODBYTES_384_29);
	dlen = MODBYTES_384_29;
    }
    else dlen = D->len;
    BIG_384_29_fromBytesLen(d,D->val, dlen);

    hlen=H->len;
    if (hlen>MODBYTES_384_29) hlen=MODBYTES_384_29;
    BIG_384_29_fromBytesLen(h,H->val,hlen);

    ECP_BLS381_generator(&G_neg);
    ECP_BLS381_neg(&G_neg);

    ECP_BLS381_mul2(&P,&G_neg,d,h);

    BIG_384_29_rcopy(r,CURVE_Order_BLS381);
    BIG_384_29_invmodp(c,c,r);
    ECP_BLS381_mul(&P,c);

    ECP_BLS381_toOctet(PK,&P,false); //uncompressed public key
    return ECP_BLS381_PUBLIC_KEY_VALIDATE(PK);
}

/* IEEE1363 ECIES encryption. Encryption of plaintext M uses public key W and produces ciphertext V,C,T */
void ECP_BLS381_ECIES_ENCRYPT(int sha,octet *P1,octet *P2,csprng *RNG,octet *W,octet *M,int tlen,octet *V,octet *C,octet *T)
{

    int i,len;
    char z[EFS_BLS381],vz[3*EFS_BLS381+1],k[2*AESKEY_BLS381],k1[AESKEY_BLS381],k2[AESKEY_BLS381],l2[8],u[EFS_BLS381];
    octet Z= {0,sizeof(z),z};
    octet VZ= {0,sizeof(vz),vz};
    octet K= {0,sizeof(k),k};
    octet K1= {0,sizeof(k1),k1};
    octet K2= {0,sizeof(k2),k2};
    octet L2= {0,sizeof(l2),l2};
    octet U= {0,sizeof(u),u};

    if (ECP_BLS381_KEY_PAIR_GENERATE(RNG,&U,V)!=0) return;
    if (ECP_BLS381_SVDP_DH(&U,W,&Z)!=0) return;

    OCT_copy(&VZ,V);
    OCT_joctet(&VZ,&Z);

    KDF2(sha,&VZ,P1,2*AESKEY_BLS381,&K);

    K1.len=K2.len=AESKEY_BLS381;
    for (i=0; i<AESKEY_BLS381; i++)
    {
        K1.val[i]=K.val[i];
        K2.val[i]=K.val[AESKEY_BLS381+i];
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
int ECP_BLS381_ECIES_DECRYPT(int sha,octet *P1,octet *P2,octet *V,octet *C,octet *T,octet *U,octet *M)
{

    int i,len;
    char z[EFS_BLS381],vz[3*EFS_BLS381+1],k[2*AESKEY_BLS381],k1[AESKEY_BLS381],k2[AESKEY_BLS381],l2[8],tag[32];
    octet Z= {0,sizeof(z),z};
    octet VZ= {0,sizeof(vz),vz};
    octet K= {0,sizeof(k),k};
    octet K1= {0,sizeof(k1),k1};
    octet K2= {0,sizeof(k2),k2};
    octet L2= {0,sizeof(l2),l2};
    octet TAG= {0,sizeof(tag),tag};

    if (ECP_BLS381_SVDP_DH(U,V,&Z)!=0) return 0;

    OCT_copy(&VZ,V);
    OCT_joctet(&VZ,&Z);

    KDF2(sha,&VZ,P1,2*AESKEY_BLS381,&K);

    K1.len=K2.len=AESKEY_BLS381;
    for (i=0; i<AESKEY_BLS381; i++)
    {
        K1.val[i]=K.val[i];
        K2.val[i]=K.val[AESKEY_BLS381+i];
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
