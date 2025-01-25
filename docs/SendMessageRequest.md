# SendMessageRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_id** | **str** |  | [optional] [default to 'works']
**channel_no** | **int** |  | 
**temp_message_id** | **int** |  | [optional] [default to 733428260]
**caller** | [**Caller**](Caller.md) |  | 
**extras** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**type** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.send_message_request import SendMessageRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SendMessageRequest from a JSON string
send_message_request_instance = SendMessageRequest.from_json(json)
# print the JSON string representation of the object
print(SendMessageRequest.to_json())

# convert the object into a dict
send_message_request_dict = send_message_request_instance.to_dict()
# create an instance of SendMessageRequest from a dict
send_message_request_from_dict = SendMessageRequest.from_dict(send_message_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


