Vagrant.configure(2) do |config|
  config.vm.box = "bento/centos-6.7"

  (1..2).each do |i|
    config.vm.define "app-#{i}" do |app|
      app.vm.provision "chef_solo" do |chef|
        chef.add_recipe "sbapp::appnode"
        chef.json = {
          "env" => "whatami",
        }
      end
    end
  end


  config.vm.network :forwarded_port, guest: 80, host: 9898
end
