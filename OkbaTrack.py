#!/usr/bin/env python3
# << CODE BY OKBA

import json
import time
import os
import sys
import re
import socket
import subprocess
from sys import stderr
from urllib.parse import urljoin

REQUIRED = ['requests', 'phonenumbers']

for pkg in REQUIRED:
    try:
        __import__(pkg.replace('-', '_'))
    except ImportError:
        print(f' ⏳ Installing {pkg}...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'
Rst = '\033[0m'

SEP = f'{Wh}├{"─"*48}┤{Rst}'
SEP_T = f'{Wh}┌{"─"*48}┐{Rst}'
SEP_B = f'{Wh}└{"─"*48}┘{Rst}'


def is_option(func):
    def wrapper(*args, **kwargs):
        banner_sub()
        func(*args, **kwargs)
    return wrapper


def show_result(title, data):
    print(f'\n{SEP_T}')
    print(f'{Wh}│ {Cy}{title:<46}{Wh}│{Rst}')
    print(SEP)
    for label, value in data:
        print(f'{Wh}│ {Gr}{label:<20}{Wh}: {Cy}{value}{Rst}')
    print(SEP_B)


@is_option
def IP_Track():
    ip = input(f'\n {Cy}🎯{Wh} Enter IP target {Gr}→{Rst} ').strip()
    if not ip:
        print(f' {Re}✖ No input{Rst}')
        return
    try:
        req = requests.get(f'http://ipwho.is/{ip}', timeout=10)
        d = json.loads(req.text)
    except Exception as e:
        print(f' {Re}✖ API error: {e}{Rst}')
        return

    lat = int(float(d.get('latitude', 0)))
    lon = int(float(d.get('longitude', 0)))
    conn = d.get('connection', {})
    tz = d.get('timezone', {})
    flag = d.get('flag', {})

    show_result('🌐 IP GEOLOCATION', [
        ('IP', d.get('ip', 'N/A')),
        ('Type', d.get('type', 'N/A')),
        ('Continent', d.get('continent', 'N/A')),
        ('Country', f'{flag.get("emoji", "")} {d.get("country", "N/A")}'),
        ('Country Code', d.get('country_code', 'N/A')),
        ('Region', d.get('region', 'N/A')),
        ('City', d.get('city', 'N/A')),
        ('Lat / Lon', f'{d.get("latitude", "N/A")}, {d.get("longitude", "N/A")}'),
        ('Maps', f'https://google.com/maps/@{lat},{lon},8z'),
        ('Postal', d.get('postal', 'N/A')),
        ('Calling Code', d.get('calling_code', 'N/A')),
        ('Capital', d.get('capital', 'N/A')),
        ('ASN', conn.get('asn', 'N/A')),
        ('ISP', conn.get('isp', 'N/A')),
        ('ORG', conn.get('org', 'N/A')),
        ('Domain', conn.get('domain', 'N/A')),
        ('Timezone', tz.get('id', 'N/A')),
        ('UTC', tz.get('utc', 'N/A')),
        ('Current Time', tz.get('current_time', 'N/A')),
    ])


@is_option
def phoneGW():
    raw = input(f'\n {Cy}📱{Wh} Phone number {Gr}→{Rst} e.g. +213600000000\n {"":>18}').strip()
    if not raw:
        print(f' {Re}✖ No input{Rst}')
        return
    try:
        p = phonenumbers.parse(raw, 'ID')
    except:
        print(f' {Re}✖ Invalid phone number{Rst}')
        return

    rcode = phonenumbers.region_code_for_number(p)
    provider = carrier.name_for_number(p, 'en')
    loc = geocoder.description_for_number(p, 'id')
    tzs = ', '.join(timezone.time_zones_for_number(p))
    ntype = phonenumbers.number_type(p)

    if ntype == phonenumbers.PhoneNumberType.MOBILE:
        typ = '📱 Mobile'
    elif ntype == phonenumbers.PhoneNumberType.FIXED_LINE:
        typ = '☎️ Fixed Line'
    else:
        typ = '❓ Other'

    show_result('📞 PHONE INFO', [
        ('Number', raw),
        ('International', phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.INTERNATIONAL)),
        ('E.164', phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)),
        ('Location', loc or 'N/A'),
        ('Region Code', rcode),
        ('Timezone', tzs),
        ('Operator', provider or 'N/A'),
        ('Type', typ),
        ('Valid', '✅ Yes' if phonenumbers.is_valid_number(p) else '❌ No'),
        ('Possible', '✅ Yes' if phonenumbers.is_possible_number(p) else '❌ No'),
    ])


