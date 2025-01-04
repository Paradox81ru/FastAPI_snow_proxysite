from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from starlette.types import ASGIApp

import httpx
import re

class ProxySiteMiddleware(BaseHTTPMiddleware):
    """ Класс промежуточного слоя проксирования содержимого сайта """
    def __init__(self, app: ASGIApp, site_url: str, content_correct: callable):
        """
        Конструктор класса
        :param app: Экземпляр FastAPI приложения.
        :param site_url: Доменное имя сайт для проксирования.
        :param content_correct: Функция с логикой изменения содержимого
        """
        super().__init__(app)
        self._site_url = site_url
        self._content_correct = content_correct

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        url_path = request.url.path
        site_path = f"{self._site_url}{url_path}"
        if not self.is_html(request.headers):
            # Менять надо только HTML содержимое.
            response = await call_next(request)
            return response
        else:
            # А ресурсы надо обрабатывать как обычно.
            response = await self._get_site_html(site_path, request)
            return HTMLResponse(response)

    async def _get_site_html(self, url: str, request: Request):
        """ Возвращает HTML содержимое стороннего сайта. """
        async with httpx.AsyncClient() as client:
            response = await client.get(url, cookies=request.cookies) \
                if request.method.lower() == 'get' else await client.post(url, cookies=request.cookies)
            content = response.content.decode()
            content = self._tag_path_corrects(content)
            content = self._content_correct(content)
            return content

    def _content_correct(self, content):
        """ Корректирует HTML содержимое """
        return self._content_correct(content)

    def _script_path_correct(self, html):
        """ Корректирует путь для javascript. """
        pattern = r'<script src="(.*?)">'
        return re.sub(pattern, f'<script src="{self._site_url}/\\g<1>">', html)

    def _stylesheet_path_correct(self, html):
        """ Корректирует путь для CSS. """
        pattern = r'<link rel="stylesheet" href="(?<!https)(.*?)">'
        return re.sub(pattern,f'<link rel="stylesheet" href="{self._site_url}/\\g<1>">', html)

    def _img_path_correct(self, html: str):
        """ Корректирует путь для IMG """
        """ <img class="sponsor-image" src="/img/sponsors/coherence-banner.png" /> """
        pattern = r'<img(\sclass=".*?")? src="(?<!https)(.*?)"\s?/>'
        return re.sub(pattern, f'<img\\g<1> src="{self._site_url}/\\g<2>" />', html)

    def _tag_path_corrects(self, content):
        """ Корректирует пути в тэгах. """
        content = self._script_path_correct(content)
        content = self._stylesheet_path_correct(content)
        content = self._img_path_correct(content)
        return content

    def is_html(self, headers):
        """ Проверка на переданное HTML содержимое """
        accept = headers.get('accept')
        return accept.startswith('text/html')