import asyncio
import aiohttp
import ssl
import itertools
import random
import lxml.html


class ProxyHelper:
    def __init__(self):
        self.proxy_providers = [
            ('https://www.proxy-list.download/api/v1/get?type=http', self._proxy_list_parser_http),
            ('https://www.proxy-list.download/api/v1/get?type=https', self._proxy_list_parser_https),
            ('https://free-proxy-list.net/', self._free_proxy_list_parser)
        ]
        self.proxies = self._init_proxies(self.proxy_providers)

    def get_random(self):
        """
        Returns a random proxy
        :return: a proxy:port string randomised from the list
        """
        return random.choice(self.proxies)

    def get_all(self):
        """
        Returns all the proxies
        :return: the proxy list
        """
        return self.proxies

    def remove(self, proxy_string):
        """
        Removes a proxy from self.proxies, useful to
        :param proxy_string: a string representing the proxy eg. 1.1.1.1:8080
        :return: Boolean True for success
        """
        try:
            self.proxies.remove(proxy_string)
            return True
        except ValueError:
            return False

    def refresh(self):
        """
        Refreshes the proxy list
        """
        self.proxies = self._init_proxies(self.proxy_providers)

    def get_count(self):
        """
        Returns the number of proxies
        :return: length of proxy list
        """
        return len(self.proxies)

    @staticmethod
    def _init_proxies(proxy_providers):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(ProxyHelper._fetch_all_proxy_lists(proxy_providers, loop))

    @staticmethod
    async def _fetch_and_parse(session, url, parser):
        async with session.get(url, ssl=ssl.SSLContext()) as response:
            content = await response.text()
            return await parser(content)

    @staticmethod
    async def _fetch_all_proxy_lists(proxy_providers, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            results = await asyncio.gather(
                *[ProxyHelper._fetch_and_parse(session, url, parser) for url, parser in proxy_providers],
                return_exceptions=True
            )
            return list(set(itertools.chain(*results)))

    @staticmethod
    async def _proxy_list_parser_http(content):
        """
        Parses the content returned from www.proxy-list.download
        :param content: The returned content
        :return: a list of proxies in format eg. 1.1.1.1:8080
        """
        return ['http://%s' % proxy_string for proxy_string in content.split("\r\n") if proxy_string]

    @staticmethod
    async def _proxy_list_parser_https(content):
        """
        Parses the content returned from www.proxy-list.download
        :param content: The returned content
        :return: a list of proxies in format eg. 1.1.1.1:8080
        """
        return ['https://%s' % proxy_string for proxy_string in content.split("\r\n") if proxy_string]

    @staticmethod
    async def _free_proxy_list_parser(content):
        """
        Parses the content returned from www.proxy-list.download
        :param content: The returned content
        :return: a list of proxies in format eg. 1.1.1.1:8080
        """
        page = lxml.html.fromstring(content)
        proxies = []
        for row in page.cssselect('tbody tr'):
            tds = row.cssselect('td')
            if 'yes' in tds[6].text_content():
                proxies.append('https://%s:%s' % (tds[0].text_content(), tds[1].text_content()))
            else:
                proxies.append('http://%s:%s' % (tds[0].text_content(), tds[1].text_content()))

        return proxies
