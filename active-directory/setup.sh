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
binddn CN=Pirelli Solal,OU=NAL-Users,OU=NAL,OU=IINFCOM,OU=IC,DC=intranet,DC=epfl,DC=ch
bindpw LALALA
searchbase DC=intranet,DC=epfl,DC=ch
EOF

# Allow ldap to bind properly to intranet.epfl.ch
echo -e '\n# Workaround for EPFL\nTLS_REQCERT\tallow' | sudo tee -a /etc/ldap/ldap.conf
