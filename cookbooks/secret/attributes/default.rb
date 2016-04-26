default['php']['version'] = "5.5.9"
default['docroot'] = "/var/www/secret"
default['apache']['mpm'] = "prefork"
default['env'] = "dev"

case node['env']
when 'dev'
  default['apache']['server_name']="test.dev.secretsales.com"
when 'pro'
  default['apache']['server_name']="test.secretsales.com"
  default['apache']['prefork']['startservers']        = 32
  default['apache']['prefork']['minspareservers']     = 32
end

