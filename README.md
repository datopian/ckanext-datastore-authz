# ckanext-datastore-authz

CKAN extension that exposes an authorization endpoint for the external
[datastore service](https://github.com/datopian/datastore).

The datastore service is a standalone API that serves and writes tabular
data, decoupled from CKAN. It delegates permission checks back to CKAN by
calling the `datastore_authorize` action provided by this extension, so
that access to a resource's data continues to honour CKAN's auth rules
(public/private packages, organization roles, collaborators, etc.).

## How it works

This extension registers a single action:

**`datastore_authorize`** — checks whether the current user is allowed to
perform a given operation on a resource (or package) and returns the
resolved `package` and `resource` metadata.

Request:

| Field         | Description                                                              |
| ------------- | ------------------------------------------------------------------------ |
| `permission`  | One of `read`, `create`, `update`, `delete`, `patch` (default: `read`).  |
| `resource_id` | Resource id. Required unless creating against a package.                 |
| `package_id`  | Package id. Used with `permission=create` when no resource exists yet.   |

Response:

```json
{
  "package":  { "...": "..." },
  "resource": { "...": "..." }
}
```

The action raises `NotAuthorized` if the user lacks permission, mapping
each `permission` to the corresponding CKAN auth function
(`resource_show`, `resource_create`, `resource_update`, etc.).

## Installation

1. Activate your CKAN virtualenv.
2. Install the extension:

   ```
   git clone https://github.com/sagargg/ckanext-datastore-authz.git
   cd ckanext-datastore-authz
   pip install -e .
   ```

3. Add `datastore_authz` to `ckan.plugins` in your CKAN config.
4. Restart CKAN.

## Tests

```
pytest --ckan-ini=test.ini
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
