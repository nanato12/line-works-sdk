# WorksAt


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**invite_url** | **str** |  | 
**users** | [**List[User]**](User.md) |  | 
**works_at_count** | **int** |  | 
**id_search_block** | **bool** |  | 

## Example

```python
from line_works.openapi.talk.models.works_at import WorksAt

# TODO update the JSON string below
json = "{}"
# create an instance of WorksAt from a JSON string
works_at_instance = WorksAt.from_json(json)
# print the JSON string representation of the object
print(WorksAt.to_json())

# convert the object into a dict
works_at_dict = works_at_instance.to_dict()
# create an instance of WorksAt from a dict
works_at_from_dict = WorksAt.from_dict(works_at_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


