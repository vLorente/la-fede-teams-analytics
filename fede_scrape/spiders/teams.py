"""Spider Teams"""
import scrapy
from shared.enums import Selector, StaticValues, TableNames
from shared.functions import decode_html_script

class TeamsSpider(scrapy.Spider):
    """Spider for scraping https://www.fbrm.org/temporadas-anteriores
    para obtener la tabla de equipos y su información de cada temporada"""

    name = "teams"
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
            }

            # Realiza la solicitud POST
            yield scrapy.FormRequest(
                url=self.url,
                formdata=data,
                callback=self.parse_regular_fase,
                meta=meta
            )

    def parse_regular_fase(self, response):
        """Parsing obtener el valor de la fase regular de cada temporada"""

        # Extrae el VIEWSTATE y otros campos ocultos
        viewstate = response.css('#__VIEWSTATE::attr(value)').get() or ''
        event_validation = response.css('#__EVENTVALIDATION::attr(value)').get() or ''
        view_state_genetator = response.css('#__VIEWSTATEGENERATOR::attr(value)').get() or ''

        # Extreaer metadata
        temporada_text = response.meta['temporada_text']

        # En este caso sólo se va a evaluar la fase "REGULAR"
        regular_option = response.css(
            f'select[name="{Selector.FASE.value}"] option:contains("REGULAR")')

        regular_option_value = regular_option.css('::attr(value)').get()

        # Configurar el body del nuevo POST
        data = {
            '__EVENTTARGET': Selector.FASE.value,
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': view_state_genetator,
            '__EVENTVALIDATION': event_validation,
            Selector.FASE.value: regular_option_value
        }

        meta = {
            'temporada_text': temporada_text,
        }

        # Realiza la solicitud POST
        yield scrapy.FormRequest(
            url=self.url,
            formdata=data,
            callback=self.parse_groups,
            meta=meta
        )

    def parse_groups(self, response):
        """Parsing para obtener los diferentes grupos de fase regular"""

        # Extrae el VIEWSTATE y otros campos ocultos
        viewstate = response.css('#__VIEWSTATE::attr(value)').get() or ''
        event_validation = response.css('#__EVENTVALIDATION::attr(value)').get() or ''
        view_state_genetator = response.css('#__VIEWSTATEGENERATOR::attr(value)').get() or ''

        # Extreaer metadata
        temporada_text = response.meta['temporada_text']

        # Obtener las opcines del selector de grupos
        options = response.css(f'select[name="{Selector.GRUPO.value}"] option')

        for option in options:
            option_value = option.css('::attr(value)').get()

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
            }

            # Realiza la solicitud POST
            yield scrapy.FormRequest(
                url=self.url,
                formdata=data,
                callback=self.parse_data,
                meta=meta
            )

    def parse_data(self, response):
        """Parsing datos de los equipos de cada temporada"""

        # Extreaer metadata
        temporada_text = response.meta['temporada_text'].strip()

        # Obtener resultados
        resultados = response.css(f'article[id="{TableNames.EQUIPOS.value}"]')
        table = resultados.xpath(
            """.//table[thead/tr/th[text()="Equipo" 
                and following-sibling::th[1][text()="Localidad"]]]""")

        rows = table.css('tbody tr')
        for row in rows:
            # Encuentra el script dentro del artículo que contiene el valor codificado
            team = decode_html_script(row.xpath('.//td[1]//script').get())
            location = decode_html_script(row.xpath('.//td[2]//script').get())
            color_home = decode_html_script(row.xpath('.//td[3]//script').get())
            color_visitor = decode_html_script(row.xpath('.//td[4]//script').get())

            yield {
                'season': temporada_text, 
                'team': team.strip(),
                'location': location.strip(),
                'color_home': color_home.strip(),
                'color_visitor': color_visitor.strip()
            }
