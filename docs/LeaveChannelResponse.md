# LeaveChannelResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | 

## Example

```python
from line_works.openapi.talk.models.leave_channel_response import LeaveChannelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LeaveChannelResponse from a JSON string
leave_channel_response_instance = LeaveChannelResponse.from_json(json)
# print the JSON string representation of the object
print(LeaveChannelResponse.to_json())

# convert the object into a dict
leave_channel_response_dict = leave_channel_response_instance.to_dict()
# create an instance of LeaveChannelResponse from a dict
leave_channel_response_from_dict = LeaveChannelResponse.from_dict(leave_channel_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


