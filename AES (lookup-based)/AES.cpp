#include "AES.h"


u32 small2big(u32 small)
{
	u32 big = (u32)((small & 0x000000ff) << 24) | (u32)((small & 0x0000ff00) << 8) | (u32)((small & 0x00ff0000) >> 8) | (u32)((small & 0xff000000) >> 24);
	return big;
}

void key_expansion(u8* key, u32* roundKey)
{
	//arrange key input column-wise
	u32 key0 = GETU32(key);
	u32 key1 = GETU32(key + 4);
	u32 key2 = GETU32(key + 8);
	u32 key3 = GETU32(key + 12);

	//===test===
	//small2big(key0);
	//printf("\n%0x %0x %0x %0x\n", key0, key1, key2, key3);	//small end

	for (int i = 0; i < AES_ROUND; i++)
	{
		*(roundKey + 4 * i + 0) = key0 ^ ((u32)S[(key3 >> 8) & 0xff]) ^ ((u32)S[(key3 >> 16) & 0xff] << 8) ^ ((u32)S[(key3 >> 24) & 0xff] << 16) ^ ((u32)S[(key3) & 0xff] << 24) ^ Rcon[i];
		key0 = *(roundKey + 4 * i + 0);
		*(roundKey + 4 * i + 1) = key0 ^ key1;
		key1 = *(roundKey + 4 * i + 1);
		*(roundKey + 4 * i + 2) = key1 ^ key2;
		key2 = *(roundKey + 4 * i + 2);
		*(roundKey + 4 * i + 3) = key2 ^ key3;
		key3 = *(roundKey + 4 * i + 3);
	}

	for (int i = 0; i < 4 * AES_ROUND; i++)
		roundKey[i] = small2big(roundKey[i]);

	printf("round keys\n");
	for (int i = 0; i < AES_ROUND; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			printf("%08x ", roundKey[4 * i + j]);
		}
		printf("\n");
	}
	printf("\n");
}

void AES_enc(u8* state, u8* c, u8* key) //key operations are column-wise, therefore key is stored column-wise, so are blocks
{
	//assert(m && c && key);
	
	//key expansion
	u32 roundKey[4 * AES_ROUND] = { 0 };
	key_expansion(key, roundKey);

	//AddRoundKey
	for (int i = 0; i < 16; i++)
		state[i] ^= key[i];
	
	printf("\nxor main key: \n");
	for (int i = 0; i < 4; i++)
		printf("%02x%02x%02x%02x ", state[4*i],state[4*i+1],state[4*i+2],state[4*i+3]);

	u32 s0, s1, s2, s3;

	printf("\nafter round encryption: \n");
	for (int r = 0; r < AES_ROUND - 1; r++)
	{
		s0 = Te0[*(state + 0)] ^ Te1[*(state + 5)] ^ Te2[*(state + 10)] ^ Te3[*(state + 15)];
		s0 = small2big(s0);
		s0 ^= roundKey[4 * r + 0];
		s1 = Te0[*(state + 4)] ^ Te1[*(state + 9)] ^ Te2[*(state + 14)] ^ Te3[*(state + 3)];
		s1 = small2big(s1);
		s1 ^= roundKey[4 * r + 1];
		s2 = Te0[*(state + 8)] ^ Te1[*(state + 13)] ^ Te2[*(state + 2)] ^ Te3[*(state + 7)];
		s2 = small2big(s2);
		s2 ^= roundKey[4 * r + 2];
		s3 = Te0[*(state + 12)] ^ Te1[*(state + 1)] ^ Te2[*(state + 6)] ^ Te3[*(state + 11)];
		s3 = small2big(s3);
		s3 ^= roundKey[4 * r + 3];
		printf("%08x %08x %08x %08x\n", s0, s1, s2, s3);
		for (int i = 0; i < 4; i++)
		{
			state[i] = (s0 >> 8 * (3 - i)) & 0xff;
			state[4 + i] = (s1 >> 8 * (3 - i)) & 0xff;
			state[8 + i] = (s2 >> 8 * (3 - i)) & 0xff;
			state[12 + i] = (s3 >> 8 * (3 - i)) & 0xff;
		}
	}

	//last round
	s0 = ((S[state[0]] & 0xff) << 24) + ((S[state[5]] & 0xff) << 16) + ((S[state[10]] & 0xff) << 8) + (S[state[15]] & 0xff);
	s0 ^= roundKey[4 * (AES_ROUND - 1) + 0];
	printf("%0x ", s0);
	s1 = ((S[state[4]] & 0xff) << 24) + ((S[state[9]] & 0xff) << 16) + ((S[state[14]] & 0xff) << 8) + (S[state[3]] & 0xff);
	s1 ^= roundKey[4 * (AES_ROUND - 1) + 1];
	printf("%0x ", s1);
	s2 = ((S[state[8]] & 0xff) << 24) + ((S[state[13]] & 0xff) << 16) + ((S[state[2]] & 0xff) << 8) + (S[state[7]] & 0xff);
	s2 ^= roundKey[4 * (AES_ROUND - 1) + 2];
	printf("%0x ", s2);
	s3 = ((S[state[12]] & 0xff) << 24) + ((S[state[1]] & 0xff) << 16) + ((S[state[6]] & 0xff) << 8) + (S[state[11]] & 0xff);
	s3 ^= roundKey[4 * (AES_ROUND - 1) + 3];
	printf("%0x\n", s3);

	for (int i = 0; i < 4; i++)
	{
		c[i] = (s0 >> 8 * (3 - i)) & 0xff;
		c[4 + i] = (s1 >> 8 * (3 - i)) & 0xff;
		c[8 + i] = (s2 >> 8 * (3 - i)) & 0xff;
		c[12 + i] = (s3 >> 8 * (3 - i)) & 0xff;
	}
}


int main()
{
	//u8 m[16] = { 0xacU, 0x0aU, 0x7fU, 0x8cU, 0x2fU, 0xaaU, 0xc4U, 0x97U, 0x75U, 0xa6U, 0x16U, 0xb7U, 0xc0U, 0xccU, 0x21U, 0xd8U };
	//u8 mainKey[16] = { 0x07U, 0x01U, 0x02U, 0x03U, 0x04U, 0x05U, 0x06U, 0x07U, 0x08U, 0x09U, 0x0aU, 0x0bU, 0x0cU, 0x0dU, 0x0eU,0x0fU };
	//u8 mainKey[16] = { 0x2b,0x7e,0x15,0x16,0x28,0xae,0xd2,0xab,0xab,0xf7,0x15,0x88,0x09,0xcf,0x4f,0x3c };
	u8 m[16] = { 0x54U, 0x77U, 0x6FU, 0x20U, 0x4FU, 0x6EU, 0x65U, 0x20U, 0x4EU, 0x69U, 0x6EU, 0x65U, 0x20U, 0x54U, 0x77U, 0x6FU };
	u8 mainKey[16] = { 0x54U, 0x68U, 0x61U, 0x74U, 0x73U, 0x20U, 0x6DU, 0x79U, 0x20U, 0x4BU, 0x75U, 0x6EU, 0x67U, 0x20U, 0x46U, 0x75U };
	printf("plaintext: \n");
	for (int i = 0; i < 16; i++)
		printf("%02x ", m[i]);
	printf("\nmain key: \n");
	for (int i = 0; i < 16; i++)
		printf("%02x ", mainKey[i]);
	printf("\n\n");
	u8 c[16] = { 0 };
	AES_enc(m, c, mainKey);
	printf("\nciphertext: \n");
	for (int i = 0; i < 16; i++)
		printf("%02x ", c[i]);
	return 0;
}