# IssueResourcePathResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | 
**var_resource_path** | **str** |  | 
**file_uuid** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.issue_resource_path_response import IssueResourcePathResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IssueResourcePathResponse from a JSON string
issue_resource_path_response_instance = IssueResourcePathResponse.from_json(json)
# print the JSON string representation of the object
print(IssueResourcePathResponse.to_json())

# convert the object into a dict
issue_resource_path_response_dict = issue_resource_path_response_instance.to_dict()
# create an instance of IssueResourcePathResponse from a dict
issue_resource_path_response_from_dict = IssueResourcePathResponse.from_dict(issue_resource_path_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


