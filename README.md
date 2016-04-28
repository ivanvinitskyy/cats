sbapp Cookbook
===========================
Creates 2 app servers and 1 web.  Web server load balances in RR mode between app servers with NGINX.
App servers both run Go which prints server hostname when called.
Go App is built with Chef when source code changes.
Source code is fetched from socalledbranch directory.  This is to simulate release process.
App servers cron chef run every 5min so automated build and releasing can occur.

Requirements
------------
Must have vagrant installed

Attributes
----------
```
node['sbapp']['appport']
node['sbapp']['docroot']
```

Usage
-----
Run startDemo.sh to launch vagrant instances, test through web server and evaluate the result 

```
./startDemo.sh
...
...
All requests were served in RR mode
```

License and Authors
-------------------
Authors: Ivan Vinitskyy
