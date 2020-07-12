from glasskit.errors import ApiError, IntegrityError


class AuthenticationError(ApiError):

    status_code = 401
    error_key = "auth_error"
    auth_url = None
    
    def __init__(self, message="you must be authenticated first", payload=None):
        super(AuthenticationError, self).__init__(message, payload=payload)

    def to_dict(self):
        from ask.idconnect.provider import BaseProvider
        data = super().to_dict()
        data["providers"] = BaseProvider.list_provider_info()
        if "state" not in data:
            data["state"] = "logged out"
        return data


class InvalidParent(ApiError):
    pass


class InvalidUser(ApiError):
    pass


class HasReferences(IntegrityError):
    pass


class InvalidTags(ApiError):
    pass


class InvalidVote(ApiError):
    pass


class InvalidPost(ApiError):
    pass


class InvalidQuestion(InvalidPost):
    pass


class ConfigurationError(ApiError):
    status_code = 500


class OAuthError(AuthenticationError):
    pass


class AlreadySubscribed(IntegrityError):
    pass


class NotSubscribed(IntegrityError):
    pass
