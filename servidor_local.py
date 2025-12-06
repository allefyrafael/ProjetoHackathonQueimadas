"""
Servidor HTTP simples para servir os arquivos HTML e KML localmente.
Necessário porque navegadores não carregam arquivos KML locais via file://
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adicionar headers CORS para permitir requisições
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        # Adicionar header para arquivos KML
        if self.path.endswith('.kml'):
            self.send_header('Content-Type', 'application/vnd.google-earth.kml+xml')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Log personalizado
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    # Verificar se os arquivos necessários existem
    html_file_leaflet = Path('visualizar_kml_leaflet.html')
    kml_file = Path('fire_footprints_south_america.kml')
    
    print("=" * 60)
    print("🌐 Servidor HTTP Local - NASA Fire Footprints")
    print("=" * 60)
    
    # Verificar arquivos
    if not html_file_leaflet.exists():
        print("⚠️  Arquivo visualizar_kml_leaflet.html não encontrado!")
        return
    
    if not kml_file.exists():
        print("⚠️  Arquivo fire_footprints_south_america.kml não encontrado!")
        print("   Execute primeiro: python nasa_fire_footprints.py")
    else:
        print(f"✓ Arquivo KML encontrado: {kml_file}")
    
    # Tentar criar servidor
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"\n🌐 Servidor HTTP iniciado na porta {PORT}")
            print(f"📂 Servindo arquivos de: {os.getcwd()}")
            print(f"\n🔗 Acesse no navegador:")
            print(f"   http://localhost:{PORT}/visualizar_kml_leaflet.html")
            print(f"\n📋 Arquivos disponíveis:")
            print(f"   - visualizar_kml_leaflet.html")
            if kml_file.exists():
                print(f"   - fire_footprints_south_america.kml")
            print(f"\n💡 Pressione Ctrl+C para parar o servidor\n")
            
            # Abrir navegador automaticamente
            try:
                url = f'http://localhost:{PORT}/visualizar_kml_leaflet.html'
                print(f"🌐 Abrindo navegador em: {url}")
                webbrowser.open(url)
            except Exception as e:
                print(f"⚠️  Não foi possível abrir o navegador automaticamente: {e}")
                print(f"   Acesse manualmente: {url}")
            
            # Servir requisições
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e) or "address is already in use" in str(e):
            print(f"\n❌ Erro: A porta {PORT} já está em uso!")
            print(f"   Tente fechar outros servidores ou use uma porta diferente.")
            print(f"   Para usar outra porta, edite PORT = {PORT} no arquivo servidor_local.py")
        else:
            print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor encerrado pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()

