from django.shortcuts import render, redirect
from .models import Empresa, Documento, Metrica
from django.contrib import messages
from django.contrib.messages import constants
from investidores.models import PropostaInvestimento
from django.utils import timezone
from datetime import timedelta

def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    if request.method == 'GET':
        return render(request, 'cadastrar_empresa.html',
                      {'tempo_existencia': Empresa.tempo_existencia_choices, 
                       'areas': Empresa.area_choices})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('areas')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        try:
            empresa = Empresa(
                    user=request.user,
                    nome=nome,
                    cnpj=cnpj,
                    site=site,
                    tempo_existencia=tempo_existencia,
                    descricao=descricao,
                    data_final_captacao=data_final,
                    percentual_equity=percentual_equity,
                    estagio=estagio,
                    area=area,
                    publico_alvo=publico_alvo,
                    valor=valor,
                    pitch=pitch,
                    logo=logo
            )
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor!')
            return redirect('/empresarios/cadastrar_empresa/')

        empresa.save()

        messages.add_message(request, constants.SUCCESS, 'Empresa Criada com sucesso!')

        return redirect('/empresarios/cadastrar_empresa/')
    
def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/logar')
    if request.method == 'GET':
        nome_empresa = request.GET.get('empresa')
        empresas = Empresa.objects.filter(user=request.user)
        if nome_empresa:
            empresas = empresas.filter(nome__icontains=nome_empresa)
        return render(request, 'listar_empresas.html', {'empresas': empresas, 'nome_empresa': nome_empresa})
    
def empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não é sua!')
        return redirect('/empresarios/listar_empresas')

    if request.method == 'GET':
        documentos = Documento.objects.filter(empresa=empresa)
        propostas_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
        percentual_vendido = 0
        total_captado = 0
        for pi in propostas_investimentos:
            if pi.status == 'PA':
                percentual_vendido += pi.percentual
                total_captado += pi.valor
        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0
        propostas_investimentos_enviada = propostas_investimentos.filter(status='PE')
        return render(request, 'empresa.html', {'empresa': empresa, 'documentos': documentos, 'propostas_investimentos_enviada': propostas_investimentos_enviada, 'percentual_vendido': int(percentual_vendido), 'total_captado': total_captado, 'valuation_atual': valuation_atual})
    
def add_doc(request, id):
    empresa = Empresa.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    if arquivo:
        extensao = arquivo.name.split('.')

    if not arquivo:
        messages.add_message(request, constants.ERROR, 'Envie um arquivo!')
        return redirect(f'/empresarios/empresa/{id}')
    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, 'Envie apenas PDF!')
        return redirect(f'/empresarios/empresa/{id}')
    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não é sua!')
        return redirect('/empresarios/listar_empresas')

    documento = Documento(
        empresa = empresa,
        titulo = titulo,
        arquivo = arquivo,
    )

    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Arquivo cadastrado com sucesso!')
    return redirect(f'/empresarios/empresa/{id}')

def excluir_doc(request, id):
    documento = Documento.objects.get(id=id)
    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não é sua!')
        return redirect('/empresarios/listar_empresas')
    documento.delete()
    messages.add_message(request, constants.SUCCESS, 'Documento deletado com sucesso!')
    return redirect(f'/empresarios/empresa/{documento.empresa.id}')

def add_metrica(request, id):
    empresa = Empresa.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    metrica = Metrica(
        empresa = empresa,
        titulo = titulo,
        valor = valor
    )

    metrica.save()

    messages.add_message(request, constants.SUCCESS, 'Métrica cadastrada com sucesso')
    return redirect(f'/empresarios/empresa/{empresa.id}')

def gerenciar_proposta(request, id):
    acao = request.GET.get('acao')
    pi = PropostaInvestimento.objects.get(id=id)

    if acao == 'aceitar':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita.')
        pi.status = 'PA'
    elif acao == 'recusar':
        messages.add_message(request, constants.SUCCESS, 'Que pena, proposta recusada.')
        pi.status = 'PR'

    pi.save()
    return redirect(f'/empresarios/empresa/{pi.empresa.id}')

def dashboard(request, id):
    empresa = Empresa.objects.get(id=id)
    hoje = timezone.now().date()

    sete_dias_atras = hoje - timedelta(days=6)

    propostas_por_dia = {}

    for i in range(7):
        dia = sete_dias_atras + timedelta(days=i)

        propostas = PropostaInvestimento.objects.filter(
            empresa=empresa,
            status='PA',
            data =dia
        )

        total_dia = 0
        for proposta in propostas:
            total_dia += proposta.valor

        propostas_por_dia[dia.strftime('%d/%m/%Y')] = int(total_dia)

    return render(request, 'dashboard.html', {'labels': list(propostas_por_dia.keys()), 'values': list(propostas_por_dia.values())})
