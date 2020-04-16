"""
Module to define the program exceptions.

Class Hierarchy:
Exception
 +-- AirssDLException
      +-- ExtractionError
           +-- AuthenticationError
           +-- AuthorizationError
           +-- NotFoundError
           +-- HttpError
"""


class AirssDLException(Exception):
    """Base class for AirssDL exceptions"""


class ExtractionError(AirssDLException):
    """Base class for exceptions during information extraction"""


class AuthenticationError(ExtractionError):
    """Invalid or missing login information"""


class AuthorizationError(ExtractionError):
    """Insufficient privileges to access a resource"""


class NotFoundError(ExtractionError):
    """Requested resource (gallery/image) does not exist"""


class HttpError(ExtractionError):
    """HTTP request during extraction failed"""
