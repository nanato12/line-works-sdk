# UploadResourceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **str** |  | [optional] [default to 'works']
**channel_no** | **int** |  | 
**filename** | **str** |  | 
**filesize** | **int** |  | 
**msg_type** | **int** |  | 
**channel_type** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.upload_resource_request import UploadResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UploadResourceRequest from a JSON string
upload_resource_request_instance = UploadResourceRequest.from_json(json)
# print the JSON string representation of the object
print(UploadResourceRequest.to_json())

# convert the object into a dict
upload_resource_request_dict = upload_resource_request_instance.to_dict()
# create an instance of UploadResourceRequest from a dict
upload_resource_request_from_dict = UploadResourceRequest.from_dict(upload_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


