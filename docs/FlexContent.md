# FlexContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] [default to 'flex']
**alt_text** | **str** |  | 
**contents** | **object** |  | 

## Example

```python
from line_works.openapi.talk.models.flex_content import FlexContent

# TODO update the JSON string below
json = "{}"
# create an instance of FlexContent from a JSON string
flex_content_instance = FlexContent.from_json(json)
# print the JSON string representation of the object
print(FlexContent.to_json())

# convert the object into a dict
flex_content_dict = flex_content_instance.to_dict()
# create an instance of FlexContent from a dict
flex_content_from_dict = FlexContent.from_dict(flex_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


