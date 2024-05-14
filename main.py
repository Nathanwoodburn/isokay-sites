from flask import Flask, make_response, redirect, request, jsonify, render_template, send_from_directory, render_template_string
import os
import dotenv
import requests
import datetime
import json
import render
import secrets
import nginx
import threading

app = Flask(__name__)
dotenv.load_dotenv()

# Get site domains
DOMAINS = os.getenv('DOMAINS')
DOMAINS = json.loads(DOMAINS)

# Add local domains
# DOMAINS.append('localhost:5000')
DOMAINS.append('127.0.0.1:5000')
IP = "0.0.0.0"

try:
    IP = requests.get('https://ipinfo.io/ip').text.strip()
except:
    IP = "Error"

# Load cookies
cookies = []

if os.path.isfile('cookies.json'):
    with open('cookies.json') as file:
        cookies = json.load(file)
else:
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)

if not os.path.isdir('avatars'):
    os.mkdir('avatars')

if not os.path.isdir('sites'):
    os.mkdir('sites')

if not os.path.isdir('certs'):
    os.mkdir('certs')

if not os.path.isdir('images'):
    os.mkdir('images')

#Assets routes
@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('templates/assets', path)

@app.route('/https.js')
def httpsJS():
    return send_from_directory('templates', 'https.js')

@app.route('/favicon.png')
def faviconPNG():
    return send_from_directory('templates/assets/img', 'favicon.png')


# Main routes
@app.route('/')
def index():
    if request.host in DOMAINS:        
        if 'auth' in request.cookies:
            auth = request.cookies['auth']
            for i in cookies:
                if i['cookie'] == auth:
                    return render_template('index.html',varo="window.location = '/site';", year=datetime.datetime.now().year)
        return render_template('index.html',varo=render.varo_login(), year=datetime.datetime.now().year)
    # Remove any ports
    host = request.host.split(':')[0]
    # Get content from site
    if os.path.isfile(f'sites/{host}.json'):
        with open(f'sites/{host}.json') as file:
            data = json.load(file)
        
        return render.site(data, host)
    return redirect(f'https://{DOMAINS[0]}')

