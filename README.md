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
> 4. Add_homo: takes input two cipher text to performs addition
> 4. Is_Homomorphic : Takes the added cipher text from Add_homo() and checks its homomorphic property . Returns  True / False
> 
> Use Gympy2 library for all the integers used in the implementation.

I will keep some notes here, with my thoughts as I go through. One initial note, however, I use `conda` for my virtual environments. In this case, setup is simply:

```
conda create -n pallier python==3.10
conda activate pallier
pip install -U pip
pip install -r requirements.txt
```

To run a demo, just open a terminal and run `python3 main.py`. Otherwise, the important functions are in `paillier_parser.py` script, with the workhorse functions in the `helper.py` script. 


# Notes and thoughts

The pallier system seems to be attractive in the sense that the encryption of two messages, in conjunction with a public key, can be converted into the encryption of the *sum* of the two messages, which is not typically possible. I will admit that the utility of this is not immediately apparent to me, but I can at least appreciate that this is interesting behaviour.

Also, since for now I have little understanding of what I'm doing, I'll not write tests. That can come later, and I'll probably do an initial coarse one by taking a message, encrypting it, decrypting the result, and seeing if it's the same. In the meantime I'll get the key generation working.

---

I have a bug! My testing is raising an intermittent mismatch between an encoded and decoded message, for example if I use the following:
```
p = 5
q = 7
g = 253
r = 10
```
then messages get garbled. Is one of my checks incorrect? Probably. Look at `calculate_keypair` again. Further testing reveals that a different selection of `r` results in a correct decryption. For example, `r = 22` works, but `r = 7` or `15` doesn't. The selection of `r`, according to wikipedia is simply a random number `0 < r < n`. Further investigation reveals that the decryption does not match the original message in cases where `r` is not coprime with n; in this case, `n = 35`, with factors `5, 7`. This is not specified in the wikipedia page, from which I am getting the algorithm, and I don't see a mention of it in the paper either.

---

Can I construct a failure state based off this understanding. Take the primes `11` and `3`, and choose a value of `g = 34`, which satisfies the conditions for `g`. Then, choosing a value of `r = {15, 12, 11, 9, 22}` will induce a corrupted message, but values of `r = {13, 14, 8, 20}` results in the expected recovery of the message. Do I need a check for this condition?

---

Found it! I was missing a check in the encrypt function - the encrypted message had to be coprime with n, as I found from my tests; this was actually stipulated in the wikipedia page, I just missed it. Fixed now, by checking in both the encrypt and decrypt functions.

---

I've got the specified tasks done, and I'm reasonably happy with the result. I'm sure there is some optimisation to be done here, as generating keypairs with primes longer than about 5-6 digits can take a pretty long time on my laptop. This will do for an initial implementation, though. If I were to spend more time on this, I would make an optimisation branch and work there.

The last thing I want to do before leaving this is to write some tests for just the encryption and decryption functions, as currently I only test them together.