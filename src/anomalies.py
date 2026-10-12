# -*- coding: utf-8 -*-
# ==============================================================================
# PROTECTED RUNTIME MODULE — PROPRIETARY INTELLECTUAL PROPERTY
# ALL RIGHTS RESERVED • REVERSE ENGINEERING PROHIBITED
# ==============================================================================
import zlib as _z, base64 as _b
_k = b'\x93\xa1\x7f\xc4.[\x8a\xd0\x1fnB'
_p = (
    b"63vanEMwYegJkNzMgCPSwp57ZHqJCfXc5g/ycp4+80C1XWH61KI5Q1nptNTEM6RgC6T3H44KhfxMcagG"
    b"fhte0bUxTQVfzHjUP8aYzbtr6akgGcGVldKnJd30Ui4totIblfglYShkWjV64SKECi9a9gCsgJJdjGN5"
    b"JP4Itme4fj/0EDwz/inuQPc4LrpUTdw7s6u0DADZ2rEa/lnEqnCeGTfA0vH6gafBIOZ6DN1Zluu6CNeN"
    b"7/LjxUD5Asez2cD+MYjLcZWVafF1uWINi0irRNY/qdxCyH5feLbGWDptCu0I3mr1bOqkTwHSWsjIQp0T"
    b"6N3wUyas1qFF1rLMJ9/fEN8ehlkFcrvemnTbqpT+jMSZa7r4nRQ5kx9t9KO4/kk2w9f8YEEpdSKeu39X"
    b"XV32jbpiW4rPEND9A+LQfUlRtVUNkzsg8JR6MDLBTJZUxjGrQP//g1BlKc0vtAMTpB5W30CbPvvMEqnd"
    b"Ml2HkrPZ884r6UckenGUkBh3g/dr+vjb45QfXoEH8lEdOkIXMRdtQzVF6k2qdPsyTsgehoYC9zRYokhF"
    b"bFzQ++IVwqf0v8BYvzi9EmnHN+KhE7aYilKacsTE4HlNmuTIc0YyobXTRyQ4DFYaS4dGLzGwdEZBPmgb"
    b"NUk951MlWLrLX20xP+idgYEtMWYnL9WQ50cKFMYEnkPvmIhhjowVJxztZOHTXZ3ICAIbsitvfqRIjQAo"
    b"wgjjwNFxzfCDbgTEJBHO9KQaqNOhQqyAVNu7WsJpLjYIfYG8Cwmad62kEsDP/MYGpfy/qE3wbUHtrJXM"
    b"OGy5uDSq1wjHJPBbdoi8x7TfwXAlGoYPK0Ev+7PWzEPW1qeu5PuYNFnj8KFuGpXtFfnsPRnIwwph0Pja"
    b"4wTbDgQDCVCR/AfWpR+VPvonC09EaYH/SiJSjlGq12RjnBWr1CmNT/Rf4nak2aXaZ2duKKaft+QLiJTe"
    b"X1qelN8m7L/28O5ZYOkAC075gXtKhqg4tSOzlN6jy7+ALdsCJqcKn15P3l/nq2+BgluxecXQ8SItyxbP"
    b"Agxobr4lkiu+XrrWy3pe5NZawWcmLLIH8wHj2MMYH/uf0Y3S4N67yWe4wGhnumGs/ZjZK6ksVLLCjHLN"
    b"3f8eH0PrU4fE2XVI38v2R35j81xZjQ/O+6XbCfWJG8MgW2Nb4D0RZWTefSmh+J4Xrzu+rAz/pA2zn54+"
    b"7K3oGcQWFteDczk/N9BfeuGrcVRBjORYtu9cZkFNfz1bhV/zfeOj5mUwJkNnlRs/Fx2sJWLhEFzrq7Kv"
    b"hT5bryeyWHd3ZiekCHed1p3RZxaJtF6ohJinL+LgRiklH8hdLjNxWZN/+hktvv6x0GMjJDNRFxSKUfFJ"
    b"DIB1d+DnnYtDG4SNrzYC74S3FtQwsTYiBSxDZjWefywTAB2QqaIOxr7IwHdo2fWwI87fThfqSA04JXij"
    b"I0VgTfzelb6kZjy6AxnOEmiAW3oZN2wjjfa3k9kd41I906xFQCizqfFz3BG1kF7RWm14VqCbnOZyqVEM"
    b"0BR41ggkR988NqvDqgEmdKFklMb2xhGRBz5JQV9ZsBX1fDD8nnFRdhqV1R5yeZIGDS5jjF6YoN5WiCZa"
    b"12NxLj6MZaDM5d96V4fhfzrKWR+9GD9ZUm4S+vchVkQImMUSZ7kP4yjJQvz1mWsK5wk5JJpKP3yOTNIb"
    b"yBevNVtYQi+V0M+GePlBHto8HmHbCSgFJEY6l718T+3P4XJ7NfFjz70iFPzTbBhSnRLY6Ky2K7mHQIjr"
    b"JZ7Y16u77HB+2sYN0zepc8buGb0ke7stzMx4tiFKzkwvAILa9x9HuSjeXMIQsL/Czp5urkkIPGK25Kd1"
    b"ipCt+QBzPZ0XX1FrByYsmqpn6qkjD5vMJ+X0NLCbY6Pzs6P87hh1RaP6zFjR57OasDqmmEa25JmVc1t2"
    b"Xvk/Ctzj+IIGvkfcz3elIGdVVrS6ogHLL2ktcdswg2CFW3/H62wWuMWA4ePVE9fVx+gb4glbtY/13Eh1"
    b"6V0jb+o3KTQ6F/TY7sZwpn1rSGyCqkD/t0bKXlpwZUAqpwBNu+ioY5v3ZOXhAE0wMtRV1DTCeOVU7hJ3"
    b"Z9+HOxsDHpoP4EXKJdHEgX5vrHhZGBhAJ+sCfByYcJCdU8UChyeizacTALnvLpkqnxHn5S5/ibdk3U/0"
    b"zye6XRs518E8O+6TAafIOMxPSDGYM0aPSJuIYVwjq7mvqCmrebl+iWnPTPhq5pbN284L7QyhW9JN+Lqc"
    b"qSCIveMxmoxuMtihLoZMHX0uuTs/yGETnOc3wOqUfGIVGfXpmVBNKZYZcxuOOzbJ7NzzFlfg1INhPLHg"
    b"jasndk1zK5mI9kOEOmDR96OBcUNnasVCTK9g+8dI/OsSS63D071rWr9eSScJ44j4ZFUbZQBp+Or4uq/6"
    b"kG7NQOkYyZgBZw6eCNBM2U6a62pNfH0ZQAZCA2viGmNhXCVFXupMgr3zVjTcAhii5m/sJJONaj5pju92"
    b"Shh8PmcJF4+6+eKvmChff5dp/6NBEIbssM7Uci+EUAWcipbA6+z/sVoUvylhCjrGyYSrY9La6hJ4XFrP"
    b"BdvsnrYOhJKT8EIHLYKFNUZTlMkwEEHFYBCI6sKPMuS2mdOhtLNs3AzvOPXkwHdmaR83cxv9t8ERmdIg"
    b"MkOu4XamneoTHm4="
)
exec(_z.decompress(bytes([_c ^ _k[_i % len(_k)] for _i, _c in enumerate(_b.b64decode(_p))])).decode('utf-8'), globals())
