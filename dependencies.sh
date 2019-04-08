#!/bin/bash

set -eux

sudo apt-get install python3-pip
sudo pip3 install beautifulsoup4

# https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh
sudo apt-get install -y openssl build-essential xorg libssl-dev
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
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
sudo ln -fs /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf
# Finallly we can install pdfkit...
sudo pip3 install pdfkit


# Install adtool
sudo apt-get install ldap-utils libldap2-dev openssl
wget https://gp2x.org/adtool/adtool-1.3.3.tar.gz
tar -xvf adtool-1.3.3.tar.gz
cd adtool-1.3.3
./configure
make
sudo make install

# Configure it
cat | sudo tee '/usr/local/etc/adtool.cfg' << EOF
uri ldaps://intranet.epfl.ch
binddn CN=Pirelli Solal,OU=DSLAB-Users,OU=DSLAB,OU=IINFCOM,OU=IC,DC=intranet,DC=epfl,DC=ch
bindpw LALALA
searchbase DC=intranet,DC=epfl,DC=ch
EOF

# Allow ldap to bind properly to intranet.epfl.ch
echo -e '\n# Workaround for EPFL\nTLS_REQCERT\tallow' | sudo tee -a /etc/ldap/ldap.conf
