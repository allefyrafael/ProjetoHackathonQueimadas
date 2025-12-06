"""
Script para descomprimir arquivo KMZ existente e extrair o KML
"""

import zipfile
import os
from pathlib import Path

def descomprimir_kmz(arquivo_kmz='fire_footprints_south_america.kml', arquivo_saida=None):
    """
    Descomprime um arquivo KMZ e extrai o KML.
    
    Args:
        arquivo_kmz: Caminho do arquivo KMZ (pode ter extensão .kml mas ser KMZ)
        arquivo_saida: Caminho de saída (se None, usa o mesmo nome com .kml)
    """
    if arquivo_saida is None:
        arquivo_saida = arquivo_kmz
    
    arquivo_path = Path(arquivo_kmz)
    
    if not arquivo_path.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_kmz}")
        return False
    
    # Verificar se é KMZ (ZIP)
    with open(arquivo_path, 'rb') as f:
        header = f.read(2)
    
    if header != b'PK':
        print(f"⚠️  Arquivo {arquivo_kmz} não parece ser um KMZ (ZIP).")
        print("   Tentando processar mesmo assim...")
    
    try:
        with zipfile.ZipFile(arquivo_path, 'r') as kmz_file:
            # Listar arquivos no ZIP
            arquivos = kmz_file.namelist()
            print(f"📦 Arquivos encontrados no KMZ: {arquivos}")
            
            # Procurar arquivo .kml dentro do ZIP
            kml_files = [f for f in arquivos if f.endswith('.kml')]
            
            if kml_files:
                # Extrair o primeiro arquivo KML encontrado
                kml_nome = kml_files[0]
                print(f"📄 Extraindo: {kml_nome}")
                
                kml_content = kmz_file.read(kml_nome)
                
                # Salvar o KML
                with open(arquivo_saida, 'wb') as f:
                    f.write(kml_content)
                
                print(f"✅ Arquivo KML extraído e salvo em: {arquivo_saida}")
                print(f"   Tamanho: {len(kml_content)} bytes")
                return True
            else:
                print(f"❌ Nenhum arquivo .kml encontrado no KMZ")
                return False
                
    except zipfile.BadZipFile:
        print(f"❌ Erro: {arquivo_kmz} não é um arquivo ZIP válido")
        print("   O arquivo pode já estar descomprimido ou estar corrompido")
        return False
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Descomprimindo arquivo KMZ")
    print("=" * 60)
    print()
    
    arquivo = 'fire_footprints_south_america.kml'
    
    if descomprimir_kmz(arquivo):
        print()
        print("✅ Processo concluído!")
        print("   Agora você pode visualizar o arquivo no navegador.")
        print("   Execute: python servidor_local.py")
    else:
        print()
        print("❌ Falha ao descomprimir o arquivo.")
        print("   Tente executar: python nasa_fire_footprints.py")
        print("   Isso irá baixar e descomprimir automaticamente.")

