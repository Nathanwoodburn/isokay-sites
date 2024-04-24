from flask import Flask, render_template, request, jsonify, redirect

def varo_login():
    return '''
    varo.auth().then(auth => {
    if (auth.success) {
		// handle success by calling your api to update the users session
		$.post("/auth", JSON.stringify(auth.data), (response) => {
			window.location = '/site';
		});
	}
    });'''


def preview(data):
    title = data['title']
    link_0 = data['link_0']
    link_1 = data['link_1']
    link_2 = data['link_2']
    link_3 = data['link_3']
    link_0_url = data['link_0_url']
    link_1_url = data['link_1_url']
    link_2_url = data['link_2_url']
    link_3_url = data['link_3_url']
    fg_0 = data['fg_0']
    bg_0 = data['bg_0']
    bg_1 = data['bg_1']
    btn_bg = data['btn_bg']
    btn_fg = data['btn_fg']
    socials = data['socials']
    image = data['image']

    if image != "":
        image = f'<img class="rounded" src="/avatar/{image}" width="128px" height="128px" style="margin-top: 25px;" />'

    links = ""
    links += link(link_0,link_0_url,btn_bg,btn_fg)
    links += link(link_1,link_1_url,btn_bg,btn_fg)
    links += link(link_2,link_2_url,btn_bg,btn_fg)
    links += link(link_3,link_3_url,btn_bg,btn_fg)

    socials = social_links(socials)
    addresss = address_links(data['address'],fg_0)
    
    return render_template('preview_card.html', title=title, links=links, image=image, bg_0=bg_0, bg_1=bg_1, fg_0=fg_0, btn_bg=btn_bg, btn_fg=btn_fg, socials=socials, addresses=addresss)



def link(name,url,btn_bg,btn_fg):
    if url == "" or name == "":
        return ""
    colour = f'background-color: {btn_bg}; color: {btn_fg};'
    target = '_blank'
    if url.startswith('/'):
        target = '_self'
    return f'<a class="btn btn-primary custom-button" role="button" style="display: block;margin: auto;margin-bottom: 25px;width: 95%; {colour}" target="{target}" href="{url}">{name}</a>'


def social_links(socials):
    html = ''
    for social in socials:
        html += render_template(social['name'] + '.html', url=social['url'])
    return html

def address_links(addresses,foreground):
    html = ''
    for address in addresses:
        token = address['token'].upper()
        html += f'<a style="margin:5px;" href=".well-known/wallets/{token}" target="_blank">{tokenImage(token,foreground)}</a>'
    return html

def tokenImage(token,foreground):
    if is_closer_to_black(foreground):
        return f'<img src="/token/{token}B" width="32px" height="32px" style="margin-top: 25px;" />'
    return f'<img src="/token/{token}W" width="32px" height="32px" style="margin-top: 25px;" />'

def site(data, injectSSL = False):
    if 'redirect' in data:
        redirect_url:str = data['redirect']
        if redirect_url.strip() != "":
            return redirect(redirect_url, code=307)



    title = data['title']
    link_0 = data['link_0']
    link_1 = data['link_1']
    link_2 = data['link_2']
    link_3 = data['link_3']
    link_0_url = data['link_0_url']
    link_1_url = data['link_1_url']
    link_2_url = data['link_2_url']
    link_3_url = data['link_3_url']
    image = f'/avatar/{data["image"]}'
    links = ''
    if data['gallery-link']:
        links += link('Gallery','/gallery',data['btn_bg'],data['btn_fg'])
    links += link(link_0,link_0_url,data['btn_bg'],data['btn_fg'])
    links += link(link_1,link_1_url,data['btn_bg'],data['btn_fg'])
    links += link(link_2,link_2_url,data['btn_bg'],data['btn_fg'])
    links += link(link_3,link_3_url,data['btn_bg'],data['btn_fg'])
    # addresses = address_links(data['address'],data['fg_0'])
    bio = data['bio'].replace('\n','<br>')

    ssl = ''
    if injectSSL:
        ssl = f'<script src="https://{injectSSL}/https.js" async=""></script>'
    page = "page.html"
    html = render_template(page, title=title, links=links, image=image,
                           btn_bg=data['btn_bg'], btn_fg=data['btn_fg'], addresses=ssl, bio=bio)
    if data['image'] != "":
        html = html.replace('/assets/img/favicon.png',f'/avatar/{data["image"]}')
    if data['bg'] != "":
        html = html.replace('/assets/img/default-bg.jpeg',f'/images/{data["bg"]}')
    return html

def gallery(data, injectSSL = False):
    title = data['title']
    image = f'/avatar/{data["image"]}'
    
    ssl = ''
    if injectSSL:
        ssl = f'<script src="https://{injectSSL}/https.js" async=""></script>'
    page = "gallery.html"
    gallery = ''
    print(data['gallery_imgs'])

    for i in range(9):
        if i % 3 == 0: 
            if i != 0:
                gallery += '</div>'
            gallery += '<div class="row" style="margin:auto; margin-bottom: 25px;max-width: 800px; display: flex; justify-content: center;">'

        if str(i) in data['gallery_imgs']:
            gallery += '<div style="margin:5px; padding:0px; border-radius: 10px; background-color: rgba(0, 0, 0, 0.71); display: inline-flex; flex-direction: column; justify-content: center; align-items: center; width: 200px;">'
            gallery += f'<img src="/images/{data["gallery_imgs"][str(i)]}" class="img-fluid" alt="Gallery Image {i}" style="border-radius: 10px;" width=200px height=200px>'
        
            gallery += f'<span style="display: block;text-align: center; margin: 5px;">{data["gallery_desc"][str(i)]}</span>'
            gallery += '</div>'
    
    gallery += '</div>'

    html = render_template(page, title=title, image=image,
                           btn_bg=data['btn_bg'], btn_fg=data['btn_fg'], addresses=ssl, gallery=gallery)
    if data['image'] != "":
        html = html.replace('/assets/img/favicon.png',f'/avatar/{data["image"]}')
    if data['bg'] != "":
        html = html.replace('/assets/img/default-bg.jpeg',f'/images/{data["bg"]}')
    return html


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

def is_closer_to_black(hex_color):
    white = (255, 255, 255)
    black = (0, 0, 0)
    color = hex_to_rgb(hex_color)
    distance_to_white = color_distance(color, white)
    distance_to_black = color_distance(color, black)
    return distance_to_black < distance_to_white

