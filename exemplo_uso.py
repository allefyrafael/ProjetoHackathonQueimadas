"""
Exemplos de uso da API NASA Fire Footprints
"""

from nasa_fire_footprints import NASAFireFootprintsAPI


def exemplo_basico():
    """Exemplo básico - América do Sul, últimas 24h, MODIS"""
    print("=" * 60)
    print("Exemplo 1: Básico - América do Sul, 24h, MODIS")
    print("=" * 60)
    
    api = NASAFireFootprintsAPI()
    kml_content, info = api.get_south_america_fire_footprints(
        date_span='24h',
        sensor='c6.1',
        save_to_file='exemplo1_24h_modis.kml'
    )
    print(f"Arquivo salvo: exemplo1_24h_modis.kml\n")


def exemplo_48h_viirs():
    """Exemplo - América do Sul, últimas 48h, VIIRS Suomi-NPP"""
    print("=" * 60)
    print("Exemplo 2: América do Sul, 48h, VIIRS Suomi-NPP")
    print("=" * 60)
    
    api = NASAFireFootprintsAPI()
    kml_content, info = api.get_south_america_fire_footprints(
        date_span='48h',
        sensor='suomi-npp-viirs-c2',
        save_to_file='exemplo2_48h_viirs.kml'
    )
    print(f"Arquivo salvo: exemplo2_48h_viirs.kml\n")


def exemplo_7d_multiplos_sensores():
    """Exemplo - América do Sul, últimos 7 dias, múltiplos sensores"""
    print("=" * 60)
    print("Exemplo 3: América do Sul, 7 dias, múltiplos sensores")
    print("=" * 60)
    
    api = NASAFireFootprintsAPI()
    
    sensores = [
        ('c6.1', 'modis'),
        ('suomi-npp-viirs-c2', 'viirs_suomi'),
        ('noaa-20-viirs-c2', 'viirs_noaa20'),
        ('noaa-21-viirs-c2', 'viirs_noaa21')
    ]
    
    for sensor, nome in sensores:
        print(f"\nObtendo dados do sensor: {sensor}")
        try:
            kml_content, info = api.get_south_america_fire_footprints(
                date_span='7d',
                sensor=sensor,
                save_to_file=f'exemplo3_7d_{nome}.kml'
            )
            print(f"✓ Arquivo salvo: exemplo3_7d_{nome}.kml")
        except Exception as e:
            print(f"✗ Erro ao obter dados do sensor {sensor}: {e}")


def exemplo_outras_regioes():
    """Exemplo - Diferentes regiões"""
    print("=" * 60)
    print("Exemplo 4: Diferentes regiões")
    print("=" * 60)
    
    api = NASAFireFootprintsAPI()
    
    regioes = [
        'south_america',
        'central_america',
        'europe'
    ]
    
    for regiao in regioes:
        print(f"\nObtendo dados da região: {regiao}")
        try:
            kml_content, info = api.get_fire_footprints(
                region=regiao,
                date_span='24h',
                sensor='c6.1',
                save_to_file=f'exemplo4_{regiao}.kml'
            )
            print(f"✓ Arquivo salvo: exemplo4_{regiao}.kml")
        except Exception as e:
            print(f"✗ Erro ao obter dados da região {regiao}: {e}")


if __name__ == "__main__":
    try:
        # Descomente o exemplo que deseja executar:
        
        exemplo_basico()
        # exemplo_48h_viirs()
        # exemplo_7d_multiplos_sensores()
        # exemplo_outras_regioes()
        
    except ValueError as e:
        print(f"\n✗ Erro de configuração: {e}")
        print("\nCertifique-se de que a variável de ambiente MAP_KEY está configurada.")
        print("Obtenha uma chave em: https://firms.modaps.eosdis.nasa.gov/api/map_key")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")

