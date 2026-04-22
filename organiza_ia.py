import streamlit as st
import anthropic

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="OrganizaIA",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Estilos visuales ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F5F0EB;
    color: #1C1C1C;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
}

/* Header hero */
.hero {
    background: linear-gradient(135deg, #2C5F2D 0%, #4A8B3F 60%, #97BC62 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem 2rem;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(44, 95, 45, 0.25);
}
.hero h1 {
    font-size: 2.8rem;
    margin-bottom: 0.3rem;
    color: white;
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1.1rem;
    opacity: 0.9;
    font-weight: 300;
    margin: 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Sección "Cómo funciona" */
.how-it-works {
    background: white;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 2rem;
    border-left: 5px solid #2C5F2D;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.how-it-works h3 {
    color: #2C5F2D;
    margin-top: 0;
    font-size: 1.3rem;
}

.step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 0.9rem;
}
.step-num {
    background: #2C5F2D;
    color: white;
    border-radius: 50%;
    width: 26px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
}

/* Chat */
.chat-container {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1.5rem;
}

.msg-user {
    background: #2C5F2D;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    margin: 0.5rem 0 0.5rem 3rem;
    font-size: 0.95rem;
    line-height: 1.5;
}
.msg-assistant {
    background: #F0F7EE;
    color: #1C1C1C;
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1.1rem;
    margin: 0.5rem 3rem 0.5rem 0;
    font-size: 0.95rem;
    line-height: 1.5;
    border-left: 3px solid #97BC62;
}
.msg-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    opacity: 0.55;
    margin-bottom: 4px;
}

/* Botón principal */
.stButton > button {
    background: linear-gradient(135deg, #2C5F2D, #4A8B3F) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(44,95,45,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(44,95,45,0.4) !important;
}

/* Input */
.stTextInput > div > div > input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 2px solid #E0EDD8 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #4A8B3F !important;
    box-shadow: 0 0 0 3px rgba(74,139,63,0.12) !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid #E8E2DB !important;
    margin: 1.5rem 0 !important;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 0.78rem;
    color: #888;
    margin-top: 2rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Estado de la sesión ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False

# ── Prompt del sistema ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un asistente de organización personal llamado OrganizaIA. Tu objetivo es ayudarme a construir hábitos de organización de forma progresiva. Comenzá haciéndome preguntas sobre mis rutinas, responsabilidades y dificultades actuales. Luego proponé pequeñas metas alcanzables (tentativas) que me acerquen a una organización equilibrada. Adaptá tu lenguaje para que sea claro, motivador y sin abrumar. Registrá mi progreso y ajustá las sugerencias según mis avances. Respondé siempre en español, con un tono cálido y alentador."""

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">✨ Powered by Claude AI</div>
    <h1>🌱 OrganizaIA</h1>
    <p>Tu asistente inteligente de organización personal.<br>
    Metas pequeñas, avances reales.</p>
</div>
""", unsafe_allow_html=True)

# ── Cómo funciona ─────────────────────────────────────────────────────────────
with st.expander("📖 ¿Cómo funciona OrganizaIA?", expanded=not st.session_state.started):
    st.markdown("""
    <div class="how-it-works">
        <h3>Tu camino hacia la organización</h3>
        <div class="step">
            <div class="step-num">1</div>
            <div><strong>Contá tu situación</strong> — OrganizaIA te hace preguntas sobre tus rutinas, responsabilidades y dificultades actuales para entender tu punto de partida.</div>
        </div>
        <div class="step">
            <div class="step-num">2</div>
            <div><strong>Recibí metas alcanzables</strong> — La IA propone pequeñas tentativas progresivas adaptadas a tu ritmo, no planes rígidos que abandonás a la semana.</div>
        </div>
        <div class="step">
            <div class="step-num">3</div>
            <div><strong>Avanzá con retroalimentación</strong> — Cada avance es celebrado y el plan se ajusta según tu progreso real, con mensajes motivadores personalizados.</div>
        </div>
        <hr>
        <p style="margin:0; color:#555; font-size:0.9rem;">
        🧠 <strong>Características clave:</strong> Personalización total · Progreso gradual y sostenible · Accesible desde cualquier navegador · Sin conocimientos técnicos requeridos
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Área de chat ──────────────────────────────────────────────────────────────
st.markdown("### 💬 Conversá con OrganizaIA")

# Mostrar historial
chat_html = '<div class="chat-container">'
if not st.session_state.messages:
    chat_html += '<p style="color:#aaa; text-align:center; font-size:0.9rem; margin:1rem 0;">Presioná el botón para comenzar tu plan de organización 👇</p>'
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="msg-label" style="text-align:right; padding-right:4px;">Vos</div><div class="msg-user">{msg["content"]}</div>'
        else:
            chat_html += f'<div class="msg-label" style="padding-left:4px;">OrganizaIA</div><div class="msg-assistant">{msg["content"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Botón de inicio ───────────────────────────────────────────────────────────
if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Comenzar mi plan de organización", use_container_width=True):
            st.session_state.started = True
            with st.spinner("OrganizaIA está pensando..."):
                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=600,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": "Hola, quiero empezar a organizarme mejor."}],
                )
                first_msg = response.content[0].text
                st.session_state.messages.append({"role": "user", "content": "Hola, quiero empezar a organizarme mejor."})
                st.session_state.messages.append({"role": "assistant", "content": first_msg})
            st.rerun()

# ── Input del usuario ─────────────────────────────────────────────────────────
if st.session_state.started:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Escribí tu mensaje...",
            placeholder="Ej: Tengo muchas tareas pendientes y no sé por dónde empezar...",
            height=90,
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Enviar ➤", use_container_width=False)

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("OrganizaIA está respondiendo..."):
            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=700,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages,
            )
            reply = response.content[0].text
            st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # Botón reiniciar
    if st.session_state.messages:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄 Reiniciar", use_container_width=True):
                st.session_state.messages = []
                st.session_state.started = False
                st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    OrganizaIA · Powered by Claude AI (Anthropic) · Gino Testa · Comisión: Prompt Engineering
</div>
""", unsafe_allow_html=True)
