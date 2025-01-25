# Sticker

sticker model

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pkg_ver** | **str** |  | 
**pkg_id** | **str** |  | 
**stk_type** | **str** |  | 
**stk_id** | **str** |  | 
**stk_opt** | **str** |  | 

## Example

```python
from line_works.openapi.talk.models.sticker import Sticker

# TODO update the JSON string below
json = "{}"
# create an instance of Sticker from a JSON string
sticker_instance = Sticker.from_json(json)
# print the JSON string representation of the object
print(Sticker.to_json())

# convert the object into a dict
sticker_dict = sticker_instance.to_dict()
# create an instance of Sticker from a dict
sticker_from_dict = Sticker.from_dict(sticker_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


