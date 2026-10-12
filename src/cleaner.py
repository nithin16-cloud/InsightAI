# -*- coding: utf-8 -*-
# ==============================================================================
# PROTECTED RUNTIME MODULE — PROPRIETARY INTELLECTUAL PROPERTY
# ALL RIGHTS RESERVED • REVERSE ENGINEERING PROHIBITED
# ==============================================================================
import zlib as _z, base64 as _b
_k = b'\x93\xa1\x7f\xc4.[\x8a\xd0\x1fnB'
_p = (
    b"63vCnPU1aeYPE5XEsZWHAo/cI3Ouyb7XzgQstjwYuSHDspGtDAh5G9JWSzctH7xPAI9P3SkrwbMztyXi"
    b"whMTBlwzj+YgfUz8OS7qRZsCbiuX3PKIGl78ndZwKdTTck/jNC5TvVlxW3TtM7bQLkiw3cFYNiuqfXl7"
    b"kZ91QR6/FCi6dCCM06qrB6v34xVBxyQRQpOzdFkjSU3i3VuS0p4OPEBb1RKgABHFrVt8dmlyRNTArDtO"
    b"OQnKMaCzrm4EfgZWUpioERh3cZL1NnjBOxswY4qPGdnjDuL73DjNWk4vNe1EsMmOTsuSrBVUYDDdFlSh"
    b"WgQMPsOD3euvby7L9XcuuQSODm73BNoNhmCgYsad8osoeXFXOldOEFVAPUB5KUfeeIJURJssXhqdSBvZ"
    b"Nmwfw9QlDp/WDF+Pon6edHfD0dU6fRkVzZAXk2RjSihedmLG49NkabkS0HtJUdXcVtyl93qPr2QcUj+o"
    b"mQwttWj+GPQiFRDTCEkZjWjp+frCvnbOcDbsH6DvBQfCDNVFX3NuIZBShI6LUcGn208aZnnYYEMZQAKu"
    b"6aWJfG3ANkqR5ecyiTGAAJoIdtKljwkBaT4SRcjOjTHRAYZnHYrjGFShJ6fK7eRmbOIq6P3bvTYMwNgF"
    b"BmcWeavUCwwS4eVO5Y4hchb75nRj5pRulMbVkPIAtLfZuK772wCbn6+00GxiVpQLAJ6rbl6pawiQTAPb"
    b"LyYs+f202xxAWfySGlnqvgKrjEnrSpiy4md+vsXSD1EA2TQmAkUHPHlN64yoyztqtaa1F+RDwQlf6Rk1"
    b"bZKdZGbMb9PGestP1uzuaNeaPPhSV8KA2GzWvetWqTS7T7ZH945RffrOIy9BqgZn+AbiK3Otn5+OCjx2"
    b"ShHuGmB8OdscTLvrY6DQmR67fpakFK6ucIUPH7Gy6M1rs9+IShgvSuHZ3y7wBA82KQmLl4OnSJQGYeF9"
    b"DfwGEX2HqA6n7WWNaToKMkk4ikZdgRsRwcte/kjA0HAbExyzOqwYmQa0Gl5FuxZHIlt26WMgwtZxaMb0"
    b"dWTdeu3iiDKtzAVxPT7PAMj9Sh4r5EDxBnEb4rkc726fgNCcEItTpOSaQhuzTSZykL8cJvAafxrDu7ed"
    b"55v8khRDr6Z9pqRNrrMreeYQLkjv8ZD3Gcw1sn4Y2dGSifunCJF+1Lvwgr+/sdHcKFWPCdCdy9YixsnJ"
    b"IGYzy5SJlrzT6UTkQoXr9SS0qpxy9gSOm8wnrnVKEBkllFb1xWxkZr3ggd76LZXhuHHXWWF7gqJyCJJA"
    b"GfqfTbkNwqr/yLZuJNi++EA4ULVKmAcKJznlT8O562S8kdGFYQ3gjdm6p1R6k1JtPeRvADbB7rRlfkP1"
    b"2/rhBiWfEFwZ+rI6Twwv+uZ2ZL+FZ1glOzImDmw1Jju4VpLVuN6OSym1NR3yBOrvPAGLpCDtrxOBOMRl"
    b"0XQnDa0HBcp5d1mkBXWhaaCwrJlTAs8B2AU885anU8pUHZsGPfNArFn7LZbQjVslae5Eg4tEehu8X8GW"
    b"RkWwobasFPTDhz9nDDAXHpSdaiT2Tt4IBEhd557x5K6zKyWAw7zjQemYG4a5YBmofOV+yWI0h7aLQPig"
    b"3PrzpNbfuiQNcAMi6jdCH5l6BT6ZIhuuGQfm+A2uZQHIwhHotcKy6ilbfZKOJ1xePVMYKwYhuMp4BofJ"
    b"UxSroF0FKUabmA/I3mKTSlcyjmKYpJvoU3ZVUaxWsyZkPWO049FhX9rPbKjhLH7y7H5T/q9yMoSR+61H"
    b"2JaDh+nh4lje0uwqBcVUaqSKOD/OZw=="
)
exec(_z.decompress(bytes([_c ^ _k[_i % len(_k)] for _i, _c in enumerate(_b.b64decode(_p))])).decode('utf-8'), globals())
