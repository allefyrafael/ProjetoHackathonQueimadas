"""
Script para fazer requisições à API da NASA FIRMS para obter dados de pegadas de incêndio (KML).
Especificamente configurado para a América do Sul.
"""

import requests
import os
import zipfile
import io
import webbrowser
import time
import threading
import http.server
import socketserver
from pathlib import Path
from typing import Optional, Tuple


class NASAFireFootprintsAPI:
    """Classe para interagir com a API de pegadas de incêndio da NASA FIRMS."""
    
    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/kml_fire_footprints/"
    
    # Regiões disponíveis
    REGIONS = {
        'canada': 'canada',
        'alaska': 'alaska',
        'usa_contiguous_and_hawaii': 'usa_contiguous_and_hawaii',
        'central_america': 'central_america',
        'south_america': 'south_america',
        'europe': 'europe',
        'northern_and_central_africa': 'northern_and_central_africa',
        'southern_africa': 'southern_africa',
        'russia_asia': 'russia_asia',
        'south_asia': 'south_asia',
        'southeast_asia': 'southeast_asia',
        'australia_newzealand': 'australia_newzealand'
    }
    
    # Intervalos de data disponíveis
    DATE_SPANS = ['24h', '48h', '72h', '7d']
    
    # Sensores disponíveis
    SENSORS = {
        'modis': 'c6.1',
        'landsat': 'landsat',
        'suomi-npp-viirs': 'suomi-npp-viirs-c2',
        'noaa-20-viirs': 'noaa-20-viirs-c2',
        'noaa-21-viirs': 'noaa-21-viirs-c2'
    }
    
    def __init__(self, map_key: Optional[str] = None):
        """
        Inicializa a classe com a chave da API.
        
        Args:
            map_key: Chave da API da NASA. Se não fornecida, tenta obter da variável de ambiente MAP_KEY.
        """
        # Tentar obter a chave de diferentes formas
        if map_key:
            self.map_key = map_key
        else:
            # Tentar variável de ambiente
            self.map_key = os.getenv('MAP_KEY') or os.getenv('map_key')
            
            # Se ainda não encontrou, tentar ler de um arquivo .env (se existir)
            if not self.map_key:
                env_file = Path('.env')
                if env_file.exists():
                    try:
                        with open(env_file, 'r') as f:
                            for line in f:
                                if line.startswith('MAP_KEY='):
                                    self.map_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                    break
                    except:
                        pass
        
        # Validar chave
        if not self.map_key or not self.map_key.strip():
            raise ValueError(
                "Chave da API (MAP_KEY) não fornecida.\n"
                "Opções:\n"
                "1. Defina a variável de ambiente: $env:MAP_KEY='sua_chave' (PowerShell) ou export MAP_KEY='sua_chave' (Linux/Mac)\n"
                "2. Crie um arquivo .env com: MAP_KEY=sua_chave\n"
                "3. Passe como parâmetro: NASAFireFootprintsAPI(map_key='sua_chave')\n"
                "Obtenha uma chave em: https://firms.modaps.eosdis.nasa.gov/api/map_key"
            )
        
        self.map_key = self.map_key.strip()
    
    def get_fire_footprints(
        self,
        region: str = 'south_america',
        date_span: str = '24h',
        sensor: str = 'c6.1',
        save_to_file: Optional[str] = None
    ) -> Tuple[bytes, dict]:
        """
        Faz uma requisição à API da NASA para obter pegadas de incêndio em formato KML.
        
        Args:
            region: Região para buscar dados (padrão: 'south_america')
            date_span: Intervalo de tempo ('24h', '48h', '72h', '7d')
            sensor: Sensor a ser usado (padrão: 'c6.1' para MODIS)
            save_to_file: Caminho opcional para salvar o arquivo KML
        
        Returns:
            Tupla contendo (conteúdo KML em bytes, informações da resposta)
        """
        # Validação dos parâmetros
        if region not in self.REGIONS.values():
            raise ValueError(f"Região inválida. Use uma das seguintes: {list(self.REGIONS.values())}")
        
        if date_span not in self.DATE_SPANS:
            raise ValueError(f"Intervalo de data inválido. Use um dos seguintes: {self.DATE_SPANS}")
        
        # Construção da URL
        params = {
            'map_key': self.map_key,
            'region': region,
            'date_span': date_span,
            'sensor': sensor
        }
        
        print(f"Fazendo requisição à API da NASA...")
        print(f"Região: {region}")
        print(f"Intervalo: {date_span}")
        print(f"Sensor: {sensor}")
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            # Informações da resposta
            response_info = {
                'status_code': response.status_code,
                'content_type': response.headers.get('Content-Type', ''),
                'content_length': len(response.content),
                'url': response.url
            }
            
            print(f"\n✓ Requisição bem-sucedida!")
            print(f"Status: {response.status_code}")
            print(f"Tamanho do conteúdo: {response_info['content_length']} bytes")
            print(f"Tipo de conteúdo: {response_info['content_type']}")
            
            # Salvar arquivo se solicitado
            if save_to_file:
                # Remover arquivo existente se houver (sobrescrever)
                arquivo_path = Path(save_to_file)
                if arquivo_path.exists():
                    arquivo_path.unlink()
                    print(f"🗑️  Arquivo existente removido: {save_to_file}")
                
                # Verificar se é KMZ (arquivo ZIP comprimido)
                content_bytes = response.content
                is_kmz = content_bytes[:2] == b'PK'  # Assinatura ZIP
                
                if is_kmz:
                    print(f"⚠️  Arquivo recebido é KMZ (comprimido). Descomprimindo...")
                    # Descomprimir KMZ e extrair o KML
                    try:
                        with zipfile.ZipFile(io.BytesIO(content_bytes)) as kmz_file:
                            # Procurar arquivo .kml dentro do ZIP
                            kml_files = [f for f in kmz_file.namelist() if f.endswith('.kml')]
                            if kml_files:
                                # Extrair o primeiro arquivo KML encontrado
                                kml_content = kmz_file.read(kml_files[0])
                                with open(save_to_file, 'wb') as f:
                                    f.write(kml_content)
                                print(f"✓ Arquivo KML extraído e salvo em: {save_to_file}")
                            else:
                                # Se não encontrar KML, salvar como está
                                with open(save_to_file, 'wb') as f:
                                    f.write(content_bytes)
                                print(f"⚠️  Nenhum arquivo KML encontrado no KMZ. Arquivo salvo como: {save_to_file}")
                    except zipfile.BadZipFile:
                        # Se não for ZIP válido, salvar como está
                        with open(save_to_file, 'wb') as f:
                            f.write(content_bytes)
                        print(f"⚠️  Erro ao descomprimir. Arquivo salvo como: {save_to_file}")
                else:
                    # É KML direto
                    with open(save_to_file, 'wb') as f:
                        f.write(content_bytes)
                    print(f"✓ Arquivo KML salvo em: {save_to_file}")
            
            return response.content, response_info
            
        except requests.exceptions.RequestException as e:
            print(f"\n✗ Erro na requisição: {e}")
            raise
    
    def get_south_america_fire_footprints(
        self,
        date_span: str = '24h',
        sensor: str = 'c6.1',
        save_to_file: Optional[str] = None
    ) -> Tuple[bytes, dict]:
        """
        Método de conveniência para obter dados da América do Sul.
        
        Args:
            date_span: Intervalo de tempo ('24h', '48h', '72h', '7d')
            sensor: Sensor a ser usado (padrão: 'c6.1' para MODIS)
            save_to_file: Caminho opcional para salvar o arquivo KML
        
        Returns:
            Tupla contendo (conteúdo KML em bytes, informações da resposta)
        """
        return self.get_fire_footprints(
            region='south_america',
            date_span=date_span,
            sensor=sensor,
            save_to_file=save_to_file
        )


