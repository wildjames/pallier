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


# Notes and thoughts

The pallier system seems to be attractive in the sense that the encryption of two messages, in conjunction with a public key, can be converted into the encryption of the *sum* of the two messages, which is not typically possible. I will admit that the utility of this is not immediately apparent to me, but I can at least appreciate that this is interesting behaviour.

Also, since for now I have little understanding of what I'm doing, I'll not write tests. That can come later, and I'll probably do an initial coarse one by taking a message, encrypting it, decrypting the result, and seeing if it's the same. In the meantime I'll get the key generation working.

I have a bug! My testing is raising an intermittent mismatch between an encoded and decoded message, for example if I use the following:
```
p = 5
q = 7
g = 253
r = 10
```
then messages get garbled. Is one of my checks incorrect? Probably. Look at `calculate_keypair` again.