FROM nginx:latest

# Install OpenSSL for generating SSL certificates
# RUN apt-get update && apt-get install -y openssl

# Copy the default Nginx configuration file
COPY default.conf /etc/nginx/conf.d/default.conf

# # Create directory for SSL certificates
# RUN mkdir -p /etc/nginx/ssl

# # Script to generate self-signed certificates
# COPY cert.sh /usr/local/bin/cert.sh
# RUN chmod +x /usr/local/bin/cert.sh

# # Run the certificate generation script before starting Nginx
# CMD /usr/local/bin/cert.sh && nginx -g 'daemon off;'

CMD nginx -g 'daemon off;'
