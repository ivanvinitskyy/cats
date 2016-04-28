include_recipe 'yum-epel', 'supervisor'

package 'golang'

user 'sbapp' do
  comment 'SB App user'
  home '/home/sbapp'
  shell '/sbin/nologin'
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
  notifies :run, 'bash[build sbapp]', :immediate
end

bash 'build sbapp' do
  cwd "#{node['sbapp']['docroot']}"
  code <<-EOH
    /usr/bin/go build sbapp.go
  EOH
  notifies :restart, 'supervisor_service[sbapp]', :delayed
  action :nothing
end

supervisor_service "sbapp" do
  command "#{node['sbapp']['docroot']}/sbapp"
  process_name "sbapp"
  action :enable
  autostart true
  user "sbapp"
end

cron "run-chef" do
  hour "*"
  minute "*/5"
  weekday "*"
  user "root"
  command "/usr/bin/chef-solo chef-solo -c /tmp/vagrant-chef/solo.rb -j /tmp/vagrant-chef/dna.json --run-lock-timeout 0 &> /dev/null; echo $? > /tmp/chef-exitcode"
end
