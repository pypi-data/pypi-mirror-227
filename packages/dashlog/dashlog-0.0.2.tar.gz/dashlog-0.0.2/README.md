# Dashlog

Official wrapper over the [dashlog.app](https://dashlog.app) api


```bash
pip install dashlog
```

```python
from dashlog import Dashlog

dash = Dashlog('<YOUR-API-KEY>')

response = dash.log(
    project='MyProject',  # string - required
    channel='Users',      # string - required

    title='New User',                           # string - required
    description='John Doe created an account',  # string - optionnal

    data={                              # dict[str, str | int | float | boolean] - optionnal
        'email': 'john.doe@dashlog.app'  # Values can be
        'username': '@johndoe',          # strings,
        'age': 29,                       # numbers,
        'premium': True                  # or booleans
    }

    notify=True,  # boolean - optionnal - send log by email if True
)

print(response.status)  # 200
print(response.json())  # {'status': 200, 'message': 'log added successfully'}

```