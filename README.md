# Detecção de manchas de óleo a partir de imagens capturadas com drone

O vazamento de óleo no Brasil foi um derrame de petróleo cru que atingiu mais de 2 mil quilômetros do litoral das regiões Nordeste e Sudeste do Brasil.
Os primeiros registros do derrame ocorreram no fim do mês de agosto de 2019.
Até 23 de outubro, a contaminação havia atingido mais de 200 localidades de vários municípios dos nove estados da Região Nordeste. 
Um relatório da Marinha estimou que mais de mil toneladas de óleo haviam sido retiradas das praias nordestinas até o dia 21 de outubro.
Segundo o Ministério Público Federal (MPF), trata-se do maior desastre ambiental já registrado no litoral brasileiro.

# Requisitos

- Python 3.8
- [Download do *dataset*](https://drive.google.com/drive/folders/15-ye1cz5ISQKyMY_9BAV217FLl_Z9Lcp?usp=sharing)

# Instalação

- Crie um *virtual environment* (**recomendado**)

No Windows:

```
> python -m venv venv
> venv\Scripts\activate.bat
```

No Linux:

```
> python3 -m venv venv
> source venv/bin/activate.sh
```

- Instale os pacotes necessários (no Linux utilize `pip3` ao invés de `pip`):

```
> pip install -r requirements.txt
```

⚠️Obs.: Caso não consiga instalar o `tensorflow`, faça o [download](https://pypi.org/project/tensorflow/#files) do arquivo `.whl` do `tensorflow 2.4.1` para `Python 3.8` 
correspondente ao seu sistema operacional e instale diretamente do arquivo:

```
> pip install <caminho do arquivo .whl>
```

# Configurar os parâmetros

Os parâmetros utilizados na busca devem estar definidos num arquivo `params.json` na mesma pasta onde o script é executado.
O repositório já contém um arquivo com os valores padrão. Para alterá-los basta editar o arquivo em um editor de texto. O arquivo deve descrever um objeto com as chaves de acordo com a tabela abaixo:
|               | Tipo   | Descrição                                                                               | Valor padrão                                                                          |
|---------------|--------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `conv_layers` | `int`  | Quantidade de camadas convolucionais                                                    | `[1, 2, 3]`                                                                           |
| `filters`     | `int`  | Quantidade de filtros em cada camada convolucional                                      | `[16, 32, 64]`                                                                        |
| `kernel_size` | `int`  | Tamanho do kernel das camadas convolucionais. Representa a altura e a largura do kernel | `[3, 5]`                                                                              |
| `dense_units` | `list` | Quantidade de neurônios em cada camada densa, respectivamente                           | `[[25], [50], [100], [25, 25], [50, 25], [50, 50], [100, 25], [100, 50], [100, 100]]` |

# *Grid search*

- Coloque os dados na pasta `../oil_spill_data`

```
└───📁brazil-oil-spill_data
|   └───📁dados
|       ├───📁train
|       │   ├───📁0
|       │   └───📁1
|       └───📁valid
|           ├───📁0
|           └───📁1
└───📁brazil-oil-spill
    └───📜main.py
    └───📜params.json
    └───📜requirements.txt
```

- Execute o *scrip* `main.py` (no Linux utilize `python3` ao invés de `python`)

```
> python main.py
```



Ao final da execução um arquivo `grid_search_result.json` contendo os resultados da busca será criado.
