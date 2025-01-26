# LeaveChannelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel_no** | **int** |  | [optional] [default to 0]
**channel_no_list** | **List[int]** |  | 

## Example

```python
from line_works.openapi.talk.models.leave_channel_request import LeaveChannelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LeaveChannelRequest from a JSON string
leave_channel_request_instance = LeaveChannelRequest.from_json(json)
# print the JSON string representation of the object
print(LeaveChannelRequest.to_json())

# convert the object into a dict
leave_channel_request_dict = leave_channel_request_instance.to_dict()
# create an instance of LeaveChannelRequest from a dict
leave_channel_request_from_dict = LeaveChannelRequest.from_dict(leave_channel_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


