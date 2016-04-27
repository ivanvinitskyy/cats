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
  source 'https://raw.githubusercontent.com/ivanvinitskyy/projects/sb/socalledreleasebranch/sbapp.go'
  owner 'sbapp'
  group 'sbapp'
  mode '0755'
  action :create
  notifies :restart, 'supervisor_service[sbapp]', :delayed
end

supervisor_service "sbapp" do
  command "#{node['sbapp']['docroot']}/sbapp.go"
  action :enable
  autostart true
  user "sbapp"
end
