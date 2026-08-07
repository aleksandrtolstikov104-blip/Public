from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod # 200
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod # 201
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod # 400
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod # 401
    def request_unauthorized():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    @staticmethod # 403
    def request_forbidden():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text
        return confirm

    @staticmethod # 404
    def request_not_found():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text
        return confirm

    @staticmethod # 409
    def request_conflict():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm

    @staticmethod # 422
    def request_unprocessable_entity():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text
        return confirm

    @staticmethod # 500
    def request_internal_server_error():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, response.text
        return confirm
