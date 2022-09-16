# Pallier cryptographics

From Jay: 

> The Paillier cryptosystem, invented by Pascal Paillier in 1999, is a partial homomorphic encryption scheme which allows two types of computation:
> 
> 1. addition of two ciphertexts
> 2. multiplication of a ciphertext by a plaintext number
> 
> Implement Paillier encryption scheme in Python with the following modules and show the Homomorphism property :
> 1. Key Generation: generate public /private Pailier keypair
> 2. Encryption: Encrypt a message m to ouput a cipher text c
> 3. Decryption: Decrypt c to get back m
> 4. Add_homo: takes input two cipher text to  performs addition
> 4. Is_Homomorphic : Takes the added cipher text  from Add_homo() and checks its homomorphic property . Returns  True / False
> 
> Use Gympy2 library for all the integers used in the implementation.

I will keep some notes here, with my thoughts as I go through. One initial note, however, I use `conda` for my virtual environments. In this case, setup is simply:

```
conda create -n pallier python==3.10
conda activate pallier
pip install -U pip
pip install -r requirements.txt
```