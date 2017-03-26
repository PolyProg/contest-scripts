#!/bin/sh

sudo pip3 install beautifulsoup4

# see https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server
sudo apt-get install wkhtmltopdf xvfb
sudo pip3 install pdfkit
echo -e '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' | sudo tee /usr/bin/wkhtmltopdf.sh
sudo chmod a+x /usr/bin/wkhtmltopdf.sh
sudo ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf