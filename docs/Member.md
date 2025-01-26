# Member


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_no** | **int** |  | 
**name** | **str** |  | 
**i18n_name** | **str** |  | 
**i18n_names** | **List[object]** |  | 
**nick_name** | **str** |  | 
**position** | **str** |  | 
**i18n_positions** | **List[object]** |  | 
**group_name** | **str** |  | 
**i18n_group_names** | **List[object]** |  | 
**group_position** | **str** |  | 
**i18n_group_positions** | **List[object]** |  | 
**photo_hash** | **str** |  | 
**join** | **bool** |  | 
**join_time** | **int** |  | 
**update_time** | **int** |  | 
**domain_id** | **int** |  | 
**property_flag** | **int** |  | 
**domain_name** | **str** |  | 
**i18n_domain_names** | **List[object]** |  | 
**service_type** | **str** |  | 
**relation_status** | **str** |  | 
**tenant_id** | **int** |  | 
**guest** | **bool** |  | 

## Example

```python
from line_works.openapi.talk.models.member import Member

# TODO update the JSON string below
json = "{}"
# create an instance of Member from a JSON string
member_instance = Member.from_json(json)
# print the JSON string representation of the object
print(Member.to_json())

# convert the object into a dict
member_dict = member_instance.to_dict()
# create an instance of Member from a dict
member_from_dict = Member.from_dict(member_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


