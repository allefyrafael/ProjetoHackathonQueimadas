# API NASA - Fire Footprints

Este projeto faz requisições à API da NASA FIRMS para obter dados de pegadas de incêndio (fire footprints) em formato KML, especificamente para a América do Sul.

## 📋 Pré-requisitos

1. **Python 3.7+**
2. **Chave da API da NASA (MAP_KEY)**
   - Obtenha uma chave gratuita em: https://firms.modaps.eosdis.nasa.gov/api/map_key

## 🚀 Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🔑 Configuração

Você precisa configurar sua chave da API da NASA. Você pode fazer isso de duas formas:

### Opção 1: Variável de Ambiente (Recomendado)

**Windows (PowerShell):**
```powershell
$env:MAP_KEY="sua_chave_aqui"
```

**Windows (CMD):**
```cmd
set MAP_KEY=sua_chave_aqui
```

**Linux/Mac:**
```bash
export MAP_KEY="sua_chave_aqui"
```

### Opção 2: Passar como Parâmetro

Modifique o código para passar a chave diretamente:

```python
api = NASAFireFootprintsAPI(map_key="sua_chave_aqui")
```

## 📖 Uso

### Uso Básico

Execute o script principal:

```bash
python nasa_fire_footprints.py
```

Isso irá:
- Fazer uma requisição para a América do Sul
- Usar dados das últimas 24 horas
- Usar o sensor MODIS (c6.1)
- Salvar o resultado em `fire_footprints_south_america.kml`

### Uso Programático

```python
from nasa_fire_footprints import NASAFireFootprintsAPI

# Inicializar a API
api = NASAFireFootprintsAPI()

# Obter dados da América do Sul
kml_content, info = api.get_south_america_fire_footprints(
    date_span='48h',  # Últimas 48 horas
    sensor='c6.1',    # MODIS
    save_to_file='incendios_america_sul.kml'
)

# Ou usar o método genérico
kml_content, info = api.get_fire_footprints(
    region='south_america',
    date_span='72h',
    sensor='suomi-npp-viirs-c2',
    save_to_file='incendios.kml'
)
```

## 🌍 Parâmetros Disponíveis

### Regiões (REGION)
- `canada`
- `alaska`
- `usa_contiguous_and_hawaii`
- `central_america`
- `south_america` ⭐ (América do Sul)
- `europe`
- `northern_and_central_africa`
- `southern_africa`
- `russia_asia`
- `south_asia`
- `southeast_asia`
- `australia_newzealand`

### Intervalos de Tempo (DATE_SPAN)
- `24h` - Últimas 24 horas
- `48h` - Últimas 48 horas
- `72h` - Últimas 72 horas
- `7d` - Últimos 7 dias

### Sensores (SENSOR)
- `c6.1` - MODIS Near Real-Time, Real-Time e Ultra Real-Time
- `landsat` - LANDSAT Near Real-Time, Real-Time e Ultra Real-Time
- `suomi-npp-viirs-c2` - VIIRS Suomi-NPP Near Real-Time, Real-Time e Ultra Real-Time
- `noaa-20-viirs-c2` - VIIRS NOAA-20 Near Real-Time, Real-Time e Ultra Real-Time
- `noaa-21-viirs-c2` - VIIRS NOAA-21 Near Real-Time, Real-Time e Ultra Real-Time

**Nota:** Dados RT (Real-Time) e URT (Ultra Real-Time) são removidos quando as detecções NRT correspondentes são processadas ou quando RT/URT tem mais de 6 horas.

## 📁 Formato de Saída

A API retorna um arquivo KML que pode ser visualizado em:
- Google Earth
- QGIS
- Google Maps (via HTML fornecido neste projeto)
- Outros softwares que suportam formato KML

## 🗺️ Visualização dos Dados KML

Este projeto inclui arquivos HTML para visualizar os dados KML. Você tem duas opções:

### ✅ Opção 1: Leaflet (Recomendado - Sem Chave de API)

**Vantagens:** Não precisa de chave de API, totalmente gratuito e open-source!

**⚠️ IMPORTANTE:** Você DEVE usar um servidor HTTP. Não abra o arquivo HTML diretamente (file://)!

1. **Inicie o servidor HTTP local:**
   ```bash
   python servidor_local.py
   ```
   
   Ou use a versão simples:
   ```bash
   python servidor_simples.py
   ```

2. **Acesse no navegador:**
   - O navegador abrirá automaticamente em `http://localhost:8000/visualizar_kml_leaflet.html`
   - Ou acesse manualmente essa URL
   - O arquivo `fire_footprints_south_america.kml` será carregado automaticamente
   - Você também pode fazer upload de outros arquivos KML usando o botão de seleção

**Características:**
- ✅ Sem necessidade de chave de API
- ✅ Usa mapas do OpenStreetMap (gratuito)
- ✅ Upload de arquivos KML
- ✅ Visualização interativa com popups
- ✅ Estilização das pegadas de incêndio

### Opção 2: Google Maps (Requer Chave de API)

1. **Configure sua chave da API do Google Maps:**
   - Obtenha uma chave em: https://console.cloud.google.com/google/maps-apis
   - Habilite a "Maps JavaScript API"
   - Abra `visualizar_kml.html` e substitua `YOUR_API_KEY` pela sua chave

2. **Inicie o servidor local:**
   ```bash
   python servidor_local.py
   ```

3. **Acesse no navegador:**
   - Acesse: `http://localhost:8000/visualizar_kml.html`

**⚠️ Importante:** O Google Maps não carrega arquivos KML locais via `file://`. Você precisa usar um servidor HTTP local.

### Arquivos HTML Disponíveis

- **`visualizar_kml_leaflet.html`** ⭐ - Visualização usando Leaflet (sem chave de API)
- **`visualizar_kml.html`** - Visualização usando Google Maps (requer chave de API)
- **`visualizar_kml_local.html`** - Versão Google Maps com upload de arquivos

### Outras Opções de Visualização

- **Google Earth Desktop:** Baixe em https://www.google.com/earth/ e abra o arquivo `.kml` diretamente
- **QGIS:** Software GIS open-source que suporta KML
- **Google My Maps:** Importe o KML em https://www.google.com/maps/d/

## 🔗 Referências

- [Documentação da API FIRMS](https://firms.modaps.eosdis.nasa.gov/content/academy/data_api/firms_api_use.html)
- [Obter Chave da API](https://firms.modaps.eosdis.nasa.gov/api/map_key)
- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)

## 📝 Exemplo de Saída

```
Fazendo requisição à API da NASA...
Região: south_america
Intervalo: 24h
Sensor: c6.1

✓ Requisição bem-sucedida!
Status: 200
Tamanho do conteúdo: 12345 bytes
Tipo de conteúdo: application/vnd.google-earth.kml+xml
✓ Arquivo KML salvo em: fire_footprints_south_america.kml

✓ Dados obtidos com sucesso!
O arquivo KML pode ser visualizado no Google Earth ou outros visualizadores KML.
```

## ⚠️ Notas Importantes

- A chave da API é necessária para todas as requisições
- Os dados são atualizados regularmente pela NASA
- Dados RT/URT são temporários e podem ser removidos após 6 horas
- A API tem limites de taxa de requisição (consulte a documentação oficial)

