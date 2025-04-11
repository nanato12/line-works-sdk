# UploadResouceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | 
**result** | [**UploadResourceReponseResult**](UploadResourceReponseResult.md) |  | 

## Example

```python
from line_works.openapi.storage.models.upload_resouce_response import UploadResouceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UploadResouceResponse from a JSON string
upload_resouce_response_instance = UploadResouceResponse.from_json(json)
# print the JSON string representation of the object
print(UploadResouceResponse.to_json())

# convert the object into a dict
upload_resouce_response_dict = upload_resouce_response_instance.to_dict()
# create an instance of UploadResouceResponse from a dict
upload_resouce_response_from_dict = UploadResouceResponse.from_dict(upload_resouce_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


