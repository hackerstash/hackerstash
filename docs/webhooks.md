# Admin Webhooks

Some admin actions can be triggered via the webhook at `/api/admin/webhook`.

### Webhook Types:
At the time of writing, the supported types are:
- `delete_user`
- `end_contest`
- `goal_setting`
- `peer_review`
- `prepare_feedback`
- `progress_update`
- `project_vote_reminder`

A complete list of webhooks can be found [here](https://github.com/hackerstash/hackerstash/blob/master/hackerstash/lib/webhooks/factory.py):

### Example:

Python example:
```python
import requests

headers = {
    'x-api-key': '<admin_api_key>'
}

json = {
    'type': '<webook_event_type>',
    'data': {}
}

r = requests.post('https://hackerstash.com/api/admin/webhook', headers=headers, json=json)
```

Successful requests will return a `202: Accepted` response 