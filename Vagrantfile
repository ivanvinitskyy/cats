Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "chef_solo" do |chef|
    chef.add_recipe "php"
    chef.add_recipe "apache2"
    chef.add_recipe "apache2::mod_php5"
    chef.add_recipe "secret"
    chef.json = {
      "env" => "pro",
      "docroot" => "/var/www/secret"
      }
  end
  config.vm.network :forwarded_port, guest: 80, host: 9898
end
