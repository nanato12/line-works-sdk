# UploadResourceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | 
**var_resource_path** | **str** |  | 
**file_uuid** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.upload_resource_response import UploadResourceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UploadResourceResponse from a JSON string
upload_resource_response_instance = UploadResourceResponse.from_json(json)
# print the JSON string representation of the object
print(UploadResourceResponse.to_json())

# convert the object into a dict
upload_resource_response_dict = upload_resource_response_instance.to_dict()
# create an instance of UploadResourceResponse from a dict
upload_resource_response_from_dict = UploadResourceResponse.from_dict(upload_resource_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


