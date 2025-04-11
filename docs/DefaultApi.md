# line_works.openapi.talk.DefaultApi

All URIs are relative to *https://talk.worksmobile.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_channel_members**](DefaultApi.md#get_channel_members) | **POST** /p/oneapp/client/chat/getChannelMembers | Get Channel Members
[**get_my_info**](DefaultApi.md#get_my_info) | **GET** /p/contact/v3/domain/contacts/my | Get My Information
[**issue_resource_path**](DefaultApi.md#issue_resource_path) | **POST** /p/oneapp/client/chat/issueResourcePath | 
[**leave_channel**](DefaultApi.md#leave_channel) | **POST** /p/oneapp/client/chat/quit | Leave Channel
[**send_message**](DefaultApi.md#send_message) | **POST** /p/oneapp/client/chat/sendMessage | Send Message


# **get_channel_members**
> GetChannelMembersResponse get_channel_members(cookie=cookie, get_channel_members_request=get_channel_members_request)

Get Channel Members

Get information about the members in the channel.

### Example


```python
import line_works.openapi.talk
from line_works.openapi.talk.models.get_channel_members_request import GetChannelMembersRequest
from line_works.openapi.talk.models.get_channel_members_response import GetChannelMembersResponse
from line_works.openapi.talk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://talk.worksmobile.com
# See configuration.py for a list of all supported configuration parameters.
configuration = line_works.openapi.talk.Configuration(
    host = "https://talk.worksmobile.com"
)


# Enter a context with an instance of the API client
with line_works.openapi.talk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = line_works.openapi.talk.DefaultApi(api_client)
    cookie = 'cookie_example' # str | cookie (optional)
    get_channel_members_request = line_works.openapi.talk.GetChannelMembersRequest() # GetChannelMembersRequest |  (optional)

    try:
        # Get Channel Members
        api_response = api_instance.get_channel_members(cookie=cookie, get_channel_members_request=get_channel_members_request)
        print("The response of DefaultApi->get_channel_members:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_channel_members: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| cookie | [optional] 
 **get_channel_members_request** | [**GetChannelMembersRequest**](GetChannelMembersRequest.md)|  | [optional] 

### Return type

[**GetChannelMembersResponse**](GetChannelMembersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_my_info**
> MyInfo get_my_info(cookie=cookie)

Get My Information

Get your own information.

### Example


```python
import line_works.openapi.talk
from line_works.openapi.talk.models.my_info import MyInfo
from line_works.openapi.talk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://talk.worksmobile.com
# See configuration.py for a list of all supported configuration parameters.
configuration = line_works.openapi.talk.Configuration(
    host = "https://talk.worksmobile.com"
)


# Enter a context with an instance of the API client
with line_works.openapi.talk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = line_works.openapi.talk.DefaultApi(api_client)
    cookie = 'cookie_example' # str | cookie (optional)

    try:
        # Get My Information
        api_response = api_instance.get_my_info(cookie=cookie)
        print("The response of DefaultApi->get_my_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_my_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| cookie | [optional] 

### Return type

[**MyInfo**](MyInfo.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **issue_resource_path**
> IssueResourcePathResponse issue_resource_path(cookie=cookie, issue_resource_path_request=issue_resource_path_request)



Issue the path to where the resource will be uploaded.

### Example


```python
import line_works.openapi.talk
from line_works.openapi.talk.models.issue_resource_path_request import IssueResourcePathRequest
from line_works.openapi.talk.models.issue_resource_path_response import IssueResourcePathResponse
from line_works.openapi.talk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://talk.worksmobile.com
# See configuration.py for a list of all supported configuration parameters.
configuration = line_works.openapi.talk.Configuration(
    host = "https://talk.worksmobile.com"
)


# Enter a context with an instance of the API client
with line_works.openapi.talk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = line_works.openapi.talk.DefaultApi(api_client)
    cookie = 'cookie_example' # str | cookie (optional)
    issue_resource_path_request = line_works.openapi.talk.IssueResourcePathRequest() # IssueResourcePathRequest |  (optional)

    try:
        # 
        api_response = api_instance.issue_resource_path(cookie=cookie, issue_resource_path_request=issue_resource_path_request)
        print("The response of DefaultApi->issue_resource_path:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->issue_resource_path: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| cookie | [optional] 
 **issue_resource_path_request** | [**IssueResourcePathRequest**](IssueResourcePathRequest.md)|  | [optional] 

### Return type

[**IssueResourcePathResponse**](IssueResourcePathResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **leave_channel**
> LeaveChannelResponse leave_channel(cookie=cookie, leave_channel_request=leave_channel_request)

Leave Channel

Leave from the channel.

### Example


```python
import line_works.openapi.talk
from line_works.openapi.talk.models.leave_channel_request import LeaveChannelRequest
from line_works.openapi.talk.models.leave_channel_response import LeaveChannelResponse
from line_works.openapi.talk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://talk.worksmobile.com
# See configuration.py for a list of all supported configuration parameters.
configuration = line_works.openapi.talk.Configuration(
    host = "https://talk.worksmobile.com"
)


# Enter a context with an instance of the API client
with line_works.openapi.talk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = line_works.openapi.talk.DefaultApi(api_client)
    cookie = 'cookie_example' # str | cookie (optional)
    leave_channel_request = line_works.openapi.talk.LeaveChannelRequest() # LeaveChannelRequest |  (optional)

    try:
        # Leave Channel
        api_response = api_instance.leave_channel(cookie=cookie, leave_channel_request=leave_channel_request)
        print("The response of DefaultApi->leave_channel:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->leave_channel: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| cookie | [optional] 
 **leave_channel_request** | [**LeaveChannelRequest**](LeaveChannelRequest.md)|  | [optional] 

### Return type

[**LeaveChannelResponse**](LeaveChannelResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_message**
> SendMessageResponse send_message(cookie=cookie, send_message_request=send_message_request)

Send Message

Send Message.

### Example


```python
import line_works.openapi.talk
from line_works.openapi.talk.models.send_message_request import SendMessageRequest
from line_works.openapi.talk.models.send_message_response import SendMessageResponse
from line_works.openapi.talk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://talk.worksmobile.com
# See configuration.py for a list of all supported configuration parameters.
configuration = line_works.openapi.talk.Configuration(
    host = "https://talk.worksmobile.com"
)


# Enter a context with an instance of the API client
with line_works.openapi.talk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = line_works.openapi.talk.DefaultApi(api_client)
    cookie = 'cookie_example' # str | cookie (optional)
    send_message_request = line_works.openapi.talk.SendMessageRequest() # SendMessageRequest |  (optional)

    try:
        # Send Message
        api_response = api_instance.send_message(cookie=cookie, send_message_request=send_message_request)
        print("The response of DefaultApi->send_message:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->send_message: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| cookie | [optional] 
 **send_message_request** | [**SendMessageRequest**](SendMessageRequest.md)|  | [optional] 

### Return type

[**SendMessageResponse**](SendMessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

