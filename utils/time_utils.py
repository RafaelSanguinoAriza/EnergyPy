"""
Utilidades para el manejo y validación de tiempo.

Este módulo proporciona funciones para validar y convertir
diferentes unidades de tiempo utilizadas en la aplicación.
"""

import re
from datetime import datetime, timedelta


def validate_time_input(value, unit='seconds'):
    """Valida que el valor de tiempo sea un número positivo.

    Args:
        value: Valor a validar (str o int)
        unit (str): Unidad de tiempo ('seconds', 'minutes', 'hours')

    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    try:
        # Convertir a entero si es string
        if isinstance(value, str):
            if not value.strip():
                return False, "El valor no puede estar vacío"
            if not value.isdigit():
                return False, "El valor debe ser un número entero positivo"
            value = int(value)
        
        # Validar rango según unidad
        if value < 0:
            return False, "El valor debe ser positivo"
        
        if unit == 'seconds':
            max_value = 86400  # 24 horas en segundos
            if value > max_value:
                return False, f"El valor máximo es {max_value} segundos (24 horas)"
        elif unit == 'minutes':
            max_value = 1440  # 24 horas en minutos
            if value > max_value:
                return False, f"El valor máximo es {max_value} minutos (24 horas)"
        elif unit == 'hours':
            max_value = 24
            if value > max_value:
                return False, f"El valor máximo es {max_value} horas"
        
        return True, ""
    except Exception as e:
        return False, f"Error de validación: {str(e)}"


def validate_time_format(time_str):
    """Valida que el formato de hora sea HH:MM.

    Args:
        time_str (str): String con formato de hora HH:MM

    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    if not time_str:
        return False, "La hora no puede estar vacía"
    
    # Validar formato HH:MM
    pattern = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
    if not re.match(pattern, time_str):
        return False, "Formato inválido. Use HH:MM (24h)"
    
    return True, ""


def convert_to_seconds(value, unit='seconds'):
    """Convierte un valor de tiempo a segundos.

    Args:
        value (int): Valor a convertir
        unit (str): Unidad de origen ('seconds', 'minutes', 'hours')

    Returns:
        int: Valor en segundos
    """
    if unit == 'seconds':
        return value
    elif unit == 'minutes':
        return value * 60
    elif unit == 'hours':
        return value * 3600
    else:
        raise ValueError(f"Unidad de tiempo no reconocida: {unit}")


def format_time_remaining(seconds):
    """Formatea el tiempo restante en un formato legible.

    Args:
        seconds (int): Segundos restantes

    Returns:
        str: Tiempo formateado (HH:MM:SS)
    """
    if seconds is None:
        return "--:--:--"
    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def time_string_to_datetime(time_str):
    """Convierte un string de hora a un objeto datetime para hoy.

    Args:
        time_str (str): String con formato de hora HH:MM

    Returns:
        datetime: Objeto datetime para la hora especificada hoy
    """
    now = datetime.now()
    hour, minute = map(int, time_str.split(':'))
    
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Si la hora ya pasó, asumimos que es para mañana
    if target_time < now:
        target_time += timedelta(days=1)
    
    return target_time


def get_time_units():
    """Retorna las unidades de tiempo disponibles.

    Returns:
        list: Lista de unidades de tiempo
    """
    return ['seconds', 'minutes', 'hours']


def get_time_unit_label(unit, language='es'):
    """Obtiene la etiqueta traducida para una unidad de tiempo.

    Args:
        unit (str): Unidad de tiempo ('seconds', 'minutes', 'hours')
        language (str): Idioma ('es' o 'en')

    Returns:
        str: Etiqueta traducida
    """
    labels = {
        'es': {
            'seconds': 'Segundos',
            'minutes': 'Minutos',
            'hours': 'Horas'
        },
        'en': {
            'seconds': 'Seconds',
            'minutes': 'Minutes',
            'hours': 'Hours'
        }
    }
    
    return labels.get(language, labels['en']).get(unit, unit)