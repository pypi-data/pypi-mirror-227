# Dashlog

Official wrapper over the [dashlog.app](https://dashlog.app) api


```bash
pip install dashlog
```

```python
from dashlog import Dashlog

dash = Dashlog('<Your-API-Key-here>')

response = dash.log(
    project='MyProject',  # string - required
    channel='Users',      # string - required

    title='New User',                           # string - required
    description='John Doe created an account',  # string - optionnal

    data={                            # dict - optionnal
        'username': '@johndoe',          # Values can be
        'email': 'john.doe@dashlog.app'  # strings,
        'age': 32,                       # numbers,
        'premium': True                  # or booleans
    }

    notify=True,  # boolean - optionnal - send log by email if True
)

print(response.status)  # 200
print(response.json())  # {'status': 200, 'message': 'log added successfully'}
```