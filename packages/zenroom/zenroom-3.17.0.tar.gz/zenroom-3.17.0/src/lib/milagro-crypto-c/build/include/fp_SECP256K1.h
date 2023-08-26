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

/**
 * @file fp_SECP256K1.h
 * @author Mike Scott
 * @brief FP Header File
 *
 */

#ifndef FP_SECP256K1_H
#define FP_SECP256K1_H

#include "big_256_28.h"
#include "config_field_SECP256K1.h"


/**
	@brief FP Structure - quadratic extension field
*/

typedef struct
{
    BIG_256_28 g;	/**< Big representation of field element */
    sign32 XES;	/**< Excess */
} FP_SECP256K1;


/* Field Params - see rom.c */
extern const BIG_256_28 Modulus_SECP256K1;	/**< Actual Modulus set in romf_yyy.c */
extern const BIG_256_28 R2modp_SECP256K1;	/**< Montgomery constant */
extern const chunk MConst_SECP256K1;		/**< Constant associated with Modulus - for Montgomery = 1/p mod 2^BASEBITS */


#define MODBITS_SECP256K1 MBITS_SECP256K1                        /**< Number of bits in Modulus for selected curve */
#define TBITS_SECP256K1 (MBITS_SECP256K1%BASEBITS_256_28)           /**< Number of active bits in top word */
#define TMASK_SECP256K1 (((chunk)1<<TBITS_SECP256K1)-1)          /**< Mask for active bits in top word */
#define FEXCESS_SECP256K1 (((sign32)1<<MAXXES_SECP256K1)-1)	     /**< 2^(BASEBITS*NLEN-MODBITS)-1 - normalised BIG can be multiplied by less than this before reduction */
#define OMASK_SECP256K1 (-((chunk)(1)<<TBITS_SECP256K1))         /**<  for masking out overflow bits */

//#define FUSED_MODMUL
//#define DEBUG_REDUCE

/* FP prototypes */

/**	@brief Tests for FP equal to zero mod Modulus
 *
	@param x BIG number to be tested
	@return 1 if zero, else returns 0
 */
extern int FP_SECP256K1_iszilch(FP_SECP256K1 *x);


/**	@brief Set FP to zero
 *
	@param x FP number to be set to 0
 */
extern void FP_SECP256K1_zero(FP_SECP256K1 *x);

/**	@brief Copy an FP
 *
	@param y FP number to be copied to
	@param x FP to be copied from
 */
extern void FP_SECP256K1_copy(FP_SECP256K1 *y,FP_SECP256K1 *x);

/**	@brief Copy from ROM to an FP
 *
	@param y FP number to be copied to
	@param x BIG to be copied from ROM
 */
extern void FP_SECP256K1_rcopy(FP_SECP256K1 *y,const BIG_256_28 x);


/**	@brief Compares two FPs
 *
	@param x FP number
	@param y FP number
	@return 1 if equal, else returns 0
 */
extern int FP_SECP256K1_equals(FP_SECP256K1 *x,FP_SECP256K1 *y);


/**	@brief Conditional constant time swap of two FP numbers
 *
	Conditionally swaps parameters in constant time (without branching)
	@param x an FP number
	@param y another FP number
	@param s swap takes place if not equal to 0
 */
extern void FP_SECP256K1_cswap(FP_SECP256K1 *x,FP_SECP256K1 *y,int s);
/**	@brief Conditional copy of FP number
 *
	Conditionally copies second parameter to the first (without branching)
	@param x an FP number
	@param y another FP number
	@param s copy takes place if not equal to 0
 */
extern void FP_SECP256K1_cmove(FP_SECP256K1 *x,FP_SECP256K1 *y,int s);
/**	@brief Converts from BIG integer to residue form mod Modulus
 *
	@param x BIG number to be converted
	@param y FP result
 */
extern void FP_SECP256K1_nres(FP_SECP256K1 *y,BIG_256_28 x);
/**	@brief Converts from residue form back to BIG integer form
 *
	@param y FP number to be converted to BIG
	@param x BIG result
 */
extern void FP_SECP256K1_redc(BIG_256_28 x,FP_SECP256K1 *y);
/**	@brief Sets FP to representation of unity in residue form
 *
	@param x FP number to be set equal to unity.
 */
extern void FP_SECP256K1_one(FP_SECP256K1 *x);
/**	@brief Reduces DBIG to BIG exploiting special form of the modulus
 *
	This function comes in different flavours depending on the form of Modulus that is currently in use.
	@param r BIG number, on exit = d mod Modulus
	@param d DBIG number to be reduced
 */
