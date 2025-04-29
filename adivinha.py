import streamlit as st
import random
from random import randint

# Inicialización del estado de sesión
def init_session_state():
    session_defaults = {
        'nickname': "",
        'control': 1,
        'num_maquina_soft': randint(1, 100),
        'num_maquina_hard': randint(1, 1000),
        'quem_adivinha': "",
        'nivel': 0,
        'tentativas': 0,
        'minimo': 1,
        'maximo': 100,
        'chute': 0,
        'chute_usuario': 0,
        'num_maquina': 0,
        'continuar': "",
        'etapa': "nickname",
        'feedback': "",
        'juego_terminado': False,
        'nuevo_intento': True
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def mostrar_feedback(feedback, color="#EE82EE", font_size="20px"):
    st.markdown(f"""
        <div style='font-size: {font_size}; color: {color}; text-align: center; font-family: "Press Start 2P", sans-serif;'>
            {feedback}
        </div>
    """, unsafe_allow_html=True)

def main():
    st.title("Adivinhe o número!")
    init_session_state()

    if st.session_state.etapa == "nickname":
        mostrar_pantalla_nickname()
    elif st.session_state.etapa == "escolha_modo":
        mostrar_pantalla_escolha_modo()
    elif st.session_state.etapa == "escolha_dificuldade":
        mostrar_pantalla_dificuldade()
    elif st.session_state.etapa == "maquina_adivinha":
        mostrar_pantalla_maquina_adivinha()
    elif st.session_state.etapa == "jogador_adivinha":
        mostrar_pantalla_jogador_adivinha()

def mostrar_pantalla_nickname():
    st.markdown("""
        <div style='font-size: 28px; font-family: "Press Start 2P", sans-serif; color: #FFA500; text-align: center; margin-bottom: 20px;'>
            Bem-vindo! Digite seu Nickname:
        </div>
    """, unsafe_allow_html=True)
    st.session_state.nickname = st.text_input("", key="nickname_input", placeholder="Ex: Jogador123")

    if st.session_state.nickname:
        st.session_state.etapa = "escolha_modo"
        st.rerun()

def mostrar_pantalla_escolha_modo():
    st.markdown(f"""
        <div style='font-size: 28px; font-family: "Press Start 2P", sans-serif; color: #FFA500; text-align: center; margin-bottom: 20px;'>
            Olá, {st.session_state.nickname}!
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Escolha quem vai adivinhar o número:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Eu quero adivinhar", key="jogador_button"):
            st.session_state.quem_adivinha = "jogador"
            st.session_state.etapa = "escolha_dificuldade"
            st.rerun()

    with col2:
        if st.button("A máquina adivinha", key="maquina_button"):
            st.session_state.quem_adivinha = "maquina"
            st.session_state.etapa = "escolha_dificuldade"
            st.rerun()

def mostrar_pantalla_dificuldade():
    st.markdown("""
        <div style='font-size: 24px; font-family: "Press Start 2P", sans-serif; color: #FF6347; text-align: center; margin-bottom: 20px;'>
            Escolha o nível de dificuldade:
        </div>
    """, unsafe_allow_html=True)

    st.session_state.nivel = st.radio(
        "Escolha o nível de dificuldade:",
        ("Normal", "Hard"),
        key="nivel_jogo",
        index=0,
        help="Escolha o nível que deseja jogar!"
    )

    if st.button("Continuar", key="btn_escolha_dificuldade"):
        st.session_state.control = 0
        st.session_state.tentativas = 0
        st.session_state.minimo = 1
        st.session_state.maximo = 100 if st.session_state.nivel == "Normal" else 1000
        st.session_state.juego_terminado = False

        if st.session_state.quem_adivinha == "maquina":
            st.session_state.etapa = "maquina_adivinha"
        else:
            # Generar un nuevo número para que adivine el jugador
            if st.session_state.nivel == "Normal":
                st.session_state.num_maquina = randint(1, 100)
            else:
                st.session_state.num_maquina = randint(1, 1000)
            st.session_state.etapa = "jogador_adivinha"
        
        st.rerun()

def mostrar_pantalla_maquina_adivinha():
    if st.session_state.nivel == "Normal":
        adivinhar_numero_soft()
    else:
        adivinhar_numero_hard()

def adivinhar_numero_soft():
    if not st.session_state.juego_terminado:
        if st.session_state.tentativas == 0 or st.session_state.nuevo_intento:
            st.session_state.chute = (st.session_state.minimo + st.session_state.maximo) // 2
            st.session_state.tentativas += 1
            st.session_state.nuevo_intento = False

        st.markdown(f"""
            <div style='font-size: 22px; font-family: "Press Start 2P", sans-serif; color: #32CD32; text-align: center;'>
                Tentativa {st.session_state.tentativas}/7
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
    O número que você pensou é maior, menor ou igual a <span style='color: #FF6347; font-size: 20px; font-weight: bold;'>{st.session_state.chute}</span>?
""", unsafe_allow_html=True)


        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Maior", key=f"maior_{st.session_state.tentativas}"):
                st.session_state.minimo = st.session_state.chute + 1
                st.session_state.nuevo_intento = True
                st.rerun()

        with col2:
            if st.button("Igual", key=f"igual_{st.session_state.tentativas}"):
                st.success(f"Adivinhei o número em {st.session_state.tentativas} tentativas!")
                st.session_state.juego_terminado = True
                st.session_state.nuevo_intento = False

        with col3:
            if st.button("Menor", key=f"menor_{st.session_state.tentativas}"):
                st.session_state.maximo = st.session_state.chute - 1
                st.session_state.nuevo_intento = True
                st.rerun()

        if st.session_state.tentativas >= 7 and not st.session_state.juego_terminado:
            st.error("Não consegui adivinhar o número em 7 tentativas. Você venceu!")
            st.session_state.juego_terminado = True

        if st.session_state.juego_terminado:
            st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")

def adivinhar_numero_hard():
    if not st.session_state.juego_terminado:
        if st.session_state.tentativas == 0 or st.session_state.nuevo_intento:
            st.session_state.chute = (st.session_state.minimo + st.session_state.maximo) // 2
            st.session_state.tentativas += 1
            st.session_state.nuevo_intento = False

        st.markdown(f"""
            <div style='font-size: 22px; font-family: "Press Start 2P", sans-serif; color: #FFD700; text-align: center;'>
                Tentativa {st.session_state.tentativas}/10
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
    O número que você pensou é maior, menor ou igual a <span style='color: #FF6347; font-size: 20px; font-weight: bold;'>{st.session_state.chute}</span>?
""", unsafe_allow_html=True)


        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Maior", key=f"maior_{st.session_state.tentativas}"):
                st.session_state.minimo = st.session_state.chute + 1
                st.session_state.nuevo_intento = True
                st.rerun()

        with col2:
            if st.button("Igual", key=f"igual_{st.session_state.tentativas}"):
                st.success(f"Adivinhei o número em {st.session_state.tentativas} tentativas!")
                st.session_state.juego_terminado = True
                st.session_state.nuevo_intento = False

        with col3:
            if st.button("Menor", key=f"menor_{st.session_state.tentativas}"):
                st.session_state.maximo = st.session_state.chute - 1
                st.session_state.nuevo_intento = True
                st.rerun()

        if st.session_state.tentativas >= 10 and not st.session_state.juego_terminado:
            st.error("Não consegui adivinhar o número em 10 tentativas. Você venceu!")
            st.session_state.juego_terminado = True

        if st.session_state.juego_terminado:
            st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")

            

def mostrar_pantalla_jogador_adivinha():
    if st.session_state.nivel == "Normal":
        conversa_adivinha_normal()
    else:
        conversa_adivinha_hard()

if "chute_normal" not in st.session_state:
    st.session_state.chute_normal = None
if "chute_hard" not in st.session_state:
    st.session_state.chute_hard = None

def conversa_adivinha_normal():
    if not st.session_state.juego_terminado:
        # Mensaje de introducción, centrado y con fuente vintage de jueguito
        st.markdown("""
            <div style='font-size: 24px; font-family: "Press Start 2P", sans-serif; color: #FFA500; text-align: center; margin-bottom: 20px;'>
                Escolheu modo normal, mamão com açúcar!
            </div>
        """, unsafe_allow_html=True)

        # Intentos restantes: texto centrado y en verde
        tentativas_restantes = 7 - st.session_state.tentativas
        st.markdown(f"""
            <div style='font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 10px; text-align: center;'>
                Você tem <strong>{tentativas_restantes}</strong> tentativas para adivinhar restantes.
            </div>
        """, unsafe_allow_html=True)


        # Campo de entrada del número
        chute = st.number_input(
            "Meu número é entre 1 e 100:",
            min_value=1,
            max_value=100,
            key="chute_normal",
            value=st.session_state.chute_normal if 'chute_normal' in st.session_state else None,  # Usar None para vaciar
            on_change=handle_chute  # Llamamos a la función para manejar el intento
        )

        # Crear un botón para enviar el número
        if st.button("Enviar", key="enviar_normal"):
            handle_chute()  # Llamamos al mismo manejador cuando presionamos el botón

        # Feedback: mensaje centrado y en amarillo brillante
        if st.session_state.feedback:
            st.markdown(f"""
                <div style='font-size: 20px; color: #EE82EE; text-align: center; font-family: "Press Start 2P", sans-serif;'>
                    {st.session_state.feedback}
                </div>
            """, unsafe_allow_html=True)

                
def handle_chute():
    # Verifica si estamos en el modo normal o hard
    if st.session_state.nivel == "Normal":
        chute = st.session_state.chute_normal  # Para el modo normal
    else:
        chute = st.session_state.chute_hard  # Para el modo hard

    # Solo procesamos si el número no es None y si no hemos agotado los intentos
    if chute is not None:
        st.session_state.tentativas += 1  # Incrementa el número de intentos
        st.write(f"Tentativas feitas: {st.session_state.tentativas}")  # Depuración

        # Compara el número ingresado con el número de la máquina
        if chute == st.session_state.num_maquina:
            st.success(f"Parabéns {st.session_state.nickname}! Adivinhou o número em {st.session_state.tentativas} tentativas!")
            st.session_state.juego_terminado = True
        elif chute < st.session_state.num_maquina:
            st.session_state.feedback = (f"Não é {chute}, meu número é maior!")  # Feedback actualizado
        else:
            st.session_state.feedback = (f"Não é {chute}, meu número é menor!")  # Feedback actualizado

        # Verificar si el jugador agotó los intentos
        if st.session_state.tentativas >= (7 if st.session_state.nivel == "Normal" else 10) and not st.session_state.juego_terminado:
            st.error(f"Tentativas esgotadas, meu número era {st.session_state.num_maquina}, jogue de novo!")
            st.session_state.juego_terminado = True

        # Borrar el número ingresado (esto lo hacemos estableciendo el valor a None)
        if st.session_state.nivel == "Normal":
            st.session_state.chute_normal = None  # Para el modo normal
        else:
            st.session_state.chute_hard = None  # Para el modo hard

    if st.session_state.juego_terminado:
        st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")



def conversa_adivinha_hard():
    if not st.session_state.juego_terminado:
        # Mensaje de introducción, centrado y con fuente vintage de jueguito
        st.markdown("""
            <div style='font-size: 24px; font-family: "Press Start 2P", sans-serif; color: #FFA500; text-align: center; margin-bottom: 20px;'>
                Escolheu modo hard, só os bravos que comem a sopa!
            </div>
        """, unsafe_allow_html=True)

        # Intentos restantes: texto centrado y en verde
        tentativas_restantes = 10 - st.session_state.tentativas
        st.markdown(f"""
            <div style='font-size: 18px; font-weight: bold; color: #4CAF50; margin-bottom: 10px; text-align: center;'>
                Você tem <strong>{tentativas_restantes}</strong> tentativas para adivinhar restantes.
            </div>
        """, unsafe_allow_html=True)

        # Campo de entrada del número
        chute = st.number_input(
            "Meu número é entre 1 e 1000:",
            min_value=1,
            max_value=1000,
            key="chute_hard",
            value=st.session_state.chute_hard if 'chute_hard' in st.session_state else None,  # Usar None para vaciar
            on_change=handle_chute  # Llamamos a la función para manejar el intento
        )

        # Crear un botón para enviar el número
        if st.button("Enviar", key="enviar_hard"):
            handle_chute()  # Llamamos al mismo manejador cuando presionamos el botón

        # Feedback: mensaje centrado y en amarillo brillante
        if st.session_state.feedback:
            st.markdown(f"""
                <div style='font-size: 20px; color: #EE82EE; text-align: center; font-family: "Press Start 2P", sans-serif;'>
                    {st.session_state.feedback}
                </div>
            """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