@is_option
def TrackLu():
    username = input(f'\n {Cy}👤{Wh} Username {Gr}→{Rst} ').strip()
    if not username:
        print(f' {Re}✖ No input{Rst}')
        return

    sites = [
        ('https://www.facebook.com/{}', 'Facebook', 'fb'),
        ('https://www.twitter.com/{}', 'Twitter', 'tw'),
        ('https://www.instagram.com/{}', 'Instagram', 'ig'),
        ('https://www.linkedin.com/in/{}', 'LinkedIn', 'in'),
        ('https://www.github.com/{}', 'GitHub', 'gh'),
        ('https://www.tiktok.com/@{}', 'TikTok', 'tt'),
        ('https://www.youtube.com/{}', 'Youtube', 'yt'),
        ('https://www.twitch.tv/{}', 'Twitch', 'twitch'),
        ('https://www.snapchat.com/add/{}', 'Snapchat', 'snap'),
        ('https://www.telegram.me/{}', 'Telegram', 'tg'),
        ('https://www.pinterest.com/{}', 'Pinterest', 'pin'),
        ('https://www.tumblr.com/{}', 'Tumblr', 'tum'),
        ('https://www.behance.net/{}', 'Behance', 'bh'),
        ('https://www.medium.com/@{}', 'Medium', 'md'),
        ('https://www.quora.com/profile/{}', 'Quora', 'qu'),
        ('https://www.flickr.com/people/{}', 'Flickr', 'fl'),
        ('https://www.dribbble.com/{}', 'Dribbble', 'dr'),
        ('https://soundcloud.com/{}', 'SoundCloud', 'sc'),
        ('https://www.producthunt.com/@{}', 'Product Hunt', 'ph'),
    ]

    results = []
    for url_tpl, name, _ in sites:
        url = url_tpl.format(username)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                status = f'{Gr}✅ Found{Rst}'
                link = f'{Cy}{url}{Rst}'
            else:
                status = f'{Re}❌ Not found{Rst}'
                link = ''
        except:
            status = f'{Ye}⚠️ Error{Rst}'
            link = ''
        results.append((name, status, link))

    print()
    print(SEP_T)
    print(f'{Wh}│ {Cy}👤 USERNAME SCAN — @{username:<31}{Wh}│{Rst}')
    print(SEP)
    for name, status, link in results:
        label = f'{name:<20}'
        if link:
            print(f'{Wh}│ {Gr}{label}{Wh}: {status}')
            print(f'{Wh}│ {"":>22}{link}')
        else:
            print(f'{Wh}│ {Gr}{label}{Wh}: {status}')
    print(SEP_B)


@is_option
def showIP():
    try:
        myip = requests.get('https://api.ipify.org/', timeout=5).text.strip()
    except:
        print(f' {Re}✖ Could not fetch IP{Rst}')
        return
    show_result('ℹ️ YOUR IP', [
        ('Public IP', myip),
    ])


META_RE = re.compile(
    r'<meta\s+http-equiv=["\']?refresh["\']?\s+content=["\']?(\d*);\s*url=([^"\' >]+)',
    re.IGNORECASE
)
JS_RE = re.compile(
    r'(?:window\.)?(?:location|document\.location)[\s.]*?(?:href)?\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE
)


def _follow_meta(url, session, depth=0, max_depth=5, seen=None):
    if seen is None:
        seen = set()
    if url in seen or depth >= max_depth:
        return url
    seen.add(url)
    try:
        r = session.get(url, timeout=15, stream=True)
        r.close()
    except:
        return url

    content_type = r.headers.get('Content-Type', '')
    if 'html' not in content_type:
        return url

    body = r.text

    m = META_RE.search(body)
    if m:
        _, target = m.groups()
        if not target.startswith('http'):
            target = urljoin(url, target)
        return _follow_meta(target, session, depth + 1, max_depth, seen)

    j = JS_RE.search(body)
    if j:
        target = j.group(1)
        if not target.startswith('http'):
            target = urljoin(url, target)
        return _follow_meta(target, session, depth + 1, max_depth, seen)

    return url


