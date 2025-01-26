# GetChannelMembersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **int** |  | 
**message** | **str** |  | 
**members** | [**List[Member]**](Member.md) |  | 

## Example

```python
from line_works.openapi.talk.models.get_channel_members_response import GetChannelMembersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetChannelMembersResponse from a JSON string
get_channel_members_response_instance = GetChannelMembersResponse.from_json(json)
# print the JSON string representation of the object
print(GetChannelMembersResponse.to_json())

# convert the object into a dict
get_channel_members_response_dict = get_channel_members_response_instance.to_dict()
# create an instance of GetChannelMembersResponse from a dict
get_channel_members_response_from_dict = GetChannelMembersResponse.from_dict(get_channel_members_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


