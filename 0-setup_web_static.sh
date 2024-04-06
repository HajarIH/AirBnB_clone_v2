#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/{releases,test,shared}
sudo chown -R ubuntu:ubuntu /data/

# Create a fake HTML file for testing
sudo mkdir -p /data/web_static/releases/test/
sudo tee /data/web_static/releases/test/index.html > /dev/null <<EOF
<html>
  <head>
  </head>
  <body>
    <h1>This is a test page</h1>
  </body>
</html>
EOF

# Ensure proper symbolic link creation
if [ ! -d "/data/web_static/releases/test/" ]; then
	    echo "Error: /data/web_static/releases/test/ directory not found."
	        exit 1
fi

# Remove existing symbolic link if exists
sudo rm -f /data/web_static/current

# Create symbolic link
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Update Nginx configuration if not already present
if ! grep -q '/hbnb_static' /etc/nginx/sites-enabled/default; then
	    sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
fi

# Restart Nginx
sudo systemctl restart nginx
