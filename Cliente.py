import Pyro4


# Classe do Cliente
@Pyro4.expose
class Client:
    def __init__(self, client_id):
        self.client_id = client_id

    def notify_event(self, filename):
        print(f"Notificação recebida: Arquivo '{filename}' está agora disponível.")

    def start(self, server_uri):
        server = Pyro4.Proxy(server_uri)  # Cria um proxy para se conectar ao servidor usando o URI fornecido
        self.register_interests(server)  # Registra os interesses do cliente no servidor

    def register_interests(self, server):
        while True:
            print("\n----- MENU -----")
            print("1. Consultar arquivos disponíveis")
            print("2. Fazer download de um arquivo")
            print("3. Registrar interesse em um arquivo")
            print("4. Cancelar registro de interesse")
            print("0. Sair")

            choice = input("Digite o número da opção desejada: ")

            if choice == "1":
                self.display_available_files(server)
            elif choice == "2":
                self.download_file(server)
            elif choice == "3":
                self.register_file_interest(server)
            elif choice == "4":
                self.unregister_file_interest(server)
            elif choice == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def display_available_files(self, server):
        files = server.get_available_files()
        if files:
            print("\nArquivos disponíveis:")
            for file in files:
                print(file)
        else:
            print("\nNenhum arquivo disponível.")

    def download_file(self, server):
        filename = input("Digite o nome do arquivo que deseja baixar: ")
        file_content = server.download_file(filename)
        if file_content:
            print(f"\nArquivo '{filename}' Baixado com sucesso.")
            # Faça algo com o conteúdo do arquivo, como salvá-lo localmente
        else:
            print(f"\nArquivo '{filename}' Não encontrado.")

    def register_file_interest(self, server):
        filename = input("Digite o nome do arquivo em que você está interessado: ")
        valid_time = int(input("Digite o tempo válido para o interesse (em segundos): "))
        server.register_interest(self.client_id, filename, valid_time)
        print(f"\nInteresse registrado para arquivo '{filename}'")

    def unregister_file_interest(self, server):
        filename = input("Digite o nome do arquivo para cancelar o interesse: ")
        server.unregister_interest(self.client_id, filename)
        print(f"\nInteresse cancelado para arquivo '{filename}'")


# Início do cliente
client_id = input("Digite o ID do cliente: ")
server_uri = input("Digite o URI do servidor: ")

client = Client(client_id)
client.start(server_uri)  # Inicia o cliente, fornecendo o URI do servidor


