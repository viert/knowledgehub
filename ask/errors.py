from uengine.errors import ApiError, IntegrityError


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
