from django.core.exceptions import ValidationError


class XMLInvalidError(Exception):
    pass

class InsufficientStock(Exception):
    pass


def validator_extension_file(value):
    alloweds_extensions = ['xml']
    extension = value.name.split('.')[-1].lower()
    if extension not in alloweds_extensions:
        raise ValidationError(
            'ERRO: Você tentou inserir um arquivo inválido. Favor insira um documento XML.')

    return True


def validator_cfop_remessa(cfop: list):
    if not set(cfop) == {6901}:
        raise XMLInvalidError(
            f'XML INVÁLIDO: CFOP da NFe não conforme. CFOP: {set(cfop)}')

    return True


def validator_cfop_retorno(cfop: list):
    if not set(cfop) == {6902}:
        raise XMLInvalidError(
            f'XML INVÁLIDO: CFOP da NFe não conforme. CFOP: {set(cfop)}')
    return True

