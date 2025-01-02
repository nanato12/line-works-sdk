# line-works-sdk

LINE Works SDK for Python

## Requirements

Python 3.11+

## Installation

```sh
$ pip install line-works-sdk
```

dev version

<https://pypi.org/project/line-works-sdk/#history>

```sh
$ pip install line-works-sdk==x.x.devyyyymmddHHMM
```

## Usage

```python
from line_works import LineWorks


WORKS_ID = "YOUR WORKS ID"
PASSWORD = "YOUR WORKS PASSWORD"

works = LineWorks(works_id=WORKS_ID, password=PASSWORD)
# [INFO] line_works/client:66 login success: LineWorks(works_id='xxxxx', tenant_id=xxxxxxxx, domain_id=xxxxxxxx, contact_no=xxxxxxxxxxxxx)

my_info = works.get_my_info()
print(f"{my_info=}")

# trace websocket
asyncio.run(works.trace())
```

## Contributors

- [nezumi0627](https://github.com/nezumi0627)

## GitHub Actions

The following linter results are detected by GitHub Actions.

- ruff
- mypy
