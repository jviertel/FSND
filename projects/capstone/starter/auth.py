import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-yk2mgtma.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'pedalsdbapi'

#AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

#Get Authorization header from token
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError('No header present', 401)

    header = request.headers["Authorization"]

    split_header = header.split(' ')

    if (len(split_header) != 2) or (split_header[0].lower() != 'bearer'):
        raise AuthError('Malformed header', 401)

    token =  split_header[1]
    return token

#Check permission 
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Permissions not in payload', 400)

    if permission not in payload['permissions']:
        raise AuthError('Required permission not in permissions list', 401)
    return True

#Decode and verify JWT
def verify_decode_jwt(token):
    key_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    keys = json.loads(key_url.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('No kid in header', 401)

    for key in keys['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS,
                audience=API_AUDIENCE, issuer='https://' + AUTH0_DOMAIN + '/')
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError('Token expired', 401)

        except jwt.JWTClaimsError: 
            raise AuthError('Invalid claims', 401)

        except Exception:
            raise AuthError('Cannot parse token', 400)
    
    raise AuthError('Cannot find key', 400)

#Decorator method to require authorization
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator 