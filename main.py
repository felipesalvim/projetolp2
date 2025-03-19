import json

# --- VARIÁVEIS GLOBAIS ---
dados = {
    "reservas": [],
    "pedidos": [],
    "caixa": {"Pix": 0.0, "Debito": 0.0, "Credito": 0.0, "Especie": 0.0},
    "estoque": {}
}

cardapio = {
"Pizzas": {
    "Calabresa": {"descrição": "Queijo, calabresa fatiada, cebola e azeitonas", "preço": 32.0},
    "Frango com Catupiry": {"descrição": "Frango desfiado, catupiry e milho", "preço": 36.0},
    "Quatro Queijos": {"descrição": "Mussarela, parmesão, provolone e gorgonzola", "preço": 38.0},
    "Vegetariana": {"descrição": "Mix de vegetais frescos e queijo mussarela", "preço": 30.0},
    "Peperoni": {"descrição": "Queijo, peperoni e orégano", "preço": 35.0},
    "Portuguesa Gourmet": {"descrição": "Queijo, presunto, ovos, cebola roxa, pimentão e azeitonas verdes", "preço": 40.0},
    "Palmito": {"descrição": "Queijo, palmito, tomate seco e manjericão", "preço": 37.0},
    "Strogonoff": {"descrição": "Recheio de strogonoff de carne e batata palha", "preço": 42.0},
    "Cheddar Bacon": {"descrição": "Queijo cheddar, bacon e cebola caramelizada", "preço": 39.0},
    "Mariscos": {"descrição": "Frutos do mar, molho especial e queijo parmesão", "preço": 45.0}
},

"Massas": {
    "Nhoque ao Sugo": {"descrição": "Nhoque de batata com molho de tomate", "preço": 22.0},
    "Penne ao Alfredo": {"descrição": "Molho branco cremoso com parmesão", "preço": 26.0},
    "Ravioli de Ricota": {"descrição": "Ravioli recheado com ricota e espinafre", "preço": 30.0},
    "Talharim Carbonara": {"descrição": "Talharim com bacon e creme de leite", "preço": 28.0},
    "Fettuccine com Camarão": {"descrição": "Molho de camarão ao azeite e alho", "preço": 35.0},
    "Canelone de Queijo": {"descrição": "Recheado com mussarela e coberto com molho rosé", "preço": 29.0},
    "Rigatoni à Bolonhesa": {"descrição": "Molho de carne com especiarias italianas", "preço": 27.0},
    "Lasanha de Espinafre": {"descrição": "Camadas de espinafre, queijo e molho branco", "preço": 32.0},
    "Espaguete ao Pesto": {"descrição": "Molho pesto de manjericão com nozes e parmesão", "preço": 30.0},
    "Capeletti de Carne": {"descrição": "Recheio de carne ao molho sugo", "preço": 28.0}
},
}

# --- FUNÇÕES AUXILIARES ---
def inicializar_estoque():
    """Inicializa o estoque com base no cardápio."""
    for categoria, itens in cardapio.items():
        for item in itens:
            if item not in dados["estoque"]:
                dados["estoque"][item] = 50  # Define quantidade padrão para cada item

def carregar_dados():
    """Carrega os dados do arquivo JSON ou cria um arquivo padrão."""
    global dados
    try:
        with open("dados_restaurante.json", "r", encoding="utf-8") as arquivo_json:
            dados = json.load(arquivo_json)
            if "caixa" not in dados:
                dados["caixa"] = {"Pix": 0.0, "Debito": 0.0, "Credito": 0.0, "Especie": 0.0}
            for metodo in ["Pix", "Debito", "Credito", "Especie"]:
                if metodo not in dados["caixa"]:
                    dados["caixa"][metodo] = 0.0
    except (FileNotFoundError, json.JSONDecodeError):
        salvar_dados()

def salvar_dados():
    """Salva os dados no arquivo JSON."""
    with open("dados_restaurante.json", "w", encoding="utf-8") as arquivo_json:
        json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)

def exibir_cardapio():
    """Exibe o cardápio completo, indicando itens fora de estoque."""
    print("\n--- CARDÁPIO COMPLETO ---")
    contador = 1
    mapeamento_itens = {}
    for categoria, itens in cardapio.items():
        print(f"\n{categoria}:")
        for item, detalhes in itens.items():
            status = "(Indisponível)" if dados["estoque"].get(item, 0) <= 0 else ""
            print(f"{contador}. {item}: {detalhes['descrição']} (R$ {detalhes['preço']:.2f}) {status}")
            mapeamento_itens[contador] = item
            contador += 1
    return mapeamento_itens

