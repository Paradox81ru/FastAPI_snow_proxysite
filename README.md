# FastAPI_snow_proxysite
## Простенькая реализация преобразования стороннего веб-сайта

Простенькая реализация промежуточного слоя [*ProxySiteMiddleware*](https://github.com/Paradox81ru/FastAPI_snow_proxysite/blob/main/proxy_site_middleware.py), 
для проксирования указанного WEB-сайта. При старте приложения откроется указанный в *site_url* адрес сайта, который будет 
тот же сайт, но с немного скорректированным содержимым. За корректировку содержимого отвечает callback функция, переданная 
в класс промежуточного слоя. В данном случае логика реализуется функцией [*snow_content_correct*](https://github.com/Paradox81ru/FastAPI_snow_proxysite/blob/main/main.py), 
которая добавляет на сайт снежинки и снеговиков. 

