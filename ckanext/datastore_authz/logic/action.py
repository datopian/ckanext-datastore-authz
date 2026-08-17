import ckan.plugins.toolkit as tk

PERMISSION_AUTH = {
    "read": "resource_show",
    "create": "resource_create",
    "update": "resource_update",
    "delete": "resource_delete",
    "patch": "resource_patch",
}


def datastore_authorize(context, data_dict):
    """Authorize a datastore operation and return package + resource info.

    Input:
        permission:  one of {read, create, update, delete, patch} (default: read)
        resource_id: '<id>' (required unless permission='create' with package_id)
        package_id:  '<id>' (used for permission='create')
    Output: {'package': {...}, 'resource': {...}}
    """
    permission = data_dict.get("permission") or "read"
    if permission not in PERMISSION_AUTH:
        raise tk.ValidationError(
            "permission must be one of: %s" % ", ".join(PERMISSION_AUTH)
        )
    auth_name = PERMISSION_AUTH[permission]

    resource_id = data_dict.get("resource_id")
    package_id = data_dict.get("package_id")
    if not (resource_id or package_id):
        raise tk.ValidationError("resource_id or package_id is required")

    if package_id and not resource_id:
        tk.check_access(auth_name, context, {"package_id": package_id})
        package = tk.get_action("package_show")(context, {"id": package_id})
        package.pop("resources", None)
        return {"package": package, "resource": {}}

    tk.check_access(auth_name, context, {"id": resource_id})
    resource = tk.get_action("resource_show")(context, {"id": resource_id})
    package = tk.get_action("package_show")(context, {"id": resource["package_id"]})
    package.pop("resources", None)
    return {
        "package": package,
        "resource": resource,
        "user": context.get("user"),
    }