extern void FP_SECP256K1_mod(BIG_256_28 r,DBIG_256_28 d);

#ifdef FUSED_MODMUL
extern void FP_SECP256K1_modmul(BIG_256_28,BIG_256_28,BIG_256_28);
#endif

/**	@brief Fast Modular multiplication of two FPs, mod Modulus
 *
	Uses appropriate fast modular reduction method
	@param x FP number, on exit the modular product = y*z mod Modulus
	@param y FP number, the multiplicand
	@param z FP number, the multiplier
 */
extern void FP_SECP256K1_mul(FP_SECP256K1 *x,FP_SECP256K1 *y,FP_SECP256K1 *z);
/**	@brief Fast Modular multiplication of an FP, by a small integer, mod Modulus
 *
	@param x FP number, on exit the modular product = y*i mod Modulus
	@param y FP number, the multiplicand
	@param i a small number, the multiplier
 */
extern void FP_SECP256K1_imul(FP_SECP256K1 *x,FP_SECP256K1 *y,int i);
/**	@brief Fast Modular squaring of an FP, mod Modulus
 *
	Uses appropriate fast modular reduction method
	@param x FP number, on exit the modular product = y^2 mod Modulus
	@param y FP number, the number to be squared

 */
extern void FP_SECP256K1_sqr(FP_SECP256K1 *x,FP_SECP256K1 *y);
/**	@brief Modular addition of two FPs, mod Modulus
 *
	@param x FP number, on exit the modular sum = y+z mod Modulus
	@param y FP number
	@param z FP number
 */
extern void FP_SECP256K1_add(FP_SECP256K1 *x,FP_SECP256K1 *y,FP_SECP256K1 *z);
/**	@brief Modular subtraction of two FPs, mod Modulus
 *
	@param x FP number, on exit the modular difference = y-z mod Modulus
	@param y FP number
	@param z FP number
 */
extern void FP_SECP256K1_sub(FP_SECP256K1 *x,FP_SECP256K1 *y,FP_SECP256K1 *z);
/**	@brief Modular division by 2 of an FP, mod Modulus
 *
	@param x FP number, on exit =y/2 mod Modulus
	@param y FP number
 */
extern void FP_SECP256K1_div2(FP_SECP256K1 *x,FP_SECP256K1 *y);
/**	@brief Fast Modular exponentiation of an FP, to the power of a BIG, mod Modulus
 *
	@param x FP number, on exit  = y^z mod Modulus
	@param y FP number
	@param z BIG number exponent
 */
extern void FP_SECP256K1_pow(FP_SECP256K1 *x,FP_SECP256K1 *y,BIG_256_28 z);
/**	@brief Fast Modular square root of a an FP, mod Modulus
 *
	@param x FP number, on exit  = sqrt(y) mod Modulus
	@param y FP number, the number whose square root is calculated

 */
extern void FP_SECP256K1_sqrt(FP_SECP256K1 *x,FP_SECP256K1 *y);
/**	@brief Modular negation of a an FP, mod Modulus
 *
	@param x FP number, on exit = -y mod Modulus
	@param y FP number
 */
extern void FP_SECP256K1_neg(FP_SECP256K1 *x,FP_SECP256K1 *y);
/**	@brief Outputs an FP number to the console
 *
	Converts from residue form before output
	@param x an FP number
 */
extern void FP_SECP256K1_output(FP_SECP256K1 *x);
/**	@brief Outputs an FP number to the console, in raw form
 *
	@param x a BIG number
 */
extern void FP_SECP256K1_rawoutput(FP_SECP256K1 *x);
/**	@brief Reduces possibly unreduced FP mod Modulus
 *
	@param x FP number, on exit reduced mod Modulus
 */
extern void FP_SECP256K1_reduce(FP_SECP256K1 *x);
/**	@brief normalizes FP
 *
	@param x FP number, on exit normalized
 */
extern void FP_SECP256K1_norm(FP_SECP256K1 *x);
/**	@brief Tests for FP a quadratic residue mod Modulus
 *
	@param x FP number to be tested
	@return 1 if quadratic residue, else returns 0 if quadratic non-residue
 */
extern int FP_SECP256K1_qr(FP_SECP256K1 *x);
/**	@brief Modular inverse of a an FP, mod Modulus
 *
	@param x FP number, on exit = 1/y mod Modulus
	@param y FP number
 */
extern void FP_SECP256K1_inv(FP_SECP256K1 *x,FP_SECP256K1 *y);




#endif
