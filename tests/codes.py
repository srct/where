class Code():
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
    
    def __str__(self):
        return str(self.code) + " " + self.msg

# success
SUCCESS = Code(200, "OK")
CREATED = Code(201, "Created")

# redirection
MOVED = Code(301, "Moved Permanently")
REDIRECT = Code(308, "Permanent Redirect")

# client errors
BAD_REQUEST = Code(400, "Bad Request")
UNAUTHORIZED = Code(401, "Unauthorized")
FORBIDDEN = Code(403, "Forbidden")
NOT_FOUND = Code(404, "Not Found")
INVALID_METHOD = Code(405, "Method Not Allowed")

# server errors
SERVER_ERR = Code(500, "Internal Server Error")

codes = {
    200: SUCCESS,
    201: CREATED,
    301: MOVED, 
    308: REDIRECT,
    400: BAD_REQUEST,
    401: UNAUTHORIZED,
    403: FORBIDDEN,
    404: NOT_FOUND,
    405: INVALID_METHOD,
    500: SERVER_ERR
}