@app.route('/site')
def site():
    # Get auth domain
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']
    for i in cookies:
        if i['cookie'] == auth:
            # Load site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)
                    # preview = render.preview(data)
            else:
                with open(f'sites/example.json') as file:
                    # data = json.load(file)
                    # preview = render.preview(data)
                    data = {
                        'title': '',
                        'link_0': '',
                        'link_1': '',
                        'link_2': '',
                        'link_3': '',
                        'link_0_url': '',
                        'link_1_url': '',
                        'link_2_url': '',
                        'link_3_url': '',
                        'image': '',
                        "bg_0": "#001665",
                        "bg_1": "#000000",
                        "fg_0": "#ffffff",
                        "btn_bg": "#2c54cf",
                        "btn_fg": "#ffffff",
                        "socials": [],
                        "address": [],
                        "nostrs": [],
                        "bio": "",
                        "gallery-link": False,
                        "bg": "",
                        "gallery_imgs": {},
                        "gallery_desc":{
                            "0": "",
                            "1": "",
                            "2": "",
                            "3": "",
                            "4": "",
                            "5": "",
                            "6": "",
                            "7": "",
                            "8": ""
                        },
                        "redirect": ""
                    }


            title = data['title']
            link_0 = data['link_0']
            link_1 = data['link_1']
            link_2 = data['link_2']
            link_3 = data['link_3']
            link_0_url = data['link_0_url']
            link_1_url = data['link_1_url']
            link_2_url = data['link_2_url']
            link_3_url = data['link_3_url']
            btn_bg = data['btn_bg']
            btn_fg = data['btn_fg']
            address = data['address']
            bio = data['bio']
            gallery_link = data['gallery-link']
            gallery_imgs = data['gallery_imgs']
            gallery_desc = data['gallery_desc']
            if 'redirect' not in data:
                data['redirect'] = ''
            redirect_url = data['redirect']

            
            address = {i['token']: i['address'] for i in address}
            tlsa = data['tlsa'] if 'tlsa' in data else ''
            ip = IP

            return render_template('site.html', year=datetime.datetime.now().year, domain=i['name'],
            title=title, link_0=link_0, link_1=link_1, link_2=link_2, link_3=link_3,
            link_0_url=link_0_url, link_1_url=link_1_url, link_2_url=link_2_url,
            link_3_url=link_3_url, btn_bg=btn_bg, btn_fg=btn_fg,address=address,
            tlsa=tlsa,ip=ip,bio=bio,gallery_link=gallery_link,gallery_imgs=gallery_imgs,gallery_desc=gallery_desc,redirect_url=redirect_url)
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/site', methods=['POST'])
def site_post():
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']

    for i in cookies:
        if i['cookie'] == auth:
            # Get site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)
            else:
                with open(f'sites/example.json') as file:
                    data = {}


            # Save site content
            data['title'] = request.form['title']
            data['link_0'] = request.form['link_0']
            data['link_1'] = request.form['link_1']
            data['link_2'] = request.form['link_2']
            data['link_3'] = request.form['link_3']
            data['link_0_url'] = request.form['link_0_url']
            data['link_1_url'] = request.form['link_1_url']
            data['link_2_url'] = request.form['link_2_url']
            data['link_3_url'] = request.form['link_3_url']
            data['btn_bg'] = request.form['btn_bg']
            data['btn_fg'] = request.form['btn_fg']
            data['bio'] = request.form['bio']
            data['redirect'] = request.form['redirect']
            data['gallery-link'] = 'gallery-link' in request.form
            if 'image' not in data:
                data['image'] = ''
            if 'bg' not in data:
                data['bg'] = ''
            
            if 'gallery_imgs' not in data:
                data['gallery_imgs'] = {}
            if 'gallery_desc' not in data:
                data['gallery_desc'] = {}
            

            address = []
            # address.append({'token': 'hns', 'address': request.form['hns']})
            # address.append({'token': 'eth', 'address': request.form['eth']})
            # address.append({'token': 'btc', 'address': request.form['btc']})
            # address.append({'token': 'sol', 'address': request.form['sol']})


            address = [i for i in address if i['address'] != '']
            data['address'] = address

            if 'image' in request.files:
                if request.files['image'].filename != '' and request.files['image'].filename != None:
                    file = request.files['image']
                    extension = file.filename.split('.')[-1]

                    file.save(f'avatars/{i["name"]}.' + extension)
                    data['image'] = f'{i["name"]}.' + extension   

            if 'bg' in request.files:
                if request.files['bg'].filename != '' and request.files['bg'].filename != None:
                    file = request.files['bg']
                    extension = file.filename.split('.')[-1]

                    file.save(f'images/{i["name"]}bg.' + extension)
                    data['bg'] = f'{i["name"]}bg.' + extension            
            

            # Gallery images
            for j in range(9):
                if f'gallery_{j}_img' in request.files:
                    if request.files[f'gallery_{j}_img'].filename != '' and request.files[f'gallery_{j}_img'].filename != None:
                        file = request.files[f'gallery_{j}_img']
                        extension = file.filename.split('.')[-1]

                        file.save(f'images/{i["name"]}gallery{j}.' + extension)
                        data['gallery_imgs'][str(j)] = f'{i["name"]}gallery{j}.' + extension
                data[f'gallery_desc'][str(j)] = request.form[f'gallery_{j}']

            with open(f'sites/{i["name"]}.json', 'w') as file:
                json.dump(data, file)
            return redirect('/site')
        
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/image/delete')
def delete_image():
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']

    for i in cookies:
        if i['cookie'] == auth:
            # Get site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)
                    if 'image' in data:
                        data['image'] = ''
                        with open(f'sites/{i["name"]}.json', 'w') as file:
                            json.dump(data, file)
            return redirect('/site')
                
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/bg/delete')
def delete_bg():
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']

    for i in cookies:
        if i['cookie'] == auth:
            # Get site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)
                    if 'bg' in data:
                        data['bg'] = ''
                        with open(f'sites/{i["name"]}.json', 'w') as file:
                            json.dump(data, file)
            return redirect('/site')
                
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/preview')
def site_preview():
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']

    for i in cookies:
        if i['cookie'] == auth:
            # Load site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)                    
            else:
                with open(f'sites/example.json') as file:
                    data = json.load(file)
            return render.site(data)
                
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/gallery')
def gallery():
    if 'auth' in request.cookies:
        auth = request.cookies['auth']

        for i in cookies:
            if i['cookie'] == auth:
                # Load site content
                if os.path.isfile(f'sites/{i["name"]}.json'):
                    with open(f'sites/{i["name"]}.json') as file:
                        data = json.load(file)                    
                else:
                    with open(f'sites/example.json') as file:
                        data = json.load(file)
                return render.gallery(data)
                    
        response = make_response(redirect('/'))
        response.set_cookie('auth', '', expires=0)
        return response
    
    if request.host in DOMAINS:        
        return redirect('/')
    # Remove any ports
    host = request.host.split(':')[0]
    # Get content from site
    if os.path.isfile(f'sites/{host}.json'):
        with open(f'sites/{host}.json') as file:
            data = json.load(file)
        
        return render.gallery(data, host)
    return redirect(f'https://{DOMAINS[0]}')

