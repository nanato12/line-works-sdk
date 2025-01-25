# MyInfo



## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tenant_id** | **int** |  | 
**domain_id** | **int** |  | 
**contact_no** | **int** |  | 
**read_only** | **bool** |  | 
**temp_id** | **bool** |  | 
**name** | [**Name**](Name.md) |  | 
**i18n_name** | **str** |  | 
**i18n_names** | **List[object]** |  | 
**photos** | **List[object]** |  | 
**organizations** | [**List[Organization]**](Organization.md) |  | 
**emails** | [**List[Email]**](Email.md) |  | 
**telephones** | **List[object]** |  | 
**messengers** | **List[object]** |  | 
**position** | **str** |  | 
**department** | **str** |  | 
**location** | **str** |  | 
**important** | **bool** |  | 
**executive** | **bool** |  | 
**photo_hash** | **str** |  | 
**works_at** | [**WorksAt**](WorksAt.md) |  | 
**access_limit** | **bool** |  | 
**user_photo_modify** | **bool** |  | 
**user_absence_modify** | **bool** |  | 
**organization** | **str** |  | 
**groups** | **List[object]** |  | 
**works_services** | **List[str]** |  | 
**custom_fields** | **List[object]** |  | 
**profile_statuses** | **List[object]** |  | 
**profile_statuses_v2** | **List[object]** |  | 
**instance** | **int** |  | 

## Example

```python
from line_works.openapi.talk.models.my_info import MyInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MyInfo from a JSON string
my_info_instance = MyInfo.from_json(json)
# print the JSON string representation of the object
print(MyInfo.to_json())

# convert the object into a dict
my_info_dict = my_info_instance.to_dict()
# create an instance of MyInfo from a dict
my_info_from_dict = MyInfo.from_dict(my_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


