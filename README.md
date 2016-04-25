secret Cookbook
===========================
Minimal set of cookbooks and options used to set up this php app.  Most default values didn't need changing but some were to demonstrate that it can be done.
Some node variables were specified in vagrant to show they don't all have to be specificed in source code.
To keep recipe simple, no platform checking takes place though both PHP and Apache2 cookbooks have it.
Since this is a testing instance, chef run is only executed once on image provisioning.


To test:
sudo vagrant up --provision
wget localhost:9898 --header "Host: test.dev.secretsales.com" -O - | grep -o '<h1 class="p">.*</h1>'

Requirements
------------
Must run under Ubuntu.  Might work with other OS but no guarantee versions will be correct.

Attributes
----------
Evironment type.  Supported types are pro and dev.  Dev is default if not specified.

Usage
-----
#### secret::default
Running secret default recipe calls php and apache cookbooks to set up the project.  Starts it once deployed.

```json
{
  "env":"dev",
  "run_list": [
    "recipe[secret]"
  ]
}
```

License and Authors
-------------------
Authors: Ivan Vinitskyy
