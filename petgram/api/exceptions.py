from fastapi import HTTPException


ERROR_IDS = {
    401: "invalid_credentials",
    400: "bad_request",
    404: "not_found",
    409: "conflict",
    303: "database_error",
    422: "unprocessable_entity"    
}


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid username or password")


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found.")


class SignupFailedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Failed to sign up.")


class UsernameTakenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="Username already taken.")


class DatabaseAccessException(HTTPException):
    def __init__(self):
        super().__init__(status_code=303, detail="Failed to access database.")


class PasswordMismatchError(HTTPException):
    def __init__(self):
        super().__init__(status_code=422, detail="Passwords do not match.")