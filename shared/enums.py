"""Enumerados compartidos"""

from enum import Enum


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

class TableNames(Enum):
    """
    Id de las tablas de las cuales se van a explotar los datos
    """

    RESULTADOS = 'resultados'
    CALENDARIO = 'calendario'
    EQUIPOS = 'equipos'
