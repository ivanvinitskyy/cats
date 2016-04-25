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
  not_if { ::File.exists?('/tmp/projectreployed') }
end

service 'apache2' do
  supports :status => true
  action [:enable, :start]
end
