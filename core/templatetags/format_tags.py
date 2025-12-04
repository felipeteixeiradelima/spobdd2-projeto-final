from django import template
import re

register = template.Library()

@register.filter
def format_cpf(value):
    """
    Formata uma string de 11 dígitos (CPF sem pontuação) para o formato XXX.XXX.XXX-XX.
    """
    if not isinstance(value, str) or len(value) != 11 or not value.isdigit():
        return value  # Retorna o valor original se não for um CPF válido (apenas dígitos, 11 chars)

    # Aplica a máscara usando regex
    # O padrão (\d{3})(\d{3})(\d{3})(\d{2}) captura grupos de dígitos
    # E substitui pelo formato desejado \1.\2.\3-\4
    formatted_cpf = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', value)
    return formatted_cpf
