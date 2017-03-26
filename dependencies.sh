#!/bin/sh

sudo pip3 install beautifulsoup4

# https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh
sudo apt-get install -y openssl build-essential xorg libssl-dev
wget http://download.gna.org/wkhtmltopdf/0.12/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
tar -xJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
cd wkhtmltox
sudo chown root:root bin/wkhtmltopdf
sudo cp -r * /usr/
cd ..
rm wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
rm -rf wkhtmltox
# see https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server
sudo apt-get install xvfb
echo -e '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' | sudo tee /usr/bin/wkhtmltopdf.sh > /dev/null
sudo chmod a+x /usr/bin/wkhtmltopdf.sh
sudo ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf
# Finallly we can install pdfkit...
sudo pip3 install pdfkit