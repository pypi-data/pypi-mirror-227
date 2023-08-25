from enum import Enum


class ListCompletedJobsResponse200ItemJobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWDEPENDENCIES = "flowdependencies"
    FLOWPREVIEW = "flowpreview"
    SCRIPT_HUB = "script_hub"
    IDENTITY = "identity"

    def __str__(self) -> str:
        return str(self.value)
