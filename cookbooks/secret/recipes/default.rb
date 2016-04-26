include_recipe 'sysctl', 'php', 'apache2', 'apache2::mod_php5'

sysctl_param 'net.ipv4.tcp_fin_timeout' do
  value 10
  action :apply
end

web_app 'secret' do
  docroot node['docroot']
  server_name node['apache']['server_name']
  cookbook "apache2"
end

bash 'get project' do
  code <<-EOH
    mkdir -p #{node['docroot']}
    curl https://s3-eu-west-1.amazonaws.com/secretsales-dev-test/devops/test.tar.gz | tar xvz -C #{node['docroot']}
    touch /tmp/projectdeployed
    EOH
  not_if { ::File.exists?('/tmp/projectdeployed') }
end

service 'apache' do
  case node['platform']
  when 'centos','redhat','fedora'
    service_name 'httpd'
  when 'ubuntu', 'debian'
    service_name 'apache2'
  end
  supports :status => true
  action [:start, :enable]
end

bash 'redeploy' do
  code <<-EOH  
    curl https://s3-eu-west-1.amazonaws.com/secretsales-dev-test/devops/test.tar.gz | tar xvz -C #{node['docroot']}
    service apache2 reload
  EOH
  action :nothing
end
