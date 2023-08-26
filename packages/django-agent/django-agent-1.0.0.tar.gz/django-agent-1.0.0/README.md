# Django Agent


This is a Django app that provides an API for executing shell commands and retrieving their output.

## Quick start

*  Add **django_agent** to your **INSTALLED_APPS** setting like this
```
INSTALLED_APPS = [
    ...,
    "django_agent",
]
```
* Include the  **django_agent** URLconf in your project **urls.py** like this
```
path("agent/", include("django_agent.urls")),
```
   


* Add **AGENT_TOKEN**  to your project **settings.py** like this
```
...
AGENT_TOKEN="my-agent-token"
```
