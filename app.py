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

                # Layout reorganizado: gráfico no centro, imagens nas laterais
                col_img_left, col_chart, col_img_right = st.columns([1, 2, 1])
                
                with col_img_left:
                    sprite_url_1 = data_1["sprites"]["front_default"]
                    st.image(sprite_url_1, width=400, caption=data_1["name"].capitalize())
                
                with col_chart:
                    #exibe o grafico
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_img_right:
                    sprite_url_2 = data_2["sprites"]["front_default"]
                    st.image(sprite_url_2, width=400, caption=data_2["name"].capitalize())

#Distribuição de Tipos de Pokémon
elif funcionalidades[selected_feature] == "analise_individual":
    st.title("🌟 Análise Individual de Pokémon")
    
    # Função para buscar descrição em português
    def buscar_descricao_pt(species_data):
        """Busca a melhor descrição em português disponível"""
        if not species_data:
            return "Descrição não disponível para este Pokémon."
        
        versoes_prioridade = [
            "ultra-sun", "ultra-moon", "sun", "moon",
            "omega-ruby", "alpha-sapphire", "x", "y",
            "black-2", "white-2", "black", "white"
        ]
        
        for entry in species_data.get("flavor_text_entries", []):
            if entry["language"]["name"] == "pt" and entry["version"]["name"] in versoes_prioridade:
                return entry["flavor_text"].replace("\n", " ").replace("\x0c", " ")
        
        for entry in species_data.get("flavor_text_entries", []):
            if entry["language"]["name"] == "pt":
                return entry["flavor_text"].replace("\n", " ").replace("\x0c", " ")
        
        for entry in species_data.get("flavor_text_entries", []):
            if entry["language"]["name"] == "en":
                return f"(Em inglês) {entry['flavor_text'].replace(chr(12), ' ')}"
        
        return "Descrição não disponível para este Pokémon."
    
    # Input do Pokémon
    pokemon_nome = st.text_input(
        "Digite o nome ou número do Pokémon:",
        placeholder="Ex: pikachu, charmander, 25",
        key="individual_pokemon"
    )
    
    # Botões de Pokémon populares
    st.markdown("**🎮 Ou escolha um Pokémon popular:**")
    
    col_pop1, col_pop2, col_pop3, col_pop4 = st.columns(4)
    with col_pop1:
        if st.button("⚡ Pikachu", key="pop_pikachu", use_container_width=True):
            pokemon_nome = "pikachu"
    with col_pop2:
        if st.button("🔥 Charmander", key="pop_charmander", use_container_width=True):
            pokemon_nome = "charmander"
    with col_pop3:
        if st.button("🌿 Bulbasaur", key="pop_bulbasaur", use_container_width=True):
            pokemon_nome = "bulbasaur"
    with col_pop4:
        if st.button("💧 Squirtle", key="pop_squirtle", use_container_width=True):
            pokemon_nome = "squirtle"
    
    col_pop5, col_pop6, col_pop7, col_pop8 = st.columns(4)
    with col_pop5:
        if st.button("🐶 Eevee", key="pop_eevee", use_container_width=True):
            pokemon_nome = "eevee"
    with col_pop6:
        if st.button("🧬 Mewtwo", key="pop_mewtwo", use_container_width=True):
            pokemon_nome = "mewtwo"
    with col_pop7:
        if st.button("🐉 Dragonite", key="pop_dragonite", use_container_width=True):
            pokemon_nome = "dragonite"
    with col_pop8:
        if st.button("👻 Gengar", key="pop_gengar", use_container_width=True):
            pokemon_nome = "gengar"
    
    st.markdown("---")
    
    # Botão de análise principal
    analisar_clicado = st.button("🔍 Analisar Pokémon", key="btn_analisar", use_container_width=True)
    
    if analisar_clicado or (pokemon_nome and 'pokemon_data' not in locals() and st.session_state.get('auto_analisar', False)):
        # Força análise quando clica nos botões
        if not analisar_clicado and pokemon_nome:
            # Caso o botão popular foi clicado, recria o estado
            pass
        
        if not pokemon_nome:
            st.warning("⚠️ Por favor, digite o nome ou número de um Pokémon.")
        else:
            with st.spinner(f"🔄 Buscando dados de {pokemon_nome}..."):
                pokemon_data = get_pokemon_data(pokemon_nome)
                
                if not pokemon_data:
                    st.error(f"❌ Pokémon '{pokemon_nome}' não encontrado.")
                else:
                    # Busca dados da espécie
                    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_data['id']}"
                    try:
                        species_response = requests.get(species_url)
                        species_data = species_response.json() if species_response.status_code == 200 else None
                    except:
                        species_data = None
                    
                    tipo_principal, cor_tipo = get_pokemon_type_and_color(pokemon_data)
                    
                    # Layout em duas colunas
                    col_left, col_right = st.columns([1, 1])
                    
                    # COLUNA ESQUERDA
                    with col_left:
                        st.markdown(f"## #{pokemon_data['id']} - {pokemon_data['name'].capitalize()}")
                        
                        try:
                            imagem_url = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
                        except:
                            imagem_url = pokemon_data["sprites"]["front_default"]
                        
                        st.image(imagem_url, width=280)
                        
                        tipos = [t["type"]["name"].capitalize() for t in pokemon_data["types"]]
                        tipos_html = " ".join([f'<span style="background-color: {POKEMON_TYPE_COLORS.get(t.lower(), "#777777")}; padding: 4px 12px; border-radius: 20px; margin-right: 8px; color: white; font-weight: bold;">{t}</span>' for t in tipos])
                        st.markdown(f"**Tipo(s):** {tipos_html}", unsafe_allow_html=True)
                        
                        altura_m = pokemon_data["height"] / 10
                        peso_kg = pokemon_data["weight"] / 10
                        
                        col_altura, col_peso = st.columns(2)
                        with col_altura:
                            st.metric("📏 Altura", f"{altura_m:.1f} m")
                        with col_peso:
                            st.metric("⚖️ Peso", f"{peso_kg:.1f} kg")
                        
                        st.subheader("✨ Habilidades")
                        for ability in pokemon_data["abilities"]:
                            if ability["is_hidden"]:
                                st.markdown(f"- 🔮 **{ability['ability']['name'].capitalize()}** *(Oculta)*")
                            else:
                                st.markdown(f"- ⚡ {ability['ability']['name'].capitalize()}")
                        
                        if species_data:
                            st.subheader("📖 Descrição")
                            descricao = buscar_descricao_pt(species_data)
                            st.info(f"💬 {descricao}")
                            
                            for genus in species_data.get("genera", []):
                                if genus["language"]["name"] == "pt":
                                    st.markdown(f"**📌 Categoria:** {genus['genus']}")
                                    break
                    
                    # COLUNA DIREITA
                    with col_right:
                        stats = {
                            "HP": pokemon_data["stats"][0]["base_stat"],
                            "Ataque": pokemon_data["stats"][1]["base_stat"],
                            "Defesa": pokemon_data["stats"][2]["base_stat"],
                            "Ataque Esp": pokemon_data["stats"][3]["base_stat"],
                            "Defesa Esp": pokemon_data["stats"][4]["base_stat"],
                            "Velocidade": pokemon_data["stats"][5]["base_stat"]
                        }
                        
                        max_stat = max(stats.values())
                        
                        df_radar = pd.DataFrame({
                            "Atributos": list(stats.keys()),
                            "Valor": list(stats.values())
                        })
                        
                        fig_radar = px.line_polar(
                            df_radar,
                            r="Valor",
                            theta="Atributos",
                            line_close=True,
                            title="📊 Atributos Base",
                            range_r=[0, max_stat + 30],
                            template="plotly_dark"
                        )
                        
                        fig_radar.update_traces(
                            fill="toself",
                            line_color=cor_tipo,
                            line_width=3,
                            marker=dict(size=6, color=cor_tipo)
                        )
                        
                        # CORREÇÃO: Removeu 'weight' do tickfont
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, max_stat + 30],
                                    tickfont=dict(size=10),
                                    gridcolor="rgba(255,255,255,0.2)"
                                ),
                                angularaxis=dict(
                                    tickfont=dict(size=11),
                                    gridcolor="rgba(255,255,255,0.2)"
                                )
                            ),
                            height=450,
                            margin=dict(l=80, r=80, t=60, b=40),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)"
                        )
                        
                        st.plotly_chart(fig_radar, use_container_width=True)
                        
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        with col_stat1:
                            st.metric("❤️ HP", stats["HP"])
                            st.metric("⚔️ Ataque", stats["Ataque"])
                        with col_stat2:
                            st.metric("🛡️ Defesa", stats["Defesa"])
                            st.metric("🔮 Ataque Esp", stats["Ataque Esp"])
                        with col_stat3:
                            st.metric("✨ Defesa Esp", stats["Defesa Esp"])
                            st.metric("⚡ Velocidade", stats["Velocidade"])
                    
                    st.divider()
                    
                    # GRÁFICO DE BARRAS
                    st.subheader("📈 Comparativo de Atributos")
                    
                    df_stats = pd.DataFrame({
                        "Atributo": list(stats.keys()),
                        "Valor": list(stats.values())
                    }).sort_values("Valor", ascending=True)
                    
                    fig_bars = px.bar(
                        df_stats,
                        x="Valor",
                        y="Atributo",
                        orientation='h',
                        text="Valor",
                        color="Valor",
                        color_continuous_scale=["#2ecc71", "#f1c40f", "#e74c3c"]
                    )
                    
                    fig_bars.update_traces(textposition="outside", textfont=dict(size=12))
                    fig_bars.update_layout(
                        height=400,
                        xaxis=dict(title="Valor Base", range=[0, max_stat + 20]),
                        yaxis=dict(title="", categoryorder="total ascending"),
                        showlegend=False,
                        margin=dict(l=10, r=40, t=10, b=20)
                    )
                    
                    st.plotly_chart(fig_bars, use_container_width=True)
                    
                    # CADEIA EVOLUTIVA
                    st.subheader("🔄 Cadeia Evolutiva")
                    
                    if species_data and "evolution_chain" in species_data:
                        try:
                            evolution_url = species_data["evolution_chain"]["url"]
                            evo_response = requests.get(evolution_url)
                            evolution_data = evo_response.json() if evo_response.status_code == 200 else None
                            
                            if evolution_data:
                                evolucoes = []
                                
                                def extrair_evolucoes(chain):
                                    evolucoes.append(chain["species"]["name"])
                                    for evolve in chain.get("evolves_to", []):
                                        extrair_evolucoes(evolve)
                                
                                extrair_evolucoes(evolution_data["chain"])
                                
                                if len(evolucoes) > 1:
                                    cols = st.columns(len(evolucoes))
                                    for idx, evo in enumerate(evolucoes):
                                        with cols[idx]:
                                            evo_data = get_pokemon_data(evo)
                                            if evo_data:
                                                try:
                                                    evo_img = evo_data["sprites"]["other"]["official-artwork"]["front_default"]
                                                except:
                                                    evo_img = evo_data["sprites"]["front_default"]
                                                st.image(evo_img, width=120)
                                                st.caption(evo.capitalize())
                                else:
                                    st.info("🌟 Este Pokémon não tem evoluções conhecidas.")
                        except:
                            st.write("❌ Erro ao carregar cadeia evolutiva.")