@app.route('/publish')
def publish():
    if 'auth' not in request.cookies:
        return redirect('/')
    auth = request.cookies['auth']

    for i in cookies:
        if i['cookie'] == auth:
            # Load site content
            if os.path.isfile(f'sites/{i["name"]}.json'):
                with open(f'sites/{i["name"]}.json') as file:
                    data = json.load(file)
                    if 'tlsa' in data:
                        # Site is already published
                        return redirect('/site')
                    def generate_ssl_and_write_nginx():
                        tlsa = nginx.generate_ssl(i['name'])
                        data['tlsa'] = tlsa
                        with open(f'sites/{i["name"]}.json', 'w') as file:
                            json.dump(data, file)
                        nginx.write_nginx_conf(i['name'])

                    threading.Thread(target=generate_ssl_and_write_nginx).start()
                    return redirect('/publishing')


                    
    response = make_response(redirect('/'))
    response.set_cookie('auth', '', expires=0)
    return response

@app.route('/.well-known/wallets/<path:path>')
def wallets(path):
    # Check if host is in domains
    if request.host in DOMAINS:
        # Check if user is logged in
        if 'auth' not in request.cookies:
            return redirect(f'https://{DOMAINS[0]}')
        auth = request.cookies['auth']
        for i in cookies:
            if i['cookie'] == auth:
                # Load site content
                if os.path.isfile(f'sites/{i["name"]}.json'):
                    with open(f'sites/{i["name"]}.json') as file:
                        data = json.load(file)
                    for i in data['address']:
                        if i['token'].upper() == path:
                            # Return as plain text
                            response = make_response(i['address'])
                            response.headers['Content-Type'] = 'text/plain'
                            return response

    # Get wallet from domain
    host = request.host.split(':')[0]

    if os.path.isfile(f'sites/{host}.json'):
        with open(f'sites/{host}.json') as file:
            data = json.load(file)
        for i in data['address']:
            if i['token'].upper() == path:
                # Return as plain text
                response = make_response(i['address'])
                response.headers['Content-Type'] = 'text/plain'
                return response
    return render_template('404.html', year=datetime.datetime.now().year), 404

@app.route('/publishing')
def publishing():
    return render_template('publishing.html')

# region Auth
@app.route('/auth', methods=['POST'])
def auth():
    global cookies
    auth = login(request)
    if auth == False:
        return render_template('index.html',varo=render.varo_login(), year=datetime.datetime.now().year, error="Failed to login")
    resp = make_response(render_template_string("Success"))
    # Gen cookie
    auth_cookie = secrets.token_hex(12 // 2)
    cookies.append({'name': auth, 'cookie': auth_cookie})

    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)

    resp.set_cookie('auth', auth_cookie)
    return resp

@app.route('/logout')
def logout():
    global cookies
    resp = make_response(redirect('/'))
    resp.set_cookie('auth', '', expires=0)

    if 'auth' not in request.cookies:
        return resp
    cookies = [i for i in cookies if i['cookie'] != request.cookies['auth']]
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)

    return resp

def login(request):
    dict = request.form.to_dict()
    keys = dict.keys()
    keys = list(keys)[0]
    keys = json.loads(keys)
    auth_request = keys['request']
    # return login(auth_request)
    r = requests.get(f'https://auth.varo.domains/verify/{auth_request}')
    r = r.json()
    if r['success'] == False:
        return False
    
    if 'data' in r:
        data = r['data']
        if 'name' in data:
            return data['name']
    return False

# endregion

@app.route('/avatar/<path:path>')
def avatar(path):
    return send_from_directory('avatars', path)

@app.route('/images/')
def no_image():
    return send_from_directory('templates/assets/img', 'noimage.webp')

@app.route('/images/<path:path>')
def images(path):
    return send_from_directory('images', path)
    

@app.route('/token/<path:path>')
def tokens(path):
    # Convert to uppercase
    path = path.upper()
    # Colour is last char
    colour = path[-1]
    token = path[:-1]
    if colour == 'W':
        return send_from_directory('templates/assets/img/tokens', f'{token}W.png')
    return send_from_directory('templates/assets/img/tokens', f'{token}.png')

# Check for other pages
@app.route('/<path:path>')
def other(path):
    if request.host not in DOMAINS:
        return render_template('404.html', year=datetime.datetime.now().year), 404
    
    if os.path.isfile(f'templates/{path}.html'):
        if 'auth' in request.cookies:
            auth = request.cookies['auth']
            for i in cookies:
                if i['cookie'] == auth:
                    return render_template(f'{path}.html', varo="window.location = '/site';", year=datetime.datetime.now().year)
        return render_template(f'{path}.html',varo=render.varo_login(), year=datetime.datetime.now().year)
    return render_template('404.html', year=datetime.datetime.now().year), 404

# 404 catch all
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', year=datetime.datetime.now().year), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')