@is_option
def expandURL():
    raw = input(f'\n {Cy}🔗{Wh} Short URLs (space/comma/newline separated) {Gr}→{Rst} ').strip()
    if not raw:
        print(f' {Re}✖ No input{Rst}')
        return

    urls = []
    for sep in (',', '\n', ' '):
        if sep in raw:
            urls = [u.strip() for u in raw.replace(',', '\n').split('\n') if u.strip()]
            break
    if not urls:
        urls = [raw]

    session = requests.Session()
    session.max_redirects = 30

    for idx, short in enumerate(urls, 1):
        if not short.startswith('http'):
            short = 'https://' + short
        try:
            r = session.get(short, timeout=15, stream=True)
            r.close()
        except requests.exceptions.TooManyRedirects:
            print(f'\n {Re}✖ [{idx}] Too many redirects (loop?) — {short}{Rst}')
            continue
        except Exception as e:
            print(f'\n {Re}✖ [{idx}] Error expanding: {short} — {e}{Rst}')
            continue

        data = [('Original', short)]
        total = len(r.history)
        if total > 0:
            for i, hop in enumerate(r.history, 1):
                location = hop.headers.get('Location', hop.url)
                data.append((f'  ➜ HTTP {i}', f'{hop.status_code} {location}'))

        body = r.text[:5000] if 'html' in r.headers.get('Content-Type', '') else ''
        meta_chain = []
        if META_RE.search(body) or JS_RE.search(body):
            resolved = _follow_meta(r.url, session)
            if resolved != r.url:
                meta_chain.append(resolved)

        if meta_chain:
            data.append(('  ➜ Meta', meta_chain[0]))
            data.append(('➜ Final', meta_chain[0]))
        else:
            data.append(('➜ Final', r.url))

        data.append(('Status', f'{r.status_code} {"✅" if r.status_code == 200 else "⚠️"}'))
        extra = total + len(meta_chain)
        data.append(('Total Hops', str(extra)))

        show_result(f'🔗 URL EXPAND #{idx}', data)


TOR_LIST_URL = 'https://check.torproject.org/torbulkexitlist'


def _fetch_tor_list():
    try:
        r = requests.get(TOR_LIST_URL, timeout=10)
        return set(r.text.strip().split('\n'))
    except:
        return set()


_tor_exit_nodes = None


def _is_tor(ip):
    global _tor_exit_nodes
    if _tor_exit_nodes is None:
        _tor_exit_nodes = _fetch_tor_list()
    return ip in _tor_exit_nodes


@is_option
def vpnCheck():
    ip = input(f'\n {Cy}🛡️{Wh} IP to check {Gr}→{Rst} ').strip()
    if not ip:
        print(f' {Re}✖ No input{Rst}')
        return

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=status,message,query,proxy,hosting,mobile,isp,org,as,country,city', timeout=10)
        d = r.json()
    except Exception as e:
        print(f' {Re}✖ API error: {e}{Rst}')
        return

    if d.get('status') == 'fail':
        print(f' {Re}✖ {d.get("message", "Invalid IP")}{Rst}')
        return

    is_proxy = d.get('proxy', False)
    is_hosting = d.get('hosting', False)
    is_mobile = d.get('mobile', False)
    is_tor = _is_tor(ip)

    if is_tor:
        verdict = f'{Re}🔴 Tor Exit Node{Rst}'
    elif is_proxy and is_hosting:
        verdict = f'{Ye}🟡 VPN / Hosting{Rst}'
    elif is_proxy:
        verdict = f'{Ye}🟡 Proxy Detected{Rst}'
    elif is_hosting:
        verdict = f'{Ye}🟡 Hosting/VPS{Rst}'
    else:
        verdict = f'{Gr}🟢 Clean (Residential){Rst}'

    tags = []
    if is_tor: tags.append('Tor')
    if is_proxy: tags.append('Proxy')
    if is_hosting: tags.append('Hosting')
    if is_mobile: tags.append('Mobile')

    show_result(f'🛡️ VPN / PROXY CHECK', [
        ('IP', d.get('query', 'N/A')),
        ('Verdict', verdict),
        ('Tags', ', '.join(tags) if tags else 'None (Residential)'),
        ('Country', d.get('country', 'N/A')),
        ('City', d.get('city', 'N/A')),
        ('ISP', d.get('isp', 'N/A')),
        ('ORG', d.get('org', 'N/A')),
        ('AS', d.get('as', 'N/A')),
    ])


@is_option
def dnsLookup():
    ip = input(f'\n {Cy}📡{Wh} IP or domain {Gr}→{Rst} ').strip()
    if not ip:
        print(f' {Re}✖ No input{Rst}')
        return

    data = [('Target', ip)]

    ptr = None
    try:
        ptr = socket.gethostbyaddr(ip)
        data.append(('PTR / Hostname', ptr[0]))
    except:
        data.append(('PTR / Hostname', f'{Ye}None{Rst}'))

    if ptr:
        aliases = ptr[1]
        if aliases:
            data.append(('Aliases', ', '.join(aliases)))
        try:
            addrs = socket.getaddrinfo(ptr[0], 0)
            ips = list(dict.fromkeys(a[4][0] for a in addrs))
            data.append(('Resolves To', ', '.join(ips)))
        except:
            pass

    try:
        addrs = socket.getaddrinfo(ip, 0)
        ips = list(dict.fromkeys(a[4][0] for a in addrs))
        if len(ips) > 1:
            data.append(('A Records', ', '.join(ips)))
    except:
        pass

    data.append(('More Info', f'{Cy}https://viewdns.info/reverseip/?t=1&host={ip}{Rst}'))

    show_result('📡 IP HISTORY / REVERSE DNS', data)


