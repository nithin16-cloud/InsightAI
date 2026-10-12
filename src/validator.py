# -*- coding: utf-8 -*-
# ==============================================================================
# PROTECTED RUNTIME MODULE — PROPRIETARY INTELLECTUAL PROPERTY
# ALL RIGHTS RESERVED • REVERSE ENGINEERING PROHIBITED
# ==============================================================================
import zlib as _z, base64 as _b
_k = b'\x93\xa1\x7f\xc4.[\x8a\xd0\x1fnB'
_p = (
    b"63uynUM0aWgOkKzM4Jf6sg+ieowwwj6qYH61Iwtw1ojy2k9xiSPaHHhH4245g+oAY6ZV61wklog8smb5"
    b"h4zbsEowW0BMK22c+/Z41wp8d405N2Kq90hR0QzI6QJ6qRiM79aISwWBBCryAFzM9of5/+2i3nILqZ0r"
    b"Fwpr0muQSjP9R5NqQd685+V4lHfm8w37v2ycpMm+R/NgKxEofPhiyRi/yybWwoAfGVoIeoKp8TLSN7pX"
    b"1CBASzhAdqJNdZ8aLx1VUxcMoD7jY2yhbspHCU/aoBOUb7vVwVBI0Sw7MuLE7MvQCZaO1zS2HaqblSBm"
    b"S4m5MyrNJs/gVO+qItK/c52uPMhKS+qoeC3T/OGPLeiGd6z9Kkf8q5a1Rmut1PfvQTWy8tN8Mxdb/Tlv"
    b"MKAuglQzFbGNyOYHn57GTax3FMMYTo8Gq5L2K2wr/UZmCN5Pn2IEiPJ0LX/BPo9mevBG8eMUer3hC8bg"
    b"JbvOII2iYLzO6xw75WYYrMpr50CzXzg6cKrZeKaAWowYk/hb4/rCh7NpIPb2xIj7eNVYLAybbSBR/W/E"
    b"Dt4AJTeOY9R4KF0LwVVmsZE7cN4OOw5+1qN0NuNU/uteFLxbrX2VZ59DNb0wx1N/dixmHzDq0M48WlGB"
    b"raGSp9ksMAfH7xeibRc84ABp+6z0v8gWZ4Gn7hrclNnvWVBYttrCyJ3jE4gMPBpUlZ0CptIYSHBcaUYO"
    b"FkIXujPq9teor0Ff/thg1PR44J0YpcrKoBvAwBZ2MBZBFpeFLSACkxUmzY9dxwMMMUtJ+KgTRxewbxw5"
    b"Ti2fktzOW8fBdLMgmg04uJek8jckcV1O7WLAtY2kBqkJuuwBSYSro5RCWLY1jVGiznxpHoQ4FBhRjI17"
    b"GndTfhnYZtlaqgcTjXtm5hsxT7sFEmLPcFNvnZWJ9hTEu+xrmeCagzVFWiGuzY4FkckLH9cpYikcNplZ"
    b"anWYLK++Qtmw7+JIbfYIO8O9rJOAT1IcYx7TuW24JxhTRBpPLShD2Iwqhpt1Ps7UK0voIEwa5zu651DT"
    b"e822necrKoO+mQan18BVbPVz6nbUHJnUpn+ZfRov/MLALKnWM8aVTvlsxub/AZ9l/0bSCFa7TWyW+smr"
    b"oclbKDS4hXoiypsU2uo8wdj4kvnQTv2HI1X6OuYqMUtLdjTXgGwDbR5H2capYPn8ZFDk4ewHBdxaivsv"
    b"HkoXKOIPMFU8M6Cq5bHdSnytPo9jD9CUHf8cj00g+B5tA13ZyIYusUtJmE6cxYe93QlmBen4xTYYHLLO"
    b"hqzuaq/3/kLpVzkKzHiP1j7wMBHTq0P65fKWgS/lz0eSOhkUupgALv6KSeTVWZQNXvks2GKHP/z5MLye"
    b"ew9TgVBy4KdJycDEejDYfRZp7fR+QGRI9zQ9MDNvPMs0WDWe7LL3KChekAQnHaCtrsY5DSoxOdhCetnX"
    b"e1Yz/nj8CfaaNzoVh0bdm+U5RNu3b+FpDvT0znkp8XPx0v0gMOjTtNwQxqr9DU7nICcEZzJjH0Di0HKq"
    b"dzVldMoQUbq0fzClFsh6ocIf/MS3/84C9P6J93cJgvXrpSmQY7P274Ob8pkpFpxrM39gRZtMSkSNaTcl"
    b"x8yek6WH0EACp4k9aA/BiZZCEW491oCnRzwcjSVYivsRg9BAhGollFpdsDwrtOoxDdSklmr+08j7ugTf"
    b"hhWx4TeNyGLXgsORcOmWvIl1xtWuLpAf3HsyAmDmAPIK/DKjjqL+7wG4bpYw5e8RKXR2nVgVAW4edC5Q"
    b"ZMiO4aLhU6tfZYrYw6h9zPsnsNX2h7mufg8/kzSJTHeiWaTzALvxrtqytsOgq8/EsEkf2AmGi0K3aTzQ"
    b"LZsWG3iKnwAnRM7J30tDDpcwu1/hpSOTW8BC8J9/Uvgg0HnHG1FsZkYcA9t27OalGi4jXqV4yIDPafyx"
    b"zZDTqfDhD8KJnvHHa3sJW5QSz0wbVNWSHLygIoXhneuwcnZjd5AJAJsfOuswEu02DTHOt5wEjbrsuLzP"
    b"Z4yaQyWHqOfcAROisN73K0MoXKL5syMt9E13zx0HyhkWA68Wf9LbeDR/yvbX5vn5PMvc5ycSf5DDDHF6"
    b"nDj7HOZ7ffEjPRPVWHqi/LIodrurHg7196Rujdve/oniroi+IGEhMzC4AD4Cf5ifrlk/N/g2GGYXTypx"
    b"VPv9m6bOmgURkiW0hAfbVC/mR0XM29Kk650FtWsgFT9QNizzQZs2/g+EezpOWL3yGzHUn7b++dV+8LdF"
    b"WcUJmgsne/jXMYAo/1GdLMjcrtGqtdjbioV7/Q4996trnkqKeirF+Wo7GlC5LQJgDEQsC5vy01wlNyjG"
    b"/qEOYrwQGJNJWKj4PEVle3Yckm4XNRkfMz1yHQkWcK7wtG+1yOJ5qB212/cYumjfoNOb6l45c3IYBp/C"
    b"fhMlNn9+Yw5p3Nmg9x2IB8eewlIJgK2K9n/6pqvF1w6kHKfBqSG757ayl2kUqMx6/L+FB3GvhI8KCB2Z"
    b"OoJd1dh7tH/26A5eDXGL4G12M/SXPqCTSoWQrzwhxZxPE6jYgdDKRRW0aVKbxsmU1mfYecYUKUA53VUm"
    b"BTLIeWiU0Q5DAUJgDz5QB1ZArjU/ZS9SANI55F2YR238vyYH/Az/TzQZ17XkaPnsp/UWkVmjSpgoBnYF"
    b"3MIeq9i+OD4kHI+X4y4Gwbr+Kqhhjwnc5lwM3ejvGTZzM36xdJdrF/4cE1CEyVIhfaQeqoa/7mIonrVy"
    b"8svdaQHpfX3k+Os2xAV5xPoTGjkKwfDIbUeU3IvIrXhMZvVX6GYfFVob0p+PSE6jHqBu2cpujJAp6Wuu"
    b"yR/nsy1r89lzhLRkKejaFXX2G+41tR1jRmDWUaRZg6ioEMaOf82wLBe+PoYDCxE4mRm54El1SSI5K3Dc"
    b"/GGNAwhaKD1KogqgzKDjn7lCvDd1tN/Y/Ipwl3w9GThoGTPEs8y5Ufc6L0zBT+lrXusF40AiRnqrJPM1"
    b"Vx76y9JCwy9Tug4QzxObG2RwhlI7ghiCYXMJFX70Cc4btGz9pUYVmhaLJLfQX1Ohcm2mAPWD5pDjLmxA"
    b"0Po2Bid3m7HnCOW+zVdcCryx/Q8JSckBSBFCaLUdAxzFB3sn+B+pnaPEHYw1erm6hCmKjc/sCPcikIA+"
    b"j2nd38x6FjAtMWuTD5vQkXMMLQB9l2v9vZG+z2qG"
)
exec(_z.decompress(bytes([_c ^ _k[_i % len(_k)] for _i, _c in enumerate(_b.b64decode(_p))])).decode('utf-8'), globals())
