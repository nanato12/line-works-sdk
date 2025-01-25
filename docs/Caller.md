# Caller


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**domain_id** | **int** |  | 
**user_no** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.caller import Caller

# TODO update the JSON string below
json = "{}"
# create an instance of Caller from a JSON string
caller_instance = Caller.from_json(json)
# print the JSON string representation of the object
print(Caller.to_json())

# convert the object into a dict
caller_dict = caller_instance.to_dict()
# create an instance of Caller from a dict
caller_from_dict = Caller.from_dict(caller_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


