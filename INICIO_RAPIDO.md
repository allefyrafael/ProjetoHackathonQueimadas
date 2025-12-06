# 🚀 Início Rápido - Visualização de Dados NASA

## Passo 1: Obter Dados da NASA

```bash
# Configure a chave da API da NASA
$env:MAP_KEY="sua_chave_nasa_aqui"

# Execute o script para baixar os dados
python nasa_fire_footprints.py
```

Isso criará o arquivo `fire_footprints_south_america.kml` na raiz do projeto.

## Passo 2: Iniciar o Servidor HTTP

**⚠️ IMPORTANTE:** Você DEVE usar um servidor HTTP. Não abra o arquivo HTML diretamente (file://)!

### Opção A: Servidor Completo (Recomendado)

```bash
python servidor_local.py
```

### Opção B: Servidor Simples (Alternativa)

```bash
python servidor_simples.py
```

## Passo 3: Acessar no Navegador

O servidor abrirá automaticamente, ou acesse manualmente:

```
http://localhost:8000/visualizar_kml_leaflet.html
```

## ✅ Pronto!

Agora você verá o mapa com as pegadas de incêndio da América do Sul.

## 🔧 Solução de Problemas

### Erro: "Porta 8000 já está em uso"
- Feche outros servidores rodando na porta 8000
- Ou edite `PORT = 8000` no arquivo do servidor para usar outra porta

### Erro: "Failed to fetch"
- Certifique-se de que está usando o servidor HTTP (não file://)
- Verifique se o arquivo `fire_footprints_south_america.kml` existe na raiz
- Verifique o console do navegador (F12) para mais detalhes

### Arquivo KML não aparece
- Execute primeiro: `python nasa_fire_footprints.py`
- Verifique se o arquivo foi criado na raiz do projeto

