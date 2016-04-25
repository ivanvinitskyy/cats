Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "chef_solo" do |chef|
    chef.add_recipe "secret"
    chef.json = {
      "env" => "dev",
      "docroot" => "/var/www/secret"
      }
  end
  config.vm.network :forwarded_port, guest: 80, host: 9898
end