options = [
    {'num': 1, 'text': '🌐  IP Tracker', 'func': IP_Track},
    {'num': 2, 'text': 'ℹ️   My IP', 'func': showIP},
    {'num': 3, 'text': '📱  Phone Lookup', 'func': phoneGW},
    {'num': 4, 'text': '👤  Username Scan', 'func': TrackLu},
    {'num': 5, 'text': '🔗  URL Expander', 'func': expandURL},
    {'num': 6, 'text': '🛡️  VPN/Proxy Check', 'func': vpnCheck},
    {'num': 7, 'text': '📡  Reverse DNS', 'func': dnsLookup},
    {'num': 0, 'text': '🚪  Exit', 'func': exit},
]


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def call_option(opt):
    for o in options:
        if o['num'] == opt:
            o['func']()
            return
    raise ValueError('Option not found')


def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}├{"─"*48}┤\n│ {Gr}Press Enter to continue  🔄{Rst}')
        main()
    except ValueError:
        print(f' {Re}✖ Invalid option{Rst}')
        time.sleep(1.5)
        main()
    except KeyboardInterrupt:
        print(f'\n {Ye}👋 Bye!{Rst}')
        time.sleep(1)
        exit()


def show_menu():
    print(f'\n{Wh}┌{"─"*48}┐')
    for o in options:
        side = '│' if o['num'] != 0 else '└'
        end = '┤' if o['num'] != 0 else '┘'
        print(f'{Wh}{side}   {Cy}{o["num"]}{Wh}. {Gr}{o["text"]:<38}{Wh}{end}')
    print()


def banner_main():
    clear()
    stderr.writelines(f"""{Wh}
   ╔══════════════════════════════════════════╗
   ║   {Gr}██████╗ ██╗  ██╗██████╗  █████╗ {Wh}   ║
   ║   {Gr}██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗{Wh}   ║
   ║   {Gr}██████╔╝█████╔╝ ██████╔╝███████║{Wh}   ║
   ║   {Gr}██╔══██╗██╔═██╗ ██╔══██╗██╔══██║{Wh}   ║
   ║   {Gr}██████╔╝██║ ██╗██████╔╝██║  ██║{Wh}   ║
   ║   {Gr}╚═════╝ ╚═╝ ╚═╝╚═════╝ ╚═╝  ╚═╝{Wh}   ║
   ║                                      ║
   ║   {Cy}🔍  O K B A T R A C K   V 1.0{Wh}   ║
   ║         {Gr}code by okba{Wh}               ║
   ╚══════════════════════════════════════════╝
{Rst}""")


def banner_sub():
    clear()
    stderr.writelines(f"""{Wh}
   ╔══════════════════════════════════════════╗
   ║    {Gr}██╗  ██╗ █████╗  ██████╗██╗  ██╗{Wh}   ║
   ║    {Gr}██║  ██║██╔══██╗██╔════╝██║ ██╔╝{Wh}   ║
   ║    {Gr}███████║███████║██║     █████╔╝ {Wh}   ║
   ║    {Gr}██╔══██║██╔══██║██║     ██╔═██╗ {Wh}   ║
   ║    {Gr}██║  ██║██║  ██║╚██████╗██║  ██╗{Wh}   ║
   ║    {Gr}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{Wh}   ║
   ║                                      ║
   ║    {Cy}⚡ O K B A T R A C K   V 1.0{Wh}    ║
   ║         {Gr}@code by okba{Wh}               ║
   ╚══════════════════════════════════════════╝
{Rst}""")
    time.sleep(0.8)


def main():
    clear()
    banner_main()
    show_menu()
    time.sleep(0.5)
    try:
        opt = int(input(f' {Cy}⚡{Wh} Select option {Gr}→{Rst} '))
        execute_option(opt)
    except ValueError:
        print(f' {Re}✖ Enter a number!{Rst}')
        time.sleep(1.5)
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n {Ye}👋 Bye!{Rst}')
        time.sleep(1)
        exit()
