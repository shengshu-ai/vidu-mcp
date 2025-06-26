class ViduAPIError(Exception):
    """Base exception for Vidu API errors."""
    pass

class ViduAuthError(ViduAPIError):
    """Authentication related errors."""
    pass
class ViduRequestError(ViduAPIError):
    """Request related errors."""
    pass