#anaconda_url=https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh


echo "Install programas uteis"
sudo apt-get -y update
sudo apt-get -y install tree


echo "Install Anaconda"
anaconda_url=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
cd /tmp
curl -O $anaconda_url
#sudo bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
bash Miniconda3-latest-Linux-x86_64.sh

#Altera owner da pasta, apenas se a instalação for feita pelo sudo
#sudo chown -R 1001:1002 $HOME/.conda

#Restart terminal (não funcionando, tem que fazer na mão)
source ~/.bashrc