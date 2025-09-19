import streamlit as st

st.title("BOT de Apoio Aviator 🎲✈️")

# Histórico de resultados
if "history" not in st.session_state:
    st.session_state.history = []

novo = st.text_input("Digite o último resultado (ex: 6.54):")

if st.button("Adicionar"):
    try:
        val = float(novo)
        st.session_state.history.append(val)
    except:
        st.warning("Digite um número válido")

# Mostrar histórico
st.subheader("Histórico")
st.write(st.session_state.history[-20:])  # últimos 20

# Simulação simples (estatísticas empíricas)
if st.session_state.history:
    data = st.session_state.history[-50:]  # últimos 50
    n = len(data)
    p_low = sum(x < 1.2 for x in data)/n
    p_mid = sum(1.2 <= x < 2 for x in data)/n
    p_med = sum(2 <= x < 5 for x in data)/n
    p_high = sum(x >= 5 for x in data)/n

    st.subheader("Probabilidades (últimos 50)")
    st.write({
        "<1.2x": round(p_low*100, 1),
        "1.2–2.0x": round(p_mid*100, 1),
        "2.0–5.0x": round(p_med*100, 1),
        "5.0x+": round(p_high*100, 1),
    })

    # Sugestão simples
    if p_low > 0.35:
        sugestao = "Alta chance de crash baixo — melhor evitar a próxima rodada."
    elif p_mid > 0.35:
        sugestao = "Boa chance até 2x — cashout rápido em 1.5x recomendado."
    elif p_high > 0.15:
        sugestao = "Alguma chance de rodada longa — arriscar até 2x ou 3x."
    else:
        sugestao = "Situação neutra — entrar apenas com valor pequeno."

    st.subheader("Sugestão do BOT")
    st.success(sugestao)
