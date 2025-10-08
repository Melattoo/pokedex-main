# 🧠 Pokedex Analytics - Projeto de Visualização de Dados Pokémon 

## 📋 Descrição do Projeto

**Pokedex Analytics** é uma aplicação web interativa desenvolvida em **Streamlit** que utiliza a **PokéAPI** para explorar e visualizar dados do universo Pokémon através de gráficos e análises estatísticas.  
O objetivo é transformar dados brutos da API em **insights visuais intuitivos e informativos**, demonstrando o poder da análise de dados aplicada de forma lúdica e educativa.

---

## 🎯 Objetivos

- Criar visualizações interativas e informativas sobre Pokémon  
- Demonstrar diferentes técnicas de análise de dados  
- Fornecer uma ferramenta educacional para fãs de Pokémon  
- Explorar as capacidades do **Streamlit** para dashboards analíticos  

---

## 📊 Escopo de Funcionalidades

### ⚔️ 1. **Comparação de Atributos (Stats)**
- **Gráfico:** Radar (Spider Chart) ou Barras agrupadas  
- **Dados:** HP, Ataque, Defesa, Velocidade, Ataque Especial, Defesa Especial  
- **Funcionalidade:** Comparar estatísticas de múltiplos Pokémon selecionados  
- **Insight:** Permite avaliar o equilíbrio e o estilo de combate de cada Pokémon


### 🧬 2. **Distribuição de Tipos de Pokémon**
- **Gráfico:** Barra ou Pizza  
- **Descrição:** Mostra quantos Pokémon pertencem a cada tipo (Fogo, Água, Grama, etc.)  
- **Insight:** Identificar os tipos mais e menos comuns  

### 🌟 3.**Análise Individual de Pokémon**
- **Gráfico:** Vários gráficos menores e texto informativo. O gráfico principal pode ser um Radar (Spider Chart) ou um gráfico de barras comparando os atributos do Pokémon selecionado com a média geral de todos os Pokémon, ou da sua própria geração/tipo. 
- **Análise:** Uma visão completa das características de um Pokémon específico, escolhido pelo usuário. A análise deve compilar e exibir dados como, dados basicos (nome, numero da Pokédex), estatísticas detalhadas (os atributos base (HP, Ataque, Defesa, etc.)), habilidades com uma lista das habilidades do Pokémon, com uma breve descrição de cada uma e a sua cadeia evolutiva. 
- **Insight:** O usuário obtém uma compreensão profunda e imediata de um Pokémon em particular. 

### ⚖️ 4. **Peso x Altura - Relação de Proporções**
- **Gráfico:** Dispersão (Scatter Plot)  
- **Análise:** Relação entre peso e altura, com agrupamento por tipo primário  
- **Insight:** Revela quais tipos tendem a ter maior densidade corporal (ex.: Pokémon de Pedra e Aço mais pesados em relação à altura)  

### 🔥 5. **Média de Ataque por Tipo**
- **Gráfico:** Barras horizontais  
- **Análise:** Calcula a média do atributo de ataque por tipo  
- **Aplicação:** Descobrir quais tipos são naturalmente mais ofensivos  

### 🧠 6. **Correlação entre Atributos**
- **Gráfico:** Heatmap (Mapa de calor)  
- **Análise:** Correlação entre todos os atributos principais  
- **Insight:** Identificar relações entre diferentes estatísticas  

### 🌍 7. **Pokémon por Região (Geração)**
- **Gráfico:** Barras empilhadas ou linha temporal  
- **Contexto:** Evolução do número de Pokémon através das gerações  

### 🏆 8. **Top 10 Pokémon por Atributo**
- **Gráfico:** Barras verticais  
- **Rankings:** HP, Ataque, Defesa, Velocidade, Ataque Especial, Defesa Especial  
- **Funcionalidade:** Identificar os Pokémon mais fortes em cada categoria  

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|-------------|--------|
| **Streamlit** | Criação da aplicação web interativa |
| **PokéAPI** | Fonte de dados principal |
| **Pandas** | Manipulação e análise de dados |
| **Plotly / Matplotlib** | Visualizações e gráficos |
| **Requests** | Requisições HTTP para a API |

---

## 📈 Metodologia

1. **Coleta de Dados:** Extração das informações diretamente da PokéAPI  
2. **Processamento:** Limpeza e estruturação dos dados para análise  
3. **Análise:** Cálculo de métricas e estatísticas descritivas  
4. **Visualização:** Criação de gráficos interativos e comparativos  
5. **Apresentação:** Dashboard unificado desenvolvido com Streamlit  

---

## 🎮 Público-Alvo

- Fãs de Pokémon interessados em dados e estatísticas  
- Estudantes de análise de dados e visualização  
- Desenvolvedores que desejam integrar APIs em seus projetos  
- Entusiastas de Data Science em busca de projetos práticos e divertidos  

---

## 🚀 Próximos Passos

O projeto será desenvolvido **incrementalmente**, começando pelas visualizações mais simples e evoluindo para análises mais complexas.  
Cada etapa incluirá melhorias na experiência do usuário, estrutura de código e eficiência das requisições à API.

---


