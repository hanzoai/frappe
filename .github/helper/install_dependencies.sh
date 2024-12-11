#!/bin/bash
set -e

echo "Setting Up System Dependencies..."

<<<<<<< HEAD
echo "::group::apt packages"
=======
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
sudo apt update
sudo apt remove mysql-server mysql-client
sudo apt install libcups2-dev redis-server mariadb-client-10.6

<<<<<<< HEAD
install_wkhtmltopdf() {
  wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
  sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
}
install_wkhtmltopdf &
echo "::endgroup::"
=======
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
>>>>>>> c3bd8892e6 (fix: in case of owner, always include owner in count data)
