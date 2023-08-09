import string
import secrets
import sympy

# 拡張ユークリッドアルゴリズム
a, b = 0, 0  # (a, b)の初期値を(0, 0)


def ExtEuclid(x, y):
    global a, b
    if(y == 0):
        a, b = 1, 0
        return x
    q, r = x//y, x % y
    d = ExtEuclid(y, r)
    a, b = b, a-b*q
    return d

# 最小公倍数


def lcm(x, y):
    ans = (x*y)//ExtEuclid(x, y)
    return ans

# 逆元


def Inverse(x, p):
    ExtEuclid(x, p)
    a_ = a
    while(a_ < 0):  # 𝑎が負の整数のとき
        a_ += p
    x_inv = a_ % p
    return x_inv

# 素数生成


def Prime(param):
    ans = sympy.randprime(2**(param/2-1), 2**param/2 - 1)
    return ans

# 鍵生成アルゴリズム


def RSAKeyGen(param):
    p, q = Prime(param), Prime(param)
    N = p*q
    e = 65537  # (p−1)(q−1)と互いに素な正整数
    d = Inverse(e, lcm(p-1, q-1))

    return (e, N), (d, N)

# RSA暗号の暗号化アルゴリズム


def RSAEnc(plain_text, public_key):
    e, N = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [pow(i, e, N) for i in plain_integers]
    encrypted_text = ''.join(chr(i) for i in encrypted_integers)

    return encrypted_text

# RSA暗号の復号アルゴリズム


def RSADec(encrypted_text, private_key):
    d, N = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_intergers = [pow(i, d, N) for i in encrypted_integers]
    decrypted_text = ''.join(chr(i) for i in decrypted_intergers)

    return decrypted_text


def sanitize(encrypted_text):
    # UnicodeEncodeError対策
    return encrypted_text.encode('utf-8', 'replace').decode('utf-8')


# パスワード生成


def pass_gen(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # chars += "%&$#()""
    return ''.join(secrets.choice(chars) for x in range(size))

# 初回暗号化時
def data2RSA(plain_text):
    param = 8   # セキュリティパラメータ

    public_key, private_key = RSAKeyGen(param)
    encrypted_text = RSAEnc(plain_text, public_key)
    # decrypted_text = RSADec(encrypted_text, private_key)

    with open("./image/RSA_key.txt", 'w') as f:
        e, N = public_key
        d, N = private_key
        f.write("%s\n%s\n%s\n" % (e, d, N))
    return encrypted_text

# 追加暗号化時
def add_data2RSA(plain_text):
    with open("./image/RSA_key.txt", "r") as f:
        RSA_Key = [s.strip() for s in f.readlines()]
    public_key = int(RSA_Key[0]), int(RSA_Key[2])
    encrypted_text = RSAEnc(plain_text, public_key)
    return encrypted_text

# 復号化
def RSA2Dec(encrypted_text):
    with open("./image/RSA_key.txt", "r") as f:
        RSA_Key = [s.strip() for s in f.readlines()]
    private_key = int(RSA_Key[1]), int(RSA_Key[2])
    decrypted_text = RSADec(encrypted_text, private_key)
    return decrypted_text


import QR_gen

def test():
    pass_size = 12  # パスワード長
    print(data2RSA(pass_gen(pass_size)))
    print("-----")
    tmp = pass_gen(pass_size)
    print(tmp)
    tmp = add_data2RSA(tmp)
    QR_gen.QR_gen_2(tmp)
    print(tmp)
    tmp = RSA2Dec(tmp)
    print(tmp)

test()