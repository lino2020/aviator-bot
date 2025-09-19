import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BOT Aviator", page_icon="✈️", layout="centered")

st.title("✈️ BOT de Apoio Aviator 🎲")

# Histórico salvo na sessão
if "history" not in st.session_state:
    st.session_state.history = []

novo = st.text_input("Digite o último resultado (ex: 6.54):")

if st.button("Adicionar resultado"):
    try:
        val = float(novo)
        st.session_state.history.append(val)
    except:
        st.warning("Digite um número válido")

if st.session_state.history:
    st.subheader("📊 Histórico (últimos 20)")
    st.write(st.session_state.history[-20:])

    # Converter para DataFrame
    data = pd.DataFrame(st.session_state.history, columns=["Multiplicador"])

    # Mostrar gráfico de linha
    st.line_chart(data.tail(50))

    # Estatísticas últimas 50
    ultimos = data.tail(50)["Multiplicador"]
    n = len(ultimos)
    p_low = sum(x < 1.2 for x in ultimos)/n
    p_mid = sum(1.2 <= x < 2 for x in ultimos)/n
    p_med = sum(2 <= x < 5 for x in ultimos)/n
    p_high = sum(x >= 5 for x in ultimos)/n

    st.subheader("📈 Probabilidades estimadas (últimos 50)")
    st.write({
        "<1.2x": f"{p_low*100:.1f}%",
        "1.2–2.0x": f"{p_mid*100:.1f}%",
        "2.0–5.0x": f"{p_med*100:.1f}%",
        "5.0x+": f"{p_high*100:.1f}%",
    })

    # Sugestão baseada em regra simples
    if p_low > 0.35:
        sugestao = "⚠️ Alta chance de crash baixo — melhor evitar a próxima rodada."
        cor = "red"
    elif p_mid > 0.35:
        sugestao = "✅ Boa chance até 2x — cashout rápido em 1.5x recomendado."
        cor = "green"
    elif p_high > 0.15:
        sugestao = "🎯 Alguma chance de rodada longa — arriscar até 2x ou 3x."
        cor = "blue"
    else:
        sugestao = "ℹ️ Situação neutra — entrar apenas com valor pequeno."
        cor = "orange"

    st.subheader("🤖 Sugestão do BOT")
    st.markdown(f"<h3 style='color:{cor}'>{sugestao}</h3>", unsafe_allow_html=True)

else:
    st.info("Insira pelo menos um resultado para começar a análise.")
