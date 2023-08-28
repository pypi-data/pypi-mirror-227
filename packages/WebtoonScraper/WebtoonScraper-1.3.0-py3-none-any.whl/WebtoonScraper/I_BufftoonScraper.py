'''Download Webtoons from Bufftoon.'''

from __future__ import annotations
import re
from pathlib import Path
import time
from async_lru import alru_cache
import logging

if __name__ in ("__main__", "I_BufftoonScraper"):
    from C_Scraper import Scraper
else:
    from .C_Scraper import Scraper


class BufftoonScraper(Scraper):
    '''Scrape webtoons from Bufftoon.'''
    def __init__(self, pbar_independent: bool = False, cookie: str = ''):
        super().__init__(pbar_independent)
        self.BASE_URL = 'https://bufftoon.plaync.com'
        self.IS_STABLE_CONNECTION = True
        self.COOKIE: str = cookie

    @alru_cache(maxsize=4)
    async def get_webtoon_data(self, titleid, get_payment: bool = False, get_login_requiered: bool | None = None, limit: int = 500):
        url = f'https://api-bufftoon.plaync.com/v2/series/{titleid}/episodes?sortType=2&offset=0&limit={limit}'
        raw_data = await self.get_internet('requests', url)
        raw_data = raw_data.json()
        subtitles = []
        episode_ids = []
        if get_login_requiered is None:
            get_login_requiered = bool(self.COOKIE)
        for raw_episode in raw_data['result']['episodes']:
            if not get_payment and raw_episode['isPaymentEpisode']:
                logging.warning(f"Episode '{raw_episode['title']}' is not free of charge episode. It won't be downloaded.")
                continue
            if not get_login_requiered and not raw_episode['isOpenFreeEpisode']:
                logging.warning(f"Episode '{raw_episode['title']}' is not opened for non-login users. It'll be not downloaded.")
                continue
            episode_no = raw_episode['episodeOrder']
            raw_episode_id = raw_episode['listImgPath']
            episode_id = int(re.search(rf'(?<=contents\/.\/{titleid}\/)(\d+)(?=\/)', raw_episode_id)[0])
            episode_ids.append(episode_id)
            subtitles.append(raw_episode['title'])
        return {'subtitles': subtitles, 'episode_ids': episode_ids}

    async def get_title(self, titleid):
        url = f'https://bufftoon.plaync.com/series/{titleid}'
        title = await self.get_internet(get_type='noNone_select_one', url=url,
                                        selector='#content > div > div > div.series-info > div.cont > div.title')
        return title.text.strip()

    async def save_webtoon_thumbnail(self, titleid, title, thumbnail_dir):
        url = f'https://bufftoon.plaync.com/series/{titleid}'
        image_url_original = await self.get_internet(get_type='noNone_select_one', url=url,
                                                     selector='#content > div > div > div.series-info > div.img')
        image_url = image_url_original['style']
        image_url = re.search(r'(?<=background-image:url\().+(?=\);)', image_url)[0]
        image_extension = self.get_file_extension(image_url)
        image_raw = await self.get_internet(get_type='requests', url=image_url)
        image_raw = image_raw.content
        Path(f'{thumbnail_dir}/{title}.{image_extension}').write_bytes(image_raw)

    async def get_all_episode_no(self, titleid):
        return await super().get_all_episode_no(titleid)

    async def get_subtitle(self, titleid, episode_no, sleep=True):
        if sleep:
            time.sleep(1)
        return await super().get_subtitle(titleid, episode_no)

    async def get_episode_images_url(self, titleid, episode_no):
        HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': self.COOKIE,
            'Dnt': '1',
            'Host': 'bufftoon.plaync.com',
            'If-None-Match': '"3a315-EG2ELuRZJEgvGHGM2DBBGcLckb4"',
            'Referer': f'https://bufftoon.plaync.com/series/{titleid}',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-Gpc': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        }
        episode_id = await self.episode_no_to_episode_id(titleid, episode_no)
        url = f'{self.BASE_URL}/series/{titleid}/{episode_id}'
        selector = '#content > div > div > div.viewer-wrapper > div > img'
        episode_images_url = await self.get_internet(get_type='soup_select', url=url,
                                                     selector=selector, headers=HEADERS)

        return [element['src'] for element in episode_images_url]

    async def download_single_image(self, episode_dir: Path, url: str, image_no: int) -> None:
        await super().download_single_image(episode_dir, url, image_no, 'png')


if __name__ == '__main__':
    wt = BufftoonScraper()
    wt.download_one_webtoon(1007888)  # 겜덕툰
