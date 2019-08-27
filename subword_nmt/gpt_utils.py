import sys

def bytes_to_unicode():
    """
    Returns list of utf-8 byte and a corresponding list of unicode strings.
    The reversible bpe codes work on unicode strings.
    This means you need a large # of unicode characters in your vocab if you want to avoid UNKs.
    When you're at something like a 10B token dataset you end up needing around 5K for decent coverage.
    This is a signficant percentage of your normal, say, 32K bpe vocab.
    To avoid that, we want lookup tables between utf-8 bytes and unicode strings.
    And avoids mapping to whitespace/control characters the bpe code barfs on.
    """
    _chr = unichr if sys.version_info[0] == 2 else chr
    bs = list(range(ord("!"), ord("~")+1))+list(range(ord("¡"), ord("¬")+1))+list(range(ord("®"), ord("ÿ")+1))
    cs = bs[:]
    n = 0
    for b in range(2**8):
        if b not in bs:
            bs.append(b)
            cs.append(2**8+n)
            n += 1
    cs = [_chr(n) for n in cs]
    return dict(zip(bs, cs))

b2u=bytes_to_unicode()
b2u_rev=dict((v,k) for k,v in b2u.items())

def gpt_encode(s):
    s_utf=s.encode("utf-8")
    s_encoded="".join(b2u[int(c)] for c in s_utf)
    return s_encoded

def gpt_decode(s):
    repr="".join(chr(b2u_rev[c]) for c in s)
    return repr
        
if __name__=="__main__":
    print(b2u)
    print(b2u_rev)
    
    #for line in gpt_encode(sys.stdin):
    #    print(line)


    
        
    
