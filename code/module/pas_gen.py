import string
import secrets

pass_size = 12

def pass_gen(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # chars += "%&$#()""
    return ''.join(secrets.choice(chars) for x in range(size))

print(pass_gen(pass_size))
