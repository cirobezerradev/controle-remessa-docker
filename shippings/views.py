from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from dom_nfe import DomNFe
from .models import Shipping, ShippingItem, ShippingStorage, ReturnOfShip, ReturnItem
from .validators import *
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Avg, Count
from .forms import SearchShip

# Create your views here.


def index(request):
    return render(request, 'shippings/pages/index.html')


def abrir_xml_remessa(request):
    if request.method == 'POST' and request.path == '/cadastrar_remessa/xml/':
        if not request.FILES == {}:
            try:
                xml = request.FILES.get('xml')

                validator_extension_file(xml)

                dom = DomNFe(xml)

                validator_cfop_remessa(dom.cfop)

                return render(request, 'shippings/pages/cadastrar_remessa.html',
                              {'cliente': dom.cliente,
                               'nfe': dom.num_nfe,
                               'emission': dom.data_emissao,
                               'limit': dom.data_limite,
                               'volumes': dom.volumes,
                               'peso': dom.peso,
                               'itens': dom.itens})
            
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'shippings/pages/cadastrar_remessa.html')
            except XMLInvalidError as e:
                messages.error(request, e)
                return render(request, 'shippings/pages/cadastrar_remessa.html')

    return redirect('cadastrar_remessa')


def cadastrar_remessa(request):
    if request.method == 'POST' and request.path == '/cadastrar_remessa/':
        try:    
            lista_remessa = request.POST.getlist('remessa')

            shipping = Shipping(*lista_remessa)
            shipping.save()

            lista_post = list(request.POST.lists())

            for i in range(1, len(lista_post)-1):
                lista_itens = request.POST.getlist(f'{i}')
                shipping_item = ShippingItem(codigo=lista_itens[0],
                                                descricao=lista_itens[1],
                                                un=lista_itens[2],
                                                quantidade=lista_itens[3],
                                                valor_unit=lista_itens[4],
                                                nfe_remessa=Shipping.objects.get(nfe=shipping.nfe))

                shipping_storage = ShippingStorage(codigo=lista_itens[0],
                                                    descricao=lista_itens[1],
                                                    un=lista_itens[2],
                                                    quantidade=lista_itens[3],
                                                    valor_unit=lista_itens[4],
                                                    nfe_remessa=Shipping.objects.get(nfe=shipping.nfe))

                shipping_item.save()
                shipping_storage.save()

            messages.info(request, f"Remessa {
                            shipping.nfe} cadastrada com sucesso!")
        
        except IntegrityError as e:
            print(e)
            messages.warning(request, f'Essa remessa {shipping.nfe} já foi cadastrada anteriormente')

    return render(request, 'shippings/pages/cadastrar_remessa.html')


def retornar_remessa(request):
    remessas_db = Shipping.objects.values().filter(status='PENDENTE')
    lista = list(remessas_db)
    return render(request, 'shippings/pages/retornar_remessa.html', {'remessas': lista})


def abrir_xml_retorno(request, nfe):
    if request.method == 'POST' and request.path == f'/cadastrar_retorno/{nfe}/xml':
        if not request.FILES == {}:
            try:
                xml = request.FILES.get('xml')

                validator_extension_file(xml)

                dom = DomNFe(xml)

                validator_cfop_retorno(dom.cfop)

                return render(request, 'shippings/pages/cadastrar_retorno.html',
                              {'cliente': dom.cliente,
                               'nfe': dom.num_nfe,
                               'emission': dom.data_emissao,
                               'limit': dom.data_limite,
                               'volumes': dom.volumes,
                               'peso': dom.peso,
                               'itens': dom.itens,
                               'nfe_remessa': nfe})
            
            except ValidationError as e:
                messages.error(request, e)
                return render(request, 'shippings/pages/cadastrar_retorno.html', {'nfe_remessa': nfe})
            except XMLInvalidError as e:
                messages.error(request, e)
                return render(request, 'shippings/pages/cadastrar_retorno.html', {'nfe_remessa': nfe})

    return redirect('cadastrar_retorno', nfe)


def cadastrar_retorno(request, nfe):
    if request.method == 'POST' and request.path == f'/cadastrar_retorno/{nfe}/':
        try:
            lista_retorno = request.POST.getlist('retorno')

            return_shipping = ReturnOfShip(*lista_retorno)
            return_shipping.save()

            lista_post = list(request.POST.lists())
            objects_items = []
            objects_storage = []

            for i in range(1, len(lista_post)-1):
                list_items = request.POST.getlist(f'{i}')
                return_item = ReturnItem(codigo=list_items[0],
                                        descricao=list_items[1],
                                        un=list_items[2],
                                        quantidade=list_items[3],
                                        valor_unit=list_items[4],
                                        nfe_retorno= ReturnOfShip.objects.get(nfe=return_shipping.nfe)
                                        )              

                # BUSCA O ID DO ITEM NO ESTOQUE QUE SERÁ RETORNADO EM CADA LOOP                
                id_item = ShippingStorage.objects.values().filter(nfe_remessa=nfe,
                                                                codigo=request.POST.getlist(f'{i}')[0])[0]['id']
                product_storage = ShippingStorage.objects.get(id=id_item)

                # VERIFICA SE A QUANTIDADE EM ESTOQUE É SUFICIENTE PARA REALIZAR O RETORNO
                if float(product_storage.quantidade) < float(return_item.quantidade):
                    raise InsufficientStock(f'ERRO: Quantidade insuficiente em estoque')
                
                product_storage.quantidade = float(product_storage.quantidade) - float(return_item.quantidade)

                objects_items.append(return_item)
                objects_storage.append(product_storage)
            
            for o in objects_items:
                o.save()
            
            for o in objects_storage:
                o.save()
            
            # SOMA O TOTAL DAS QUANTIDADES DOS ITENS EM ESTOQUE DA REMESSA
            total = ShippingStorage.objects.values().filter(nfe_remessa=nfe).aggregate(total=Sum('quantidade'))['total']

            # VERIFICA SE O ESTOQUE ZEROU PARA ALTERAR O STATUS DA REMESSA DE PENDENTE PARA FINALIZADA
            if total == 0:
                shipping = Shipping.objects.get(nfe=return_shipping.nfe_remessa.nfe)
                shipping.status = 'FINALIZADA'
                shipping.save()
                messages.info(request, f'A REMESSA {nfe} foi {shipping.status}!')
                            
            messages.info(request, f'Retorno {return_shipping.nfe} efetuado com SUCESSO!')

        except InsufficientStock as e:
            messages.error(request, e)
            messages.warning(request, f'ITEM: {return_item.codigo} {return_item.descricao}, \
                                QTD.: {return_item.quantidade}')
            messages.warning(request, f'QTD EM ESTOQUE: {product_storage.quantidade}')
            return_rollback = ReturnOfShip.objects.get(nfe=return_shipping.nfe)
            return_rollback.delete()
        
        except IntegrityError as e:
            print(e)
            messages.warning(request, f'Esse retorno {shipping.nfe} já foi cadastrada anteriormente')
                
        
    return render(request, 'shippings/pages/cadastrar_retorno.html', {'nfe_remessa': nfe})

def buscar_remessas(request):
    if request.method == 'POST':
        pass

    form = SearchShip()

    shippings = Shipping.objects.all()
    paginator = Paginator(shippings, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shippings/pages/buscar_remessas.html', {'form': form, 'page_obj': page_obj})
