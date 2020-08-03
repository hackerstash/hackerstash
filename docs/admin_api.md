# Admin API

The admin api is prefixed with `/api/admin/` and requires an API key.

### Example:

Curl:
```shell script
$ curl --location --request DELETE 'http://localhost:5000/api/admin/users/1' --header 'x-api-key: teapot'
```
