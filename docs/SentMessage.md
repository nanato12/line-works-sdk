# SentMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message_id** | **int** |  | 
**channel_no** | **int** |  | 
**writer_id** | **str** |  | 
**user_no** | **int** |  | 
**bot_no** | **int** |  | 
**message_no** | **int** |  | 
**content** | **str** |  | 
**member_count** | **int** |  | 
**message_type_code** | **int** |  | 
**message_status_type** | **str** |  | 
**message_status_type_code** | **int** |  | 
**extras** | **str** |  | [optional] 
**tid** | **int** |  | 
**create_time** | **int** |  | 
**update_time** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.sent_message import SentMessage

# TODO update the JSON string below
json = "{}"
# create an instance of SentMessage from a JSON string
sent_message_instance = SentMessage.from_json(json)
# print the JSON string representation of the object
print(SentMessage.to_json())

# convert the object into a dict
sent_message_dict = sent_message_instance.to_dict()
# create an instance of SentMessage from a dict
sent_message_from_dict = SentMessage.from_dict(sent_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


