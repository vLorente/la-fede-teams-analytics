""" Spider Results """
import scrapy
from shared.enums import Selector, StaticValues, TableNames
from shared.functions import decode_html_script

class ResultsSpider(scrapy.Spider):
    """Spider for scraping https://www.fbrm.org/temporadas-anteriores
    para obtener la tabla de resultados de cada temporada, fase y grupo"""

    name = "results"
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
                'fase_text': option_text,
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
        temporada_text = response.meta['temporada_text']
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
                'fase_text': fase_text,
                'grupo_text': option_text,
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

        # Obtener resultados
        resultados = response.css(f'article[id="{TableNames.RESULTADOS.value}"]')
        table = resultados.xpath(
            './/table[thead/tr/th[text()="N°" and following-sibling::th[1][text()="Nombre"]]]')

        rows = table.css('tbody tr')
        for row in rows:
            # Encuentra el script dentro del artículo que contiene el valor codificado
            position = decode_html_script(row.xpath('.//td[1]/script').get())
            team = decode_html_script(row.xpath('.//td[2]//script').get())
            matches_played = decode_html_script(row.xpath('.//td[3]//script').get())
            win = decode_html_script(row.xpath('.//td[4]//script').get())
            lose = decode_html_script(row.xpath('.//td[5]//script').get())
            scored = decode_html_script(row.xpath('.//td[6]//script').get())
            against = decode_html_script(row.xpath('.//td[7]//script').get())
            points = decode_html_script(row.xpath('.//td[8]//script').get())

            yield {
                'season': response.meta['temporada_text'].strip(), 
                'phase': response.meta['fase_text'].strip(),
                'group': response.meta['grupo_text'].strip(),
                'position': position, # Posición en la clasificación
                'team': team.strip(),
                'matches_played': matches_played, # Partidos totales
                'win': win, # Victorias
                'lose': lose, # Derrotas
                'scored': scored, # Puntos a favor
                'against': against, # Puntos en contra
                'points': points # Puntos en la clasificación             
            }
