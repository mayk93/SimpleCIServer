KEY = 0
VALUE = 1


def get_other_data(repo_data):
    if repo_data is None:
        return {
            "updated_at": "unknown",
            "size": "unknown"
        }
    return {
        "updated_at": repo_data.get("updated_at", "unknown"),
        "size": repo_data.get("size", "unknown")
    }