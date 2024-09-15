import random
import bitarray
from urllib.parse import urlparse, urlunparse

# TODO:
# Should add multiple mutations randomly per given URL
# Have a list of functions that gets called per mutation
# Call random amount of random functions random times
# Give different weights to the functions


# Main mutator
def url_mutator(i: str) -> str:
    functions = [mutate_scheme, remove_char, 
                 remove_random_chars, multiply_url,
                 do_a_flip, do_many_flips]
    return random.choice(functions)(str(i))
    
# Helper functions

# Mutates schemes
# Weight 0.5
def mutate_scheme(url: str) -> str:
    schemes = ['protocol', 'javascript', 'tor', 
               'http', 'https', 'ftp', 'sftp', 
               'ws', 'wss', 'smtp', 'file', 'imap', 
               'pop3', 'telnet', 'ssh', 'ldap', 'nfs', 
               'git', 'null', 'true']
    
    parsed_url = urlparse(url)
    new_scheme = random.choice(schemes)
    parsed_url = parsed_url._replace(scheme=new_scheme)
    return urlunparse(parsed_url)

# Removes a random character from a given string
# Weight 0.2
def remove_char(s: str) -> str:
    if len(s) == 0:
        return s
    i = random.randint(0, len(s) - 1)
    return s[:i] + s[i+1:]

# Removes a random number of random characters from given string
# Weight 0.2
def remove_random_chars(s: str) -> str:
    if len(s) == 0:
        return s
    l = len(s)
    num_chars_to_remove = random.randint(1, l)
    indices_to_remove = random.sample(range(l), num_chars_to_remove)
    return ''.join(s[i] for i in range(l) if i not in indices_to_remove)

# Multiplies the given url
# Weight 0.1
def multiply_url(s: str) -> str:
    if len(s) == 0:
        return s
    i = random.randint(1,3)
    return s+(s*i)

# Flip a random bits
# Weight 0.5
def do_a_flip(s: str) -> str:
    if len(s) == 0:
        return s
    bits = bitarray.bitarray()
    bits.frombytes(s.encode('utf-8'))
    bit_list = bits.tolist()
    n = random.randint(0, len(bit_list)-1)
    if bit_list[n] == 1:
        bit_list[n] = 0
    else:
        bit_list[n] = 1
    return bitarray.bitarray(bit_list).tobytes().decode('latin-1')

# Flip bits from 0..n
# Weight 0.5
def do_many_flips(s: str) -> str:
    if len(s) == 0:
        return s
    bits = bitarray.bitarray()
    bits.frombytes(s.encode('utf-8'))
    bit_list = bits.tolist()
    n = random.randint(0, len(bit_list)-1 )
    for i in range(0,n):
        if bit_list[i] == 1:
            bit_list[i] = 0
        else:
            bit_list[i] = 1
    return bitarray.bitarray(bit_list).tobytes().decode('latin-1')

if __name__ == "__main__":
    main()
