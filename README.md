# ig-driver

## Brief

Instagram navigator with Selenium Driver.
The script runs once and does the following:
1. Login to given account
2. Likes a page post of a different given user
3. Likes given hashtags.
4. Selects randomly from given comments and posts them on given hashtags.


## Constraints

1. The script has a fixed time out so it does not handle time outs correctly.
1. The script has to have an example.in to run.
1. The script look for a fixed number of pages only, most recent depending on the render of the web browser.
1. The script relies on SeleniumDriver for Chrome.

# Setup development

## Workspace setup
On workspace run:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r ./requirements.txt
```

Ensure to have SeleniumDriver installed.
For installation steps, follow https://www.nuget.org/packages/Selenium.WebDriver:w
 
 
 ## Config setup
 Create a file `example.ini` in the workspace path.
 Copy and refer to `.example.ini` template.
 
 ## Run script
 
```
python3 run.py
```