def iniciar_servidor_e_abrir_navegador(porta=8000):
    """Inicia o servidor HTTP e abre o navegador automaticamente."""
    
    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            if self.path.endswith('.kml'):
                self.send_header('Content-Type', 'application/vnd.google-earth.kml+xml')
            super().end_headers()
        
        def log_message(self, format, *args):
            # Silenciar logs do servidor
            pass
    
    def servidor_thread():
        try:
            with socketserver.TCPServer(("", porta), MyHTTPRequestHandler) as httpd:
                httpd.serve_forever()
        except OSError:
            # Porta já em uso, não fazer nada
            pass
    
    # Iniciar servidor em thread separada
    server_thread = threading.Thread(target=servidor_thread, daemon=True)
    server_thread.start()
    
    # Aguardar servidor iniciar
    time.sleep(1)
    
    # Abrir navegador
    url = f'http://localhost:{porta}/visualizar_kml_leaflet.html'
    try:
        webbrowser.open(url)
        print(f"\n🌐 Navegador aberto em: {url}")
        print(f"💡 O servidor está rodando em background. Feche este terminal para encerrar.")
    except Exception as e:
        print(f"\n⚠️  Não foi possível abrir o navegador automaticamente: {e}")
        print(f"   Acesse manualmente: {url}")


def main():
    """Função principal para demonstrar o uso da API."""
    try:
        # Inicializar a API
        api = NASAFireFootprintsAPI()
        
        # Obter dados da América do Sul
        # Você pode ajustar os parâmetros conforme necessário
        kml_content, info = api.get_south_america_fire_footprints(
            date_span='24h',  # Últimas 24 horas
            sensor='c6.1',    # MODIS
            save_to_file='fire_footprints_south_america.kml'
        )
        
        print(f"\n✓ Dados obtidos com sucesso!")
        print(f"O arquivo KML pode ser visualizado no Google Earth ou outros visualizadores KML.")
        
        # Verificar se o arquivo HTML existe
        html_file = Path('visualizar_kml_leaflet.html')
        if html_file.exists():
            print(f"\n🚀 Iniciando servidor e abrindo navegador...")
            iniciar_servidor_e_abrir_navegador()
            # Manter o programa rodando para o servidor continuar funcionando
            try:
                print(f"\n⏳ Pressione Ctrl+C para encerrar o servidor e sair.\n")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n\n🛑 Servidor encerrado.")
        else:
            print(f"\n⚠️  Arquivo visualizar_kml_leaflet.html não encontrado.")
            print(f"   Execute: python servidor_local.py para visualizar os dados.")
        
    except ValueError as e:
        print(f"\n✗ Erro de configuração: {e}")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")


if __name__ == "__main__":
    main()

