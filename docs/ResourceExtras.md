# ResourceExtras


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filesize** | **int** |  | 
**filename** | **str** |  | 
**resourcepath** | **str** |  | [optional] [default to '']
**width** | **int** |  | [optional] 
**height** | **int** |  | [optional] 

## Example

```python
from line_works.openapi.storage.models.resource_extras import ResourceExtras

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceExtras from a JSON string
resource_extras_instance = ResourceExtras.from_json(json)
# print the JSON string representation of the object
print(ResourceExtras.to_json())

# convert the object into a dict
resource_extras_dict = resource_extras_instance.to_dict()
# create an instance of ResourceExtras from a dict
resource_extras_from_dict = ResourceExtras.from_dict(resource_extras_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


