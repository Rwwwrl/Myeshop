from typing import Annotated

from mock import Mock

FileStorageApiMockType = Annotated[Mock, 'Mock(spec=IFileStorageApi)']
