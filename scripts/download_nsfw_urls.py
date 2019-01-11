import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.pornhub.com'


def get_albums_urls_from_keyword(keyword, max_page_num=30):
    album_urls = []
    for page_num in range(1, max_page_num + 1):
        search_url = f'{BASE_URL}/albums?search={keyword}&page={page_num}'
        html = requests.get(search_url).text
        bs_data = BeautifulSoup(html, "lxml")
        album_divs = bs_data.find_all("div", {"class": "photoAlbumListBlock"})

        for div in album_divs:
            try:
                album_url = div.find_all("a", href=True)[0].attrs["href"]
                album_urls.append(f'{BASE_URL}{album_url}')
            except Exception as e:
                print(e)
    return album_urls


def get_preview_urls_from_album_url(album_url):
    html = requests.get(album_url).text
    bs_data = BeautifulSoup(html, "lxml")
    preview_divs = bs_data.find_all("div", {"class": "photoAlbumListBlock"})
    preview_urls = []
    for preview_div in preview_divs:
        short_preview_url = preview_div.find_all("a", href=True)[0].attrs["href"]
        preview_urls.append(f'{BASE_URL}{short_preview_url}')
    return preview_urls


def get_image_url_from_preview_url(preview_url):
    html = requests.get(preview_url).text
    bs_data = BeautifulSoup(html, "lxml")
    try:
        center_img_div = bs_data.find_all("div", {"class": "centerImage"})[1]
    except Exception as e:
        print(f"Couldn't get image url from preview url {preview_url}:\n{str(e)}")
        return None
    image_url = center_img_div.find_all("a", href=True)[-1].find_all("img")[0]['src']
    return image_url


def print_image_urls_from_keyword(keyword, out_file, jpg_only=True, max_page_num=30):
    album_urls = get_albums_urls_from_keyword(keyword, max_page_num)
    if len(album_urls) > 0:
        for album_url in album_urls:
            preview_urls = get_preview_urls_from_album_url(album_url)
            if len(preview_urls) > 0:
                for preview_url in preview_urls:
                    if len(preview_urls) > 0:
                        image_url = get_image_url_from_preview_url(preview_url)
                        if image_url is not None:
                            if (jpg_only and image_url.endswith('.jpg')) or (not jpg_only):
                                with open(out_file, "a") as f:
                                    f.write(image_url + "\n")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-k", "--keyword", dest="keyword", help="search keyword", required=True)
    parser.add_argument("-o", "--out_file", dest="out_file", help="output filepath", required=True)
    parser.add_argument("-j", "--jpg_only", dest="jpg_only", help="download jpg only", default=True)
    parser.add_argument("-p", "--page_num", dest="page_num", help="maximum number of page to parse", default=30)
    args = parser.parse_args()
    print_image_urls_from_keyword(keyword=args.keyword, out_file=args.out_file,
                                  jpg_only=bool(args.jpg_only), max_page_num=int(args.page_num))
