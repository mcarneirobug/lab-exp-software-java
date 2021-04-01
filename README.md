<h1 align="center">
    <span>Laboratório de Experimentação de Software</span>
</h1>
<p align="center">🚀 mineração de repositórios focado na linguagem Java para analise de métricas de software.</p>

![Badge](https://img.shields.io/github/languages/top/mcarneirobug/lab-exp-software-java)
![Badge](https://img.shields.io/github/issues-pr/mcarneirobug/lab-exp-software-java?logoColor=red)
![Badge](https://img.shields.io/github/issues-pr-closed-raw/mcarneirobug/lab-exp-software-java)
![Badge](https://img.shields.io/github/last-commit/mcarneirobug/lab-exp-software-java)
![Badge](https://img.shields.io/github/contributors/mcarneirobug/lab-exp-software-java)

Tabela de conteúdos
=================
<!--ts-->
   * [Sobre o projeto](#page_facing_up-sobre-o-projeto)
   * [Metodologia](#----hammer-metodologia)
      * [Seleção de Repositórios](#bulb-1-seleção-de-repositórios)
      * [Questões de pesquisa](#dart-2-questões-de-pesquisa)
      * [Definição de Métricas](#sparkles-3-definição-de-métricas)
      * [Coleta e Análise de Dados](#white_check_mark-4-coleta-e-análise-de-dados)
   * [Relatório final](#pencil-relatório-final)
   * [Processo de desenvolvimento](#octocat-processo-de-desenvolvimento)
   * [Alunos](#busts_in_silhouette-alunos)
   * [Professor responsável](#bust_in_silhouette-professor-responsável)
<!--te-->

### :page_facing_up: Sobre o projeto

No processo de desenvolvimento de sistemas open-source, em que diversos desenvolvedores contribuem em partes diferentes do código, um dos riscos a serem gerenciados diz respeito à evolução dos seus atributos de qualidade interna. Isto é, ao se adotar uma abordagem colaborativa, corre-se o risco de tornar vulnerável aspectos como modularidade, manutenabilidade, ou legalidade do software produzido. Para tanto, diversas abordagens modernas buscam aperfeiçoar tal processo, através da adoção de práticas relacionadas à revisão de código ou à análise estática através de ferramentas de CI/CD.

Neste contexto, o objetivo deste laboratório é analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionado-os com características do seu processo de desenvolvimento, sob a perspectiva de métricas de produto calculadas através da ferramenta <a href="https://github.com/mauricioaniche/ck">CK</a>.

### 

<h1 align="center">
    <span>:hammer: Metodologia</span>
</h1>

### :bulb: 1. Seleção de Repositórios

- Com o objetivo de analisar repositórios relevantes, escritos na linguagem estudada, coletaremos os top-1000 repositórios Java mais populares do GitHub, calculando cada uma das métricas definidas na Seção 3.

### :dart: 2. Questões de Pesquisa

- Desta forma, este laboratório tem o objetivo de responder às seguintes questões de pesquisa:

**RQ 01**. Qual a relação entre a **popularidade** dos repositórios e as métricas de qualidade? <br>
**RQ 02**. Qual a relação entre a **maturidade** do repositórios e as suas métricas de qualidade? <br>
**RQ 03**. Qual a relação entre a **atividade** dos repositórios e as suas métricas de qualidade? <br> 
**RQ 04**. Qual a relação entre o **tamanho** dos repositórios e as suas métricas de qualidade?  

### :sparkles: 3. Definição de Métricas

Para cada questão de pesquisa, realizaremos a comparação entre as características do processo de desenvolvimento dos repositórios e os seus valores obtidos para as seguintes métricas. Para as métricas de processo, define-se:

**Popularidade**: número de estrelas. <br>
**Maturidade**: idade (em anos) de cada repositório coletado. <br>
**Atividade**: número de releases. <br>
**Tamanho**: linhas de código (LOC) e linhas de comentários. <br>

- Por **métricas de qualidade**, entende-se:

**CBO**: Coupling between objects. <br>
**DIT**: Depth Inheritance Tree. <br>
**WMC**: Weight Method Class. <br>

- Para **cada** questão de pesquisa será analisado utilizando todas as métricas de qualidade.

### :white_check_mark: 4. Coleta e Análise de Dados 

Para análise das métricas de popularidade, atividade e maturidade, serão coletadas informações dos repositórios mais populares em Java, utilizando as APIs REST ou GraphQL do GitHub. Para medição dos valores de qualidade, utilizaremos uma ferramenta de análise estática de código (por exemplo, o <a href="https://github.com/mauricioaniche/ck">CK</a>).

### :pencil: Relatório final

Para cada uma questões de pesquisa, faça uma sumarização dos dados obtidos através de valores medianos (Links para um site externo.), por repositório. Mesmo que de forma informal, elabore hipóteses sobre o que você espera de resposta e tente analisar a partir dos valores obtidos. 

Elabore um documento que apresente (i) uma introdução simples com hipóteses informais; (ii) a metodologia que você utilizou para responder às questões de pesquisa; (iii) os resultados obtidos para cada uma delas; (iii) a discussão sobre o que você esperava como resultado (suas hipóteses) e os valores obtidos.  

### :octocat: Processo de desenvolvimento

- [X] Lab01S01: Lista dos 1000 repositórios Java + Script de Automação de clone e Coleta de Métricas (**6 pontos**)

- [X] Lab01S02: Arquivo csv com o resultado de todas as medições (**7 pontos**) 

- [X] Lab01S03: Análise de dados + elaboração do relatório final (**7 pontos**) 

`Prazo final: **31/03** | Valor total: **20 pontos** | Desconto de **0.5 pontos** por dia de atraso.`

### :busts_in_silhouette: Alunos

- <a href="https://github.com/mcarneirobug" target="_blank">Matheus Santos Rosa Carneiro</a>.
- <a href="https://github.com/raissavilela" target="_blank">Raíssa Carolina Vilela da Silva</a>.
- <a href="https://github.com/ovitorj" target="_blank">Vitor Augusto Alves de Jesus</a>.

### :bust_in_silhouette: Professor responsável

- Jose Laerte Pires Xavier Junior.

<h4 align="center"> 
	🚧  Spring 3 🚀 Finalizado ...  🚧
</h4>
