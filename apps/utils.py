import base64
import binascii
import hashlib
import hmac
import os
import random
import string

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage
from urllib.parse import urlencode, urlparse,  urlunparse, parse_qs


Account = get_user_model()


def random_string_gen(size=10, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def unique_slug_gen(title, instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{random_string_gen(size=4)}'
        return unique_slug_gen(title, instance, new_slug=new_slug)
    return slug


def encrypt_data(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decrypt_data(data):
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')


def compute_appsecret_proof(secret, token):
    # Generate an appsecret_proof parameter to secure the Graph API call
    # see https://developers.facebook.com/docs/graph-api/securing-requests
    msg = token.encode("utf-8")
    key = secret.encode("utf-8")
    appsecret_proof = hmac.new(key, msg, digestmod=hashlib.sha256).hexdigest()
    return appsecret_proof


def generate_unique_username(username):
    digits = list(string.digits)
    random.shuffle(digits)
    if not Account.objects.filter(username=username).exists():
        return username

    if Account.objects.filter(username=username).exists():
        random.shuffle(digits)
        return generate_unique_username(username + ''.join(digits[0:2]))


def k_number(number):
    if number < 100:
        return number
    num = number/1000
    num = int(num) if str(num).split('.')[1] == str(0) else round(num, 1)
    return f'{k_number}K'


def round_rate(rate):
    if rate:
        return round(rate)
    return 0


def generate_token(size):
    strings = list(string.ascii_letters)
    random.shuffle(strings)
    altchars = str.encode(''.join(strings[0:2]))
    encoded = binascii.b2a_base64(os.urandom(size))[:-1]
    return encoded.translate(bytes.maketrans(b'+/', altchars)).decode()


def unique_wallet_id(instance):
    chars = list(string.digits) + list(string.ascii_uppercase)
    random.shuffle(chars)
    wallet_id = 'WAL-' + ''.join(chars[0:8])

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(walletID=wallet_id).exists()

    if not qs_exists and len(wallet_id) == 12:
        return wallet_id

    return unique_wallet_id(instance)


def split_query(query, reverse=False):
    result = []
    query_words = query.split()

    if reverse:
        query_words = query_words[::-1]

    length = len(query_words)

    for i in range(length):
        try:
            k = 0
            while k < length:
                if len(query_words[i + 1:length-k]) == 0:
                    k = length
                    result.append(f'{query_words[i]} {query_words[length-0]}')
                else:
                    words = ' '.join(query_words[i + 1:length-k])
                    result.append(f'{query_words[i]} {words}')
                    k += 1

        except IndexError:
            result.append(f'{query_words[0]} {query_words[length - 1]}')

    return list(set(query_words + result + [' '.join(query_words)]))


def paginate(objects, current_url, items_per_page, current_page = 1):
    links = []
    p = Paginator(objects, items_per_page)
    page_number = int(current_page)
    url = parse_url(current_url)

    try:
        page_obj = p.page(page_number)
        objs = page_obj.object_list

    except EmptyPage:
        page_obj = None
        objs = []
        links = []

    if page_obj:
        if page_obj.has_previous():
            prev_page = page_obj.previous_page_number()
            links.append(
                {
                    'label': '« Previous',
                    'url': f'{url}?page={prev_page}' if '?' not in url else f'{url}&page={prev_page}',
                }
            )

        for i in p.page_range:
            active = False
            if i == page_number:
                active = True

            links.append(
                {
                    'label': i,
                    'url': f'{url}?page={i}' if '?' not in url else f'{url}&page={i}',
                    'active': active
                }
            )

        if page_obj.has_next():
            next_page = page_obj.next_page_number()
            links.append(
                {
                    'label': 'Next »',
                    'url': f'{url}?page={next_page}' if '?' not in url else f'{url}&page={next_page}',
                }
            )
    return objs, links


def parse_url(url):
    u = urlparse(url)
    query = parse_qs(u.query, keep_blank_values=True)
    query.pop('page', None)
    u = u._replace(query=urlencode(query, True))
    return urlunparse(u)


