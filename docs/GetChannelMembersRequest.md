# GetChannelMembersRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**channel_no** | **int** |  | 
**member_update_time** | **int** |  | [optional] [default to 0]
**paging_count** | **int** |  | [optional] [default to 500]

## Example

```python
from line_works.openapi.talk.models.get_channel_members_request import GetChannelMembersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetChannelMembersRequest from a JSON string
get_channel_members_request_instance = GetChannelMembersRequest.from_json(json)
# print the JSON string representation of the object
print(GetChannelMembersRequest.to_json())

# convert the object into a dict
get_channel_members_request_dict = get_channel_members_request_instance.to_dict()
# create an instance of GetChannelMembersRequest from a dict
get_channel_members_request_from_dict = GetChannelMembersRequest.from_dict(get_channel_members_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


