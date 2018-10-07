
"""
Convenience module for access of custom bookmarks application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# The maximum length of title 
MAX_BOOKMARK_TITLE_LENGTH = getattr(settings, 'MAX_BOOKMARK_TITLE_LENGTH', 255)

# The maximum description of title 
MAX_BOOKMARK_DESCRIPTION_LENGTH = getattr(settings, 'MAX_BOOKMARK_DESCRIPTION_LENGTH', 2047)

# The maximum length of url 
MAX_BOOKMARK_URL_LENGTH = getattr(settings, 'MAX_BOOKMARK_URL_LENGTH', 2047)

