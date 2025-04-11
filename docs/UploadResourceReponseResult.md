# UploadResourceReponseResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_key** | **str** |  | 
**resource_cid** | **str** |  | 
**resource_size** | **int** |  | 
**injection_uploaded** | **str** |  | 
**stream_length** | **int** |  | 

## Example

```python
from line_works.openapi.storage.models.upload_resource_reponse_result import UploadResourceReponseResult

# TODO update the JSON string below
json = "{}"
# create an instance of UploadResourceReponseResult from a JSON string
upload_resource_reponse_result_instance = UploadResourceReponseResult.from_json(json)
# print the JSON string representation of the object
print(UploadResourceReponseResult.to_json())

# convert the object into a dict
upload_resource_reponse_result_dict = upload_resource_reponse_result_instance.to_dict()
# create an instance of UploadResourceReponseResult from a dict
upload_resource_reponse_result_from_dict = UploadResourceReponseResult.from_dict(upload_resource_reponse_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


