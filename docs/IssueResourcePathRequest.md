# IssueResourcePathRequest


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
from line_works.openapi.talk.models.issue_resource_path_request import IssueResourcePathRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueResourcePathRequest from a JSON string
issue_resource_path_request_instance = IssueResourcePathRequest.from_json(json)
# print the JSON string representation of the object
print(IssueResourcePathRequest.to_json())

# convert the object into a dict
issue_resource_path_request_dict = issue_resource_path_request_instance.to_dict()
# create an instance of IssueResourcePathRequest from a dict
issue_resource_path_request_from_dict = IssueResourcePathRequest.from_dict(issue_resource_path_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


