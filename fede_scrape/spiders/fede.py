""" Fede Spider """
import scrapy
from shared.enums import Selector, StaticValues, TableNames

class FedeSpider(scrapy.Spider):
    """Spider for scraping https://www.fbrm.org/temporadas-anteriores"""

    name = "fede"
    allowed_domains = ["www.fbrm.org"]
    start_urls = ["https://www.fbrm.org/temporadas-anteriores"]
    url = 'https://www.fbrm.org/temporadas-anteriores'



    def parse(self, response, **kwargs):
        """Parsing de la primera llamada a FBRM."""
        # Extrae el VIEWSTATE y otros campos ocultos
        viewstate = response.css('#__VIEWSTATE::attr(value)').get() or ''
        event_validation = response.css('#__EVENTVALIDATION::attr(value)').get() or ''
        view_state_genetator = response.css('#__VIEWSTATEGENERATOR::attr(value)').get() or ''

        # Extrae todas las opciones del selector de Temporada
        options = response.css(f'select[name="{Selector.TEMPORADAS.value}"] option')

        # Valores y etiquetas
        for option in options:
            option_value = option.css('::attr(value)').get()
            option_text = option.css('::text').get()

            # Configurar el body del nuevo POST
            data = {
                '__EVENTTARGET': Selector.TEMPORADAS.value,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': view_state_genetator,
                '__EVENTVALIDATION': event_validation,
                Selector.TEMPORADAS.value: option_value,
                Selector.COMPETICION.value: StaticValues.COMPETICION.value,
                Selector.CATEGORIA.value: StaticValues.CATEGORIA.value,
            }

            meta = {
                'temporada_text': option_text,
                'temporada_value': option_value
            }

            # Realiza la solicitud POST
            yield scrapy.FormRequest(
                url=self.url,
                formdata=data,
                callback=self.parse_fases,
                meta=meta
            )

    def parse_fases(self, response):
        """
        Parsing de la segunda llamada a FBRM.
        Obtención dinámica de las posibles fases.
        """
        # Extrae el VIEWSTATE y otros campos ocultos
        viewstate = response.css('#__VIEWSTATE::attr(value)').get() or ''
        event_validation = response.css('#__EVENTVALIDATION::attr(value)').get() or ''
        view_state_genetator = response.css('#__VIEWSTATEGENERATOR::attr(value)').get() or ''

        # Extrae metadata
        temporada_value = response.meta['temporada_value']
        temporada_text = response.meta['temporada_text']

        # Extrae todas las opciones del selector de Temporada
        options = response.css(f'select[name="{Selector.FASE.value}"] option')

        # Valores y etiquetas
        for option in options:
            option_value = option.css('::attr(value)').get()
            option_text = option.css('::text').get()

            # Configurar el body del nuevo POST
            data = {
                '__EVENTTARGET': Selector.FASE.value,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': view_state_genetator,
                '__EVENTVALIDATION': event_validation,
                Selector.FASE.value: option_value,
            }

            meta = {
                'temporada_text': temporada_text,
                'temporada_value': temporada_value,
                'fase_text': option_text,
                'fase_value': option_value
            }

            # Realiza la solicitud POST
            yield scrapy.FormRequest(
                url=self.url,
                formdata=data,
                callback=self.parse_grupos,
                meta=meta
            )


    def parse_grupos(self, response):
        """
        Parsing de la tercera llamada a FBRM.
        Obtención dinámica de los posibles grupos.
        """

        # Extrae el VIEWSTATE y otros campos ocultos
        viewstate = response.css('#__VIEWSTATE::attr(value)').get() or ''
        event_validation = response.css('#__EVENTVALIDATION::attr(value)').get() or ''
        view_state_genetator = response.css('#__VIEWSTATEGENERATOR::attr(value)').get() or ''

        # Extrae metadata
        temporada_value = response.meta['temporada_value']
        temporada_text = response.meta['temporada_text']
        fase_value = response.meta['fase_value']
        fase_text = response.meta['fase_text']

        # Extrae todas las opciones del selector de Temporada
        options = response.css(f'select[name="{Selector.GRUPO.value}"] option')

        # Valores y etiquetas
        for option in options:
            option_value = option.css('::attr(value)').get()
            option_text = option.css('::text').get()

            # Configurar el body del nuevo POST
            data = {
                '__EVENTTARGET': Selector.GRUPO.value,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': view_state_genetator,
                '__EVENTVALIDATION': event_validation,
                Selector.GRUPO.value: option_value
            }

            meta = {
                'temporada_text': temporada_text,
                'temporada_value': temporada_value,
                'fase_text': fase_text,
                'fase_value': fase_value,
                'grupo_text': option_text,
                'grupo_value': option_value
            }

            # Realiza la solicitud POST
            yield scrapy.FormRequest(
                url=self.url,
                formdata=data,
                callback=self.parse_data,
                meta=meta
            )

    def parse_data(self, response):
        """
        Parsing de la ultima llamada a FBRM.
        Obtención y almacenamiento de los datos.
        """

        # Extrae metadata
        temporada_text = response.meta['temporada_text']
        fase_text = response.meta['fase_text']
        grupo_text = response.meta['grupo_text']

        # Obtener tablas de datos
        resultados = response.css(f'article[id="{TableNames.RESULTADOS.value}"]')
        calendario = response.css(f'article[id="{TableNames.CALENDARIO.value}"]')
        equipos = response.css(f'article[id="{TableNames.EQUIPOS.value}"]')

        print(resultados)
        print(calendario)
        print(equipos)

        yield {
            'temporada': temporada_text,
            'fase': fase_text,
            'grupo': grupo_text,
        }

