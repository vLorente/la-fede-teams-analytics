""" Fede Spider """
from enum import Enum
import scrapy

class Selector(Enum):
    """ 
    Selectores del formulario identificados por el campo "id"
    """
    TEMPORADAS = 'ctl00$contenedor_informacion$DDLTemporadas'
    COMPETICION = 'ctl00$contenedor_informacion$DDLCompeticiones'
    CATEGORIA = 'ctl00$contenedor_informacion$DDLCategorias'
    FASE = 'ctl00$contenedor_informacion$DDLFases'
    GRUPO = 'ctl00$contenedor_informacion$DDLGrupos'

class StaticValues(Enum):
    """ 
    Valores estáticos para los selectores
    """
    COMPETICION = '379' # COMPETICIONES FBRM
    CATEGORIA = '1025' # 2ª Autonómica Masculina
    DEFAULT_VALUE = '1'

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

            print(f'Temporada: {option_text}, Valor: {option_value}')

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

            print(f'Fase: {option_text}, Valor: {option_value}')

            # Configurar el body del nuevo POST
            data = {
                '__EVENTTARGET': Selector.FASE.value,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': view_state_genetator,
                '__EVENTVALIDATION': event_validation,
                # Selector.TEMPORADAS.value: temporada_value,
                # Selector.COMPETICION.value: StaticValues.COMPETICION.value,
                # Selector.CATEGORIA.value: StaticValues.CATEGORIA.value,
                Selector.FASE.value: option_value,
                # Selector.GRUPO.value: '5186'
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

            print(f'Grupo: {option_text}, Valor: {option_value}')

            # Configurar el body del nuevo POST
            data = {
                '__EVENTTARGET': Selector.GRUPO.value,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': view_state_genetator,
                '__EVENTVALIDATION': event_validation,
                # Selector.TEMPORADAS.value: temporada_value,
                # Selector.COMPETICION.value: StaticValues.COMPETICION.value,
                # Selector.CATEGORIA.value: StaticValues.CATEGORIA.value,
                # Selector.FASE.value: fase_value,
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
        temporada_value = response.meta['temporada_value']
        temporada_text = response.meta['temporada_text']
        fase_value = response.meta['fase_value']
        fase_text = response.meta['fase_text']
        grupo_text = response.meta['grupo_text']
        print('\033[91m' + f'Temporada: {temporada_text}, Fase: {fase_text}, Grupo: {grupo_text}' + '\033[0m')
