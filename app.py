import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Pokédex",
    page_icon="⚔️",
    layout="wide"
)

POKEMON_TYPE_COLORS = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "grass": "#78C850",
    "electric": "#F8D030",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "steel": "#B8B8D0",
    "dark": "#705848",
    "fairy": "#EE99AC",
}


@st.cache_data     #evitar requisicoes repetidas, salvar o cache
def get_pokemon_data(pokemon_name):
    if not pokemon_name:
        return None
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None
    
def get_pokemon_type_and_color(data):
    if data and "types" in data and len(data["types"]) > 0:
        main_type = data["types"][0]["type"]["name"]
        color = POKEMON_TYPE_COLORS.get(main_type, "#777777")
        return main_type, color
    return None, "#777777"

# lista de opções para o rádio button
funcionalidades = {
    "1. ⚔️ Comparação de Atributos (Status)": "comparacao_status",
    "3. 🌟 Análise Individual de Pokémon": "analise_individual",
    "2. 🧬 Distribuição de Tipos de Pokémon": "distribuicao_tipos",
    "3. ⚖️ Peso x Altura - Relação de Proporções": "peso_altura",
    "4. 🔥 Média de Ataque por Tipo": "media_ataque",
    "5. 🧠 Correlação entre Atributos": "correlacao_atributos",
    "6. 🌍 Pokémon por Região (Geração)": "pokemon_por_regiao",
    "7. 🏆 Top 10 Pokémon por Atributo": "top_10_atributos"
}

# st.radio é usado para criar botões de opção exclusivos
selected_feature = st.sidebar.radio(
    "Selecione uma Etapa",
    list(funcionalidades.keys()),
    format_func=lambda x: x.split(".")[1].strip() # Formata o nome na barra lateral
)

if funcionalidades[selected_feature] == "comparacao_status":   
    st.title("⚔️ Comparação de Atributos")

    col1, col2 = st.columns(2)
    with col1:
        pokemon_1_name = st.text_input("Primeiro Pokémon", placeholder="Ex: pikachu")
    with col2:
        pokemon_2_name = st.text_input("Segundo Pokémon", placeholder="Ex: charmander")

    #logica de comparacao - valida se ambos estao preenchidos e busca dados na API
    if st.button("Comparar"):
        if not pokemon_1_name or not pokemon_2_name:
            st.warning("Por favor, digite o nome de dois Pokémons para comparar.")
        else:
            data_1 = get_pokemon_data(pokemon_1_name)
            data_2 = get_pokemon_data(pokemon_2_name)

            if not data_1:
                st.error(f"Pokémon' {pokemon_1_name}' não encontrado.")
            if not data_2:
                st.error(f"Pokémon '{pokemon_2_name}' não encontrado.")

            if data_1 and data_2:
                pokemon_1_type, pokemon_1_color = get_pokemon_type_and_color(data_1)    
                pokemon_2_type, pokemon_2_color = get_pokemon_type_and_color(data_2)

                stats_1 = {stat["stat"]["name"]:stat["base_stat"] for stat in data_1["stats"]}
                stats_2 = {stat["stat"]["name"]:stat["base_stat"] for stat in data_2["stats"]}
                # formatar dados para o grafico
                comparison_data = {
                    "Estatística": list(stats_1.keys()),
                    data_1["name"].capitalize(): list(stats_1.values()),
                    data_2["name"].capitalize(): list(stats_2.values())
                }
                df = pd.DataFrame(comparison_data)

                #transformar os dados
                df_melted = df.melt(id_vars="Estatística", var_name="Pokémon", value_name="Valor")

                #pegando a cor para o grafico
                color_map ={
                    data_1["name"].capitalize(): pokemon_1_color,
                    data_2["name"].capitalize(): pokemon_2_color
                }

                #grafico
                fig = px.line_polar(
                    df_melted,
                    r="Valor",
                    theta="Estatística",
                    color="Pokémon",
                    line_close=True,
                    title=f"Comparativo de Estatística: {data_1['name'].capitalize()} vs {data_2['name'].capitalize()}",
                    color_discrete_map=color_map
                )
                fig.update_traces(fill="toself")

                #exibe o grafico
                st.plotly_chart(fig, use_container_width=True)

                #imagem do pokemon
                col_img1, col_img2 = st.columns(2)
                with col_img1:
                    sprite_url_1 = data_1["sprites"]["front_default"]
                    st.image(sprite_url_1, width= 500, caption=data_1["name"].capitalize())
                with col_img2:
                    sprite_url_2 = data_2["sprites"]["front_default"]
                    st.image(sprite_url_2, width= 500, caption=data_2["name"].capitalize())

#Distribuição de Tipos de Pokémon
elif funcionalidades[selected_feature] == "analise_individual":
    st.title("🌟 Análise Individual de Pokémon")
    st.write("Em breve, aqui você verá uma analise individual do Pokémon que escolher!")