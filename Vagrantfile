# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise32"  
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.provision :shell, :path => "Vagrantfile_.sh"

  config.vm.network :forwarded_port, host: 6543, guest: 6543

  #config.vm.network :private_network, ip: "10.0.0.2"

  config.vm.provider "virtualbox" do |v|
    v.name = "TrackMyBus"
  end

end
