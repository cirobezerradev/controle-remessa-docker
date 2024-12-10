from xml.dom import minidom
from datetime import datetime, timedelta


class DomNFe:
    def __init__(self, xml: None) -> None:
        
        self.dom_nfe = minidom.parse(xml.file)

        self.cliente = self.dom_nfe.getElementsByTagName('xNome')[0].firstChild.data

        self.num_nfe = int(self.dom_nfe.getElementsByTagName('nNF')[
                           0].firstChild.data)
        # A data é formatada pelo método format_data
        self.data_emissao = self.format_data(self.dom_nfe.getElementsByTagName('dhEmi')[
            0].firstChild.data[:10])
        self.data_limite = self.limite()
        self.volumes = int(self.dom_nfe.getElementsByTagName(
            'qVol')[0].firstChild.data)
        self.peso = float(self.dom_nfe.getElementsByTagName(
            'pesoB')[0].firstChild.data)
        self.itens = []  # Armazena os itens da remessa
        # armazena a quantidade de itens da remessa
        self.quantidade_itens = len(self.dom_nfe.getElementsByTagName('det'))
        self.itens_remessa(xml)  # insere os itens na lista self.itens
        self.cfop = self.cfop_itens(xml)

    def itens_remessa(self, url) -> None:
        
        for i in range(self.quantidade_itens):
            self.itens.append([int(self.dom_nfe.getElementsByTagName('cProd')[i].firstChild.data),
                               self.dom_nfe.getElementsByTagName(
                                   'xProd')[i].firstChild.data,
                               self.dom_nfe.getElementsByTagName(
                                   'uCom')[i].firstChild.data,
                               float(self.dom_nfe.getElementsByTagName(
                                   'qCom')[i].firstChild.data),
                               float(self.dom_nfe.getElementsByTagName('vUnCom')[i].firstChild.data)])
    
    def cfop_itens(self, url: str) -> list:
        lista_cfop = []
        for i in range(self.quantidade_itens):
            lista_cfop.append(int(self.dom_nfe.getElementsByTagName('CFOP')[i].firstChild.data))
        return lista_cfop

    # FORMATATAÇÃO DE DATA
    def format_data(self, data) -> object:
        data = datetime.strptime(data, '%Y-%m-%d')
        return data.strftime('%Y-%m-%d')
    
    def limite(self):
        data = datetime.strptime(self.data_emissao, '%Y-%m-%d') + timedelta(days=180)
        return data.strftime('%Y-%m-%d')