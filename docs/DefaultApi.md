# line_works.openapi.talk.DefaultApi

All URIs are relative to *https://talk.worksmobile.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_my_info**](DefaultApi.md#get_my_info) | **GET** /p/contact/v3/domain/contacts/my | Get My Information
[**send_message**](DefaultApi.md#send_message) | **POST** /p/oneapp/client/chat/sendMessage | Send Message


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