# --- GESTÃO DE PEDIDOS ---
def registrar_pedido():
    """Registra pedidos de clientes, verificando o estoque."""
    cliente = input("Digite o nome do cliente: ").strip()
    if not cliente:
        print("O nome do cliente não pode ser vazio.")
        return

    pedido = {"cliente": cliente, "itens": [], "total": 0.0}
    mapeamento_itens = exibir_cardapio()

    while True:
        escolha = input("\nDigite o número do item (ou 'sair' para finalizar): ").strip()
        if escolha.lower() == "sair":
            break
        try:
            escolha_numero = int(escolha)
            if escolha_numero in mapeamento_itens:
                nome_item = mapeamento_itens[escolha_numero]
                if dados["estoque"].get(nome_item, 0) <= 0:
                    print(f"Desculpe, o item '{nome_item}' está indisponível no momento.")
                    continue
                quantidade = int(input(f"Digite a quantidade de {nome_item}: "))
                if quantidade <= dados["estoque"][nome_item]:
                    preco = cardapio[next(cat for cat in cardapio if nome_item in cardapio[cat])][nome_item]["preço"]
                    pedido["itens"].append({"nome": nome_item, "quantidade": quantidade, "preço_unitário": preco})
                    pedido["total"] += quantidade * preco
                    dados["estoque"][nome_item] -= quantidade
                    salvar_dados()
                    print(f"{quantidade}x {nome_item} adicionados ao pedido.")
                else:
                    print(f"Estoque insuficiente. Apenas {dados['estoque'][nome_item]} unidades disponíveis.")
            else:
                print("Número inválido. Por favor, tente novamente.")
        except (ValueError, KeyError):
            print("Entrada inválida. Por favor, digite um número válido.")

    if pedido["itens"]:
        dados["pedidos"].append(pedido)
        salvar_dados()
        print(f"Pedido registrado com sucesso para {cliente}!")

