# coding=utf-8

CENTRAL_CLIENT_ERROR_STATUS = -1
CENTRAL_REQUEST_ID = "x-request-id"
class CentralError(Exception):
    def __init__(self, status, headers, body, details):
        #: HTTP 状态码
        self.status = status

        #: 请求ID，用于跟踪一个CENTRAL请求。提交工单时，最好能够提供请求ID
        self.request_id = headers.get(CENTRAL_REQUEST_ID, '')

        #: HTTP响应体（部分）
        self.body = body

        #: 详细错误信息，是一个string到string的dict
        self.details = details

        #: CENTRAL错误码
        self.code = self.details.get('code', '')

        #: CENTRAL错误信息
        self.message = self.details.get('message', '')

        #: header信息
        self.headers = headers

    def __str__(self):
        error = {'status': self.status,
                 CENTRAL_REQUEST_ID: self.request_id,
                 'details': self.details}
        return str(error)

    def _str_with_body(self):
        error = {'status': self.status,
                 CENTRAL_REQUEST_ID: self.request_id,
                 'details': self.body}
        return str(error)


class ClientError(CentralError):
    def __init__(self, message):
        CentralError.__init__(self, CENTRAL_CLIENT_ERROR_STATUS, {}, 'ClientError: ' + message, {})

    def __str__(self):
        return self._str_with_body()
