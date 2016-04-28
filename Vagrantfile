Vagrant.configure(2) do |config|
  config.vm.box = "bento/centos-6.7"

  (1..2).each do |i|
    config.vm.define "app-#{i}" do |app|
      app.vm.hostname = "app-#{i}"
      app.vm.network :private_network, ip: "10.10.10.#{i+1}", :netmask => "255.0.0.0"
      app.vm.provision "chef_solo" do |chef|
        chef.add_recipe "sbapp::appnode"
        chef.json = {
          "env" => "whatami",
        }
      end
    end
  end

  config.vm.define "web-1" do |web|
    web.vm.hostname = "web-1"
    web.vm.network :private_network, ip: "10.10.10.254", :netmask => "255.0.0.0"
    web.vm.provision "chef_solo" do |chef|
      chef.add_recipe "sbapp::webnode"
      chef.json = {
        "appservers" => [
	  "10.10.10.2",
          "10.10.10.3"
        ]
      }
      end
    web.vm.network "forwarded_port", guest: 9999, host: 9999
  end

end