def finalizar_pedido():
    """Finaliza um pedido e registra o pagamento."""
    if not dados["pedidos"]:
        print("Nenhum pedido registrado.")
        return

    for i, pedido in enumerate(dados["pedidos"], start=1):
        print(f"\nPedido {i}: Cliente: {pedido['cliente']}, Total: R$ {pedido['total']:.2f}")
        for item in pedido["itens"]:
            print(f"  - {item['quantidade']}x {item['nome']} (R$ {item['preço_unitário']:.2f} cada)")

    try:
        numero_pedido = int(input("\nDigite o número do pedido a ser finalizado: ")) - 1
        if 0 <= numero_pedido < len(dados["pedidos"]):
            pedido = dados["pedidos"].pop(numero_pedido)
            print(f"Finalizando pedido do cliente {pedido['cliente']}, Total: R$ {pedido['total']:.2f}")
            print("\nEscolha o método de pagamento:")
            print("1. Pix")
            print("2. Débito")
            print("3. Crédito")
            print("4. Espécie")
            metodo = input("Digite o número correspondente ao método de pagamento: ").strip()

            metodos_pagamento = {"1": "Pix", "2": "Debito", "3": "Credito", "4": "Especie"}
            if metodo in metodos_pagamento:
                dados["caixa"][metodos_pagamento[metodo]] += pedido["total"]
                salvar_dados()
                print("Pagamento registrado e pedido finalizado!")
            else:
                print("Método de pagamento inválido. Por favor, tente novamente.")
        else:
            print("Número do pedido inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

# --- GESTÃO DE FUNCIONÁRIOS ---
def cadastrar_funcionario():
    """Cadastra um novo funcionário."""
    print("\n--- CADASTRAR FUNCIONÁRIO ---")
    nome = input("Nome do funcionário: ").strip()
    cargo = input("Cargo: ").strip()
    salario = float(input("Salário (em R$): "))
    horario = input("Horário de trabalho (ex: 08:00 às 17:00): ").strip()

    funcionario = {
        "nome": nome,
        "cargo": cargo,
        "salario": salario,
        "horario": horario
    }

    if "funcionarios" not in dados:
        dados["funcionarios"] = []

    dados["funcionarios"].append(funcionario)
    salvar_dados()
    print(f"Funcionário {nome} cadastrado com sucesso!")

def exibir_funcionarios():
    """Exibe todos os funcionários cadastrados."""
    if "funcionarios" not in dados or not dados["funcionarios"]:
        print("\nNenhum funcionário cadastrado.")
    else:
        print("\n--- LISTA DE FUNCIONÁRIOS ---")
        for i, funcionario in enumerate(dados["funcionarios"], start=1):
            print(f"{i}. Nome: {funcionario['nome']}, Cargo: {funcionario['cargo']}, Salário: R$ {funcionario['salario']:.2f}, Horário: {funcionario['horario']}")

def editar_funcionario():
    """Edita as informações de um funcionário."""
    exibir_funcionarios()
    if "funcionarios" not in dados or not dados["funcionarios"]:
        return

    try:
        numero = int(input("\nDigite o número do funcionário para editar: ")) - 1
        if 0 <= numero < len(dados["funcionarios"]):
            funcionario = dados["funcionarios"][numero]
            print(f"\nEditando informações de {funcionario['nome']}:")
            funcionario["nome"] = input("Novo nome (deixe vazio para manter o atual): ").strip() or funcionario["nome"]
            funcionario["cargo"] = input("Novo cargo (deixe vazio para manter o atual): ").strip() or funcionario["cargo"]
            salario = input("Novo salário (deixe vazio para manter o atual): ").strip()
            funcionario["salario"] = float(salario) if salario else funcionario["salario"]
            funcionario["horario"] = input("Novo horário (deixe vazio para manter o atual): ").strip() or funcionario["horario"]
            salvar_dados()
            print("Funcionário atualizado com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

def remover_funcionario():
    """Remove um funcionário do sistema."""
    exibir_funcionarios()
    if "funcionarios" not in dados or not dados["funcionarios"]:
        return

    try:
        numero = int(input("\nDigite o número do funcionário para remover: ")) - 1
        if 0 <= numero < len(dados["funcionarios"]):
            funcionario = dados["funcionarios"].pop(numero)
            salvar_dados()
            print(f"Funcionário {funcionario['nome']} removido com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

# --- GESTÃO DE FORNECEDORES ---
def cadastrar_fornecedor():
    """Cadastra um novo fornecedor."""
    print("\n--- CADASTRAR FORNECEDOR ---")
    nome = input("Nome do fornecedor: ").strip()
    contato = input("Contato (telefone ou email): ").strip()
    endereco = input("Endereço: ").strip()

    fornecedor = {
        "nome": nome,
        "contato": contato,
        "endereco": endereco,
        "historico_compras": []
    }

    if "fornecedores" not in dados:
        dados["fornecedores"] = []

    dados["fornecedores"].append(fornecedor)
    salvar_dados()
    print(f"Fornecedor {nome} cadastrado com sucesso!")

def exibir_fornecedores():
    """Exibe todos os fornecedores cadastrados."""
    if "fornecedores" not in dados or not dados["fornecedores"]:
        print("\nNenhum fornecedor cadastrado.")
    else:
        print("\n--- LISTA DE FORNECEDORES ---")
        for i, fornecedor in enumerate(dados["fornecedores"], start=1):
            print(f"{i}. Nome: {fornecedor['nome']}, Contato: {fornecedor['contato']}, Endereço: {fornecedor['endereco']}")
            if fornecedor["historico_compras"]:
                print("   Histórico de Compras:")
                for compra in fornecedor["historico_compras"]:
                    print(f"     - {compra}")
            else:
                print("   Sem compras registradas.")

def editar_fornecedor():
    """Edita as informações de um fornecedor."""
    exibir_fornecedores()
    if "fornecedores" not in dados or not dados["fornecedores"]:
        return

    try:
        numero = int(input("\nDigite o número do fornecedor para editar: ")) - 1
        if 0 <= numero < len(dados["fornecedores"]):
            fornecedor = dados["fornecedores"][numero]
            print(f"\nEditando informações de {fornecedor['nome']}:")
            fornecedor["nome"] = input("Novo nome (deixe vazio para manter o atual): ").strip() or fornecedor["nome"]
            fornecedor["contato"] = input("Novo contato (deixe vazio para manter o atual): ").strip() or fornecedor["contato"]
            fornecedor["endereco"] = input("Novo endereço (deixe vazio para manter o atual): ").strip() or fornecedor["endereco"]
            salvar_dados()
            print("Fornecedor atualizado com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

def remover_fornecedor():
    """Remove um fornecedor do sistema."""
    exibir_fornecedores()
    if "fornecedores" not in dados or not dados["fornecedores"]:
        return

    try:
        numero = int(input("\nDigite o número do fornecedor para remover: ")) - 1
        if 0 <= numero < len(dados["fornecedores"]):
            fornecedor = dados["fornecedores"].pop(numero)
            salvar_dados()
            print(f"Fornecedor {fornecedor['nome']} removido com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

def registrar_compra_fornecedor():
    """Adiciona um registro de compra ao histórico de um fornecedor."""
    exibir_fornecedores()
    if "fornecedores" not in dados or not dados["fornecedores"]:
        return

    try:
        numero = int(input("\nDigite o número do fornecedor para registrar uma compra: ")) - 1
        if 0 <= numero < len(dados["fornecedores"]):
            fornecedor = dados["fornecedores"][numero]
            detalhes_compra = input("Digite os detalhes da compra (ex: '10 caixas de molho de tomate por R$ 500'): ").strip()
            fornecedor["historico_compras"].append(detalhes_compra)
            salvar_dados()
            print("Compra registrada com sucesso!")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

# --- MENU GESTÃO DE FORNECEDORES ---
def menu_gestao_fornecedores():
    """Menu para gestão de fornecedores."""
    while True:
        print("\n--- GESTÃO DE FORNECEDORES ---")
        print("1. Cadastrar Fornecedor")
        print("2. Exibir Fornecedores")
        print("3. Editar Fornecedor")
        print("4. Remover Fornecedor")
        print("5. Registrar Compra com Fornecedor")
        print("6. Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_fornecedor()
        elif opcao == "2":
            exibir_fornecedores()
        elif opcao == "3":
            editar_fornecedor()
        elif opcao == "4":
            remover_fornecedor()
        elif opcao == "5":
            registrar_compra_fornecedor()
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")

# --- MENU PRINCIPAL ---
def menu_principal():
    """Menu principal do sistema."""
    carregar_dados()
    inicializar_estoque()
    while True:
        print("\n--- SISTEMA DE GESTÃO ---")
        print("1. Exibir Cardápio")
        print("2. Registrar Pedido")
        print("3. Finalizar Pedido")
        print("4. Gerir Estoque")
        print("5. Gestão de Funcionários")
        print("6. Gestão de Fornecedores")
        print("7. Exibir Caixa")
        print("8. Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            exibir_cardapio()
        elif opcao == "2":
            registrar_pedido()
        elif opcao == "3":
            finalizar_pedido()
        elif opcao == "4":
            gerir_estoque()
        elif opcao == "5":
            menu_gestao_funcionarios()
        elif opcao == "6":
            menu_gestao_fornecedores()
        elif opcao == "7":
            exibir_caixa()
        elif opcao == "8":
            salvar_dados()
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# --- MENU GESTÃO DE FUNCIONÁRIOS ---
def menu_gestao_funcionarios():
    """Menu para gestão de funcionários."""
    while True:
        print("\n--- GESTÃO DE FUNCIONÁRIOS ---")
        print("1. Cadastrar Funcionário")
        print("2. Exibir Funcionários")
        print("3. Editar Funcionário")
        print("4. Remover Funcionário")
        print("5. Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_funcionario()
        elif opcao == "2":
            exibir_funcionarios()
        elif opcao == "3":
            editar_funcionario()
        elif opcao == "4":
            remover_funcionario()
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")

# --- MENU GESTÃO DE FORNECEDORES ---
def menu_gestao_fornecedores():
    """Menu para gestão de fornecedores."""
    while True:
        print("\n--- GESTÃO DE FORNECEDORES ---")
        print("1. Cadastrar Fornecedor")
        print("2. Exibir Fornecedores")
        print("3. Editar Fornecedor")
        print("4. Remover Fornecedor")
        print("5. Registrar Compra com Fornecedor")
        print("6. Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_fornecedor()
        elif opcao == "2":
            exibir_fornecedores()
        elif opcao == "3":
            editar_fornecedor()
        elif opcao == "4":
            remover_fornecedor()
        elif opcao == "5":
            registrar_compra_fornecedor()
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")

# --- GESTÃO DE ESTOQUE ---
def gerir_estoque():
    """Permite visualizar e repor o estoque."""
    print("\n--- ESTOQUE ---")
    for item, qtd in dados["estoque"].items():
        print(f"{item}: {qtd} unidades")
    item = input("Digite o nome do item para repor (ou 'sair' para voltar): ").strip()
    if item in dados["estoque"]:
        try:
            qtd = int(input(f"Quantidade a adicionar para {item}: "))
            dados["estoque"][item] += qtd
            salvar_dados()
            print(f"Estoque atualizado: {item} agora tem {dados['estoque'][item]} unidades.")
        except ValueError:
            print("Quantidade inválida.")
    elif item.lower() != "sair":
        print("Item não encontrado.")

# --- GESTÃO DE CAIXA ---
def exibir_caixa():
    """Exibe o total acumulado no caixa por método de pagamento."""
    print("\n--- CAIXA ---")
    for metodo, valor in dados["caixa"].items():
        print(f"{metodo}: R$ {valor:.2f}")

# --- EXECUTAR SISTEMA ---
if __name__ == "__main__":
    menu_principal()