# Specifications :
# Hash function stream cipher - uses a 'random' input from user to then generate a hash function which is then used as a seed for a psuedo rng
# which can have a variable length unlike the hash function so it can be used for any length plaintext

# Comments throughout explain it


from hashlib import sha256


def plaintext():
    user_input = input("Enter plaintext :").strip()
    cleaned_string = "".join(char for char in user_input if char.isalpha() or char.isspace())
    
    return cleaned_string.strip() # Only includes the letters and spaces of the plaintext

def generate_key():
    print("Smash your keyboard, type random words, or paste random text to generate the key")
    print("Type 'DONE' on a new line to finish")
    
    randomness = [] 
    
    while True:
        randword = input("Enter Randomness >>") # Uses 'random' input from keyborad as the basis for the pseudo random key
        if randword.strip().lower() == "done":
            break
        randomness.append(randword)

    if not randomness:
        print("No randomness provided, Manual Key Generation aborted.")
        return None

    temphash = sha256()
    
    # Generates hash code chunk by chunk instead of one go - more memory efficient if using large inputs 
    
    for bit in randomness:
        temphash.update(bit.encode()) # Changes bit from str to bytes which is need for hash function
        
    bytekey = temphash.digest() # Pads data left in buffer to 64 bytes, compresses output down to a 32 byte output

    print("[+] Randomness has been harvested + hashed")
    print(f"bytekey : {bytekey}")
    print(f"length : {len(bytekey)} bytes")
    
    return bytekey

def stream_cipher(plaintext,seed):

    user_bytes = plaintext
    
    output = bytearray()
    block_interval = 32 # .digest() Outputs blocks of 32 bytes
    counter = 0 # Incremented and added to each string to ensure even if there is a repeated string it will have a different hash, and adds more 'randomness'

    # Input is only alphabet characters, in this case each character is encoded in utf-8 so we can assume size is +1 byte per character
    
    for i in range(0, len(user_bytes), block_interval):     # Start 0, Length of user input in bytes, Interval of block size
        chunk = user_bytes[i : i + block_interval]                 # Slices string in 32 byte intervals

        counter_bytes = counter.to_bytes(8,"big") # Sets counter number to 8 bytes , can count up to 2^64 or 590 Petabytes, Byteorder = big-endian which means MSB first
        stream_block = sha256(seed + counter_bytes).digest() # Extracts a 32 byte block of the user randomness and the changing counter variable
        
        output.extend(c ^ s for c, s in zip(chunk,stream_block)) # Bitwise XOR, .extend() is used as processed_chunk is iterable

        counter += 1

    return bytes(output) # Changes output from a mutable bytesarray to an immutable bytes

my_seed = generate_key()

text = plaintext().encode()

ciphertext = stream_cipher(text,my_seed)

print(f"\nCiphertext (Hex): {ciphertext.hex()}")
    
decrypted_bytes = stream_cipher(ciphertext, my_seed)

print(f"\nDecrypted Plaintext: {decrypted_bytes.decode("utf-8")}")   
    



    




        
