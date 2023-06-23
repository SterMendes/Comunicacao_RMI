import Pyro4
import time

@Pyro4.expose
class FileServer:
    def __init__(self):
        self.files = {}  # Dicionário para armazenar os arquivos disponíveis
        self.interests = {}  # Dicionário para armazenar os interesses dos clientes

    def upload_file(self, filename, file_content):
        self.files[filename] = file_content  # Faz o upload de um arquivo para ser compartilhado
        self.notify_interests(filename)  # Notifica os clientes interessados sobre o novo arquivo disponível

    def get_available_files(self):
        return list(self.files.keys())  # Retorna a lista de arquivos disponíveis

    def download_file(self, filename):
        return self.files.get(filename)  # Retorna o conteúdo de um arquivo específico

    def register_interest(self, client_id, filename, valid_time):
        valid_until = time.time() + valid_time  # Calcula o tempo válido para o interesse
        self.interests.setdefault(filename, {})[client_id] = valid_until  # Registra o interesse do cliente no arquivo

    def unregister_interest(self, client_id, filename):
        if filename in self.interests:
            self.interests[filename].pop(client_id, None)  # Cancela o interesse do cliente no arquivo

    def notify_interests(self, filename):
        if filename in self.interests:
            for client_id, valid_until in self.interests[filename].items():
                if time.time() < valid_until:
                    try:
                        client = Pyro4.Proxy(client_id)  # Cria um proxy para se comunicar com o cliente
                        client.notify_event(filename)  # Chama o método do cliente para enviar a notificação
                    except Pyro4.errors.CommunicationError:
                        print(f"Falha ao notificar o cliente {client_id}")
                else:
                    self.interests[filename].pop(client_id, None)  # Remove o interesse expirado

# Inicia o servidor
daemon = Pyro4.Daemon()
file_server = FileServer()
uri = daemon.register(file_server)  # Registra a instância do servidor no daemon

print("URI do servidor:", uri)

# Inicia o loop para receber solicitações dos clientes
daemon.requestLoop()


