"""
sudo apt update
sudo apt install python python-dev python3 python3-dev
sudo apt-get install python3-setuptools
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
alias python=python3
sudo apt-get python3-setuptools
sudo easy_install3 pip
sudo pip3 install pandas
sudo pip3 install requests
sudo pip3 install dotenv
git clone https://github.com/raph-m/safe_driver_prediction
cd safe_driver_prediction/proj2
python gdrive.py 1EQ0zE_2WLQdNIepWUjroPyGmi-dvN5KK ../../data.zip
cd ..
cd ..
sudo apt-get install unzip
unzip data.zip
cd safe_driver_prediction
echo "ENV_NAME=vm" > .env
cd proj2
python feature_engineering.py
"""