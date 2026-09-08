class CategoryDeletionError(Exception):
    """Raised when a category cannot be deleted."""


class CategoryVersionConflictError(Exception):
    """Raised when a category was modified concurrently."""