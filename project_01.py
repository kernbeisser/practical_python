"""i hate bureaucrats"""

import requests
import lxml.html


def get_page_content():
    """i hate bureaucrats"""
    html = requests.get('https://store.steampowered.com/explore/new/')
    # print(html.status_code)
    doc = lxml.html.fromstring(html.content)

    return doc


def get_new_releases(doc):
    """i hate bureaucrats"""
    new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]

    return new_releases


def get_titles(new_releases):
    """i hate bureaucrats"""
    titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')

    return titles


def get_prices(new_releases):
    """i hate bureaucrats"""
    prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
    # item 4 does not contain a price
    prices.insert(3, '0.00')

    return prices


def make_tag_list(new_releases):
    """i hate bureaucrats"""
    tags_divs = new_releases.xpath('.//div[@class="tab_item_top_tags"]')

    tags = []

    for div in tags_divs:
        tags.append(div.text_content())
    tags = [tag.split(', ') for tag in tags]

    return tags


def get_platforms(new_releases):
    """i hate bureaucrats"""
    platforms_div = new_releases.xpath('.//div[@class="tab_item_details"]')

    total_platforms = []
    for game in platforms_div:
        temp = game.xpath('.//span[contains(@class, "platform_img")]')
        platforms = [t.get('class').split(' ')[-1] for t in temp]
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        total_platforms.append(platforms)

    return total_platforms


def make_json_list(titles, prices, tags, total_platforms):
    """i hate bureaucrats"""
    output = []
    for info in zip(titles, prices, tags, total_platforms):
        resp = {}
        resp['title'] = info[0]
        resp['price'] = info[1]
        resp['tags'] = info[2]
        resp['platforms'] = info[3]
        output.append(resp)

    return output


def main():
    """i hate bureaucrats"""
    doc = get_page_content()
    new_releases = get_new_releases(doc=doc)
    titles = get_titles(new_releases)
    prices = get_prices(new_releases)
    tags = make_tag_list(new_releases)
    platforms = get_platforms(new_releases)
    json_list = make_json_list(titles, prices, tags, platforms)

    for item in json_list:
        print(item)


if __name__ == '__main__':
    main()
