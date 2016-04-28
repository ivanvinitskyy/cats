include_recipe 'nginx'

template "#{node['nginx']['dir']}/sites-available/sbapp" do
  source 'sbapp.erb'
  owner  'root'
  group  node['root_group']
  mode   '0644'
  notifies :reload, 'service[nginx]', :delayed
end

nginx_site 'sbapp'
