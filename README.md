# Zenoss Service Impact API Demo
This repo contains a python script which is designed to demonstrate how the Zenoss REST API can be used to create services.
In order to use it, you'll also need the awesome Zenoss API helper classes developed by [Adam McCurdy](https://github.com/amccurdy): https://github.com/amccurdy/zenoss_api, and will need your system configured to point this API to your target Zenoss system.

The script is designed to take a single parameter on the command line, in the form of a JSON string, containing the following entries:

- `dynamicOrganiser`: The name of the top level Dynamic Organiser to use
- `dynamicService`:   The name of the Service to use 
- `components`:       A list of the components to be added to the service, in the format:
    - `{ "device": "<device_name>", "component": "component_name" }`

For example:

```
{
    "dynamicOrganiser": "/Demo",
    "dynamicService": "Sample",
    "components": [
        { "device": "server1.sample.com", "component": "httpd" },
        { "device": "web.sample.com", "component": "httpd" },
        { "device": "dcloud.sample.com", "component": "httpd" }
    ]
}
```

## Important Caveats
Please note that this is **NOT PRODUCTION CODE**.  The code is designed to demonstrate the techniques involved in creating Services and Service Organizers.  Specifically:

1. There is no error checking in the code.
2. The code is written for readability - not using common defensive programming strategies.
3. The code makes certain assumptions:
    - The Dynamic Organizer will always be at the top level
    - The components specified will definitely exist!
    - If the service exists already, the script will still attempt to add the components.
4. This is **NOT PRODUCTION CODE!** ;-)
