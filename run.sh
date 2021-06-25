# Prerequisite
apt-get update
apt-get install -y git tor curl python3 make python3-pip wget

# Kalitorify
git clone https://github.com/brainfucksec/kalitorify.git
cd kalitorify && make install && cd .. && rm -rf kalitorify

# Chrome
CHROME_VERSION="89.0.4389.90-1"
wget -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt-get install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# Requirements
pip3 install -r requirements.txt