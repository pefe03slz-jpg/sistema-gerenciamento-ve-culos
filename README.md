Sistema de Gerenciamento de Carros
Este projeto é uma aplicação desenvolvida em Python utilizando a biblioteca Tkinter para criar uma interface gráfica de gerenciamento de carros em serviço. O sistema permite cadastrar, editar e remover carros, além de gerenciar vendedores e acompanhar o status de cada veículo.

O programa armazena os dados em arquivos JSON, garantindo persistência entre execuções. São utilizados dois arquivos principais: carros_data.json para os registros dos veículos e vendedores_data.json para a lista de vendedores. Caso os arquivos não existam, o sistema inicializa com dados de exemplo.

Entre as funcionalidades disponíveis estão a exibição dos carros em uma tabela interativa, pesquisa por placa, vendedor ou status, adição de novos registros com validação, edição de informações já cadastradas e remoção automática de veículos finalizados. Também é possível gerenciar vendedores, adicionando ou removendo nomes conforme necessário.

Para executar o sistema, basta ter Python 3 instalado e rodar o arquivo principal do projeto. A interface gráfica será aberta e estará pronta para uso imediato.

OBS: carros_data.json e vendedores_data.json não representam dados reais.
