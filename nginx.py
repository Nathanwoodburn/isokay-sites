import os

def write_nginx_conf(domain):

    ssl = f'''
        listen 443 ssl;
        ssl_certificate /root/hns-links/certs/{domain}/cert.crt;
        ssl_certificate_key /root/hns-links/certs/{domain}/cert.key;
        '''
    

    conf = f'''
    server {{
  listen 80;
  listen [::]:80;
  server_name {domain} *.{domain};

    location / {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}

    
    {ssl}
    }}
    '''

    
    with open(f'/etc/nginx/sites-enabled/{domain}.conf', 'w') as file:
        file.write(conf)

    # Restart nginx
    os.system('systemctl restart nginx')
    return True

def generate_ssl(domain):
    tlsa = os.popen(f'./tlsa.sh {domain}').read().strip()
    return tlsa