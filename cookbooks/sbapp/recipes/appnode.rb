include_recipe 'supervisor'

package 'golang'

user 'sbapp' do
  comment 'SB App user'
  home '/home/sbapp'
  shell '/bin/nologin'
end

directory "#{node['sbapp']['docroot']}" do
  owner 'sbapp'
  group 'sbapp'
  mode '0755'
  recursive true
  action :create
end

remote_file "#{node['sbapp']['docroot']}/sbapp.go" do
  source 'https://github.com/ivanvinitskyy/projects/tree/sb/socalledreleasebranch/sbapp.go'
  owner 'sbapp'
  group 'sbapp'
  mode '0755'
  action :create
end

supervisor_service "celery" do
  command "#{node['sbapp']['docroot']}/sbapp.go"
  action :enable
  autostart true
  user "sbapp"
end

template "#{node['nginx']['dir']}/sites-available/app" do
  source 'app.erb'
  owner  'root'
  group  node['root_group']
  mode   '0644'
  notifies :reload, 'service[nginx]', :delayed
end

nginx_site 'app'
