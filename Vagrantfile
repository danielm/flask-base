#
# File: Vagrantfile
# 
# By: Daniel Morales <daniminas@gmail.com>
#
# Web: https://github.com/danielm/flask-base
#
# Licence: GPL/MIT

# Configuration file version
Vagrant.configure(2) do |config|

  # Box
  config.vm.box = "ubuntu/focal64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Provisioning our Box
  config.vm.provision "shell", inline:<<-SHELL
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get install python3 python-is-python3 python3-pip python3-virtualenv -y

SHELL
end