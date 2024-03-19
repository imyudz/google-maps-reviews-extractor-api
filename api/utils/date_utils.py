from datetime import datetime, timedelta
from typing import List

def calcular_data(atraso: str) -> datetime:
    """
    Calcula a data a partir de um atraso especificado em linguagem natural.

    Args:
        atraso (str): Atraso em linguagem natural, como "3 dias atrás" ou "1 mês atrás".

    Returns:
        datetime: Data atrasada.

    Raises:
        ValueError: Se a unidade de tempo não for suportada.
    """

    hoje: datetime = datetime.now()

    quantidade: int
    unidade: str

    quantidade, unidade = _extrair_tempo(atraso)

    try:
        data_atrasada = _calcular_data_atrasada(hoje, quantidade, unidade)
    except ValueError as e:
        raise ValueError("Unidade de tempo não suportada") from e

    return data_atrasada

def _extrair_tempo(atraso: str) -> tuple[int, str]:
    """
    Extrai a quantidade e a unidade de tempo de uma string.

    Args:
        atraso (str): Atraso em linguagem natural, como "3 dias atrás" ou "1 mês atrás".

    Returns:
        tuple: Tupla com a quantidade (int) e a unidade (str) de tempo.
    """

    partes: List[str] = atraso.split()

    if len(partes) == 3:  # Se o tempo estiver em extenso
        quantidade = _tratar_um(partes[0])
        unidade = partes[1].lower()
    else:  # Se o tempo estiver em formato padrão
        quantidade = int(partes[0])
        unidade = partes[1].lower()

    return quantidade, unidade

def _calcular_data_atrasada(hoje: datetime, quantidade: int, unidade: str) -> datetime:
    """
    Calcula a data atrasada a partir da data atual, quantidade e unidade de tempo.

    Args:
        hoje (datetime): Data atual.
        quantidade (int): Quantidade de tempo.
        unidade (str): Unidade de tempo.

    Returns:
        datetime: Data atrasada.

    Raises:
        ValueError: Se a unidade de tempo não for suportada.
    """

    if unidade == "dia" or unidade == "dias":
        data_atrasada = hoje - timedelta(days=quantidade)
    elif unidade == "semana" or unidade == "semanas":
        data_atrasada = hoje - timedelta(weeks=quantidade)
    elif unidade == "mês" or unidade == "meses":
        data_atrasada = hoje - timedelta(days=quantidade * 30)
    elif unidade == "ano" or unidade == "anos":
        data_atrasada = hoje - timedelta(days=quantidade * 365)
    elif unidade == "hora" or unidade == "horas":
        data_atrasada = hoje - timedelta(hours=quantidade)
    else:
        raise ValueError(f"Unidade de tempo '{unidade}' não suportada")

    return data_atrasada

def _tratar_um(texto: str) -> int:
    """
    Trata o caso especial de "um" e "uma".

    Args:
        texto (str): Texto a ser tratado.

    Returns:
        int: 1 se o texto for "um" ou "uma", o valor original caso contrário.
    """

    if texto.lower() == "um" or texto.lower() == "uma":
        return 1
    return int(texto)