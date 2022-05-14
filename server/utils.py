from flask import Response


def create_error(error_msg: str, status_code=400):
    return Response(error_msg, status=status_code)
