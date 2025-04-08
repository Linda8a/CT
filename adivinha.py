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
    st.session_state.nickname = st.text_input("Digite seu nickname: ")
    if st.session_state.nickname:
        st.session_state.etapa = "escolha_modo"
        st.rerun()

def mostrar_pantalla_escolha_modo():
    st.write(f"Olá, {st.session_state.nickname}!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Eu quero adivinhar"):
            st.session_state.quem_adivinha = "jogador"
            st.session_state.etapa = "escolha_dificuldade"
            st.rerun()
    with col2:
        if st.button("A máquina adivinha"):
            st.session_state.quem_adivinha = "maquina"
            st.session_state.etapa = "escolha_dificuldade"
            st.rerun()

def mostrar_pantalla_dificuldade():
    st.session_state.nivel = st.radio(
        "Escolha o nível de dificuldade:",
        ("1 (normal)", "2 (hard)"),
        key="nivel_jogo"
    )
    
    if st.button("Continuar", key="btn_escolha_dificuldade"):
        st.session_state.control = 0
        st.session_state.tentativas = 0
        st.session_state.minimo = 1
        st.session_state.maximo = 100 if st.session_state.nivel == "1 (normal)" else 1000
        st.session_state.juego_terminado = False
        
        if st.session_state.quem_adivinha == "maquina":
            st.session_state.etapa = "maquina_adivinha"
        else:
            # Generar nuevo número para que adivine el jugador
            if st.session_state.nivel == "1 (normal)":
                st.session_state.num_maquina = randint(1, 100)
            else:
                st.session_state.num_maquina = randint(1, 1000)
            st.session_state.etapa = "jogador_adivinha"
        st.rerun()

def mostrar_pantalla_maquina_adivinha():
    if st.session_state.nivel == "1 (normal)":
        adivinhar_numero_soft()
    else:
        adivinhar_numero_hard()

def adivinhar_numero_soft():
    if not st.session_state.juego_terminado:
        # Solo calculamos un nuevo chute si es el primer intento o si se ha cambiado el rango
        if st.session_state.tentativas == 0 or st.session_state.nuevo_intento:
            st.session_state.chute = (st.session_state.minimo + st.session_state.maximo) // 2
            st.session_state.tentativas += 1
            st.session_state.nuevo_intento = False

        # Mostramos la cantidad de intentos
        st.write(f"Tentativa {st.session_state.tentativas}/7")
        st.write(f"O número que você pensou é maior (M), menor (m) ou igual (=) a {st.session_state.chute}?")

        # Botones de respuesta
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Maior", key=f"maior_{st.session_state.tentativas}"):

                # Actualizamos el mínimo si la respuesta es "Maior"
                st.session_state.minimo = st.session_state.chute + 1
                st.session_state.nuevo_intento = True
                st.rerun()

        with col2:
            if st.button("Igual", key=f"igual_{st.session_state.tentativas}"):

                # Si el número es igual, el juego termina
                st.success(f"Adivinhei o número em {st.session_state.tentativas} tentativas!")
                st.session_state.juego_terminado = True  # Se marca como terminado
                st.session_state.nuevo_intento = False

        with col3:
            if st.button("Menor", key=f"menor_{st.session_state.tentativas}"):

                # Actualizamos el máximo si la respuesta es "Menor"
                st.session_state.maximo = st.session_state.chute - 1
                st.session_state.nuevo_intento = True
                st.rerun()

        # Verificación de intentos agotados (si se alcanzan 7 intentos sin adivinar)
        if st.session_state.tentativas >= 7 and not st.session_state.juego_terminado:
            st.error("Não consegui adivinhar o número em 7 tentativas. Você venceu!")
            st.session_state.juego_terminado = True

        # Si el juego ha terminado, preguntar si quiere jugar nuevamente
        if st.session_state.juego_terminado:
            st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")
            

def adivinhar_numero_hard():
    if not st.session_state.juego_terminado:
        # Solo calculamos un nuevo chute si es el primer intento o si se ha cambiado el rango
        if st.session_state.tentativas == 0 or st.session_state.nuevo_intento:
            st.session_state.chute = (st.session_state.minimo + st.session_state.maximo) // 2
            st.session_state.tentativas += 1
            st.session_state.nuevo_intento = False

        # Mostramos la cantidad de intentos
        st.write(f"Tentativa {st.session_state.tentativas}/10")
        st.write(f"O número que você pensou é maior (M), menor (m) ou igual (=) a {st.session_state.chute}?")

        # Botones de respuesta
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Maior", key=f"maior_{st.session_state.tentativas}"):

                # Actualizamos el mínimo si la respuesta es "Maior"
                st.session_state.minimo = st.session_state.chute + 1
                st.session_state.nuevo_intento = True
                st.rerun()

        with col2:
            if st.button("Igual", key=f"igual_{st.session_state.tentativas}"):

                # Si el número es igual, el juego termina
                st.success(f"Adivinhei o número em {st.session_state.tentativas} tentativas!")
                st.session_state.juego_terminado = True  # Se marca como terminado
                st.session_state.nuevo_intento = False

        with col3:
            if st.button("Menor", key=f"menor_{st.session_state.tentativas}"):

                # Actualizamos el máximo si la respuesta es "Menor"
                st.session_state.maximo = st.session_state.chute - 1
                st.session_state.nuevo_intento = True
                st.rerun()

        # Verificación de intentos agotados (si se alcanzan 10 intentos sin adivinar)
        if st.session_state.tentativas >= 10 and not st.session_state.juego_terminado:
            st.error("Não consegui adivinhar o número em 10 tentativas. Você venceu!")
            st.session_state.juego_terminado = True

        # Si el juego ha terminado, preguntar si quiere jugar nuevamente
        if st.session_state.juego_terminado:
            st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")
            

def mostrar_pantalla_jogador_adivinha():
    if st.session_state.nivel == "1 (normal)":
        conversa_adivinha_normal()
    else:
        conversa_adivinha_hard()

def conversa_adivinha_normal():
    if not st.session_state.juego_terminado:
        st.write("Escolheu modo normal, mamão com açúcar!")
        st.write("Faça seu melhor chute e adivinhe meu número!")

        if st.session_state.feedback:
            st.write(st.session_state.feedback)

        # Calculamos los intentos restantes
        tentativas_restantes = 7 - st.session_state.tentativas
        st.write(f"Você tem {tentativas_restantes} tentativas restantes.")

        chute = st.number_input(
            "Digite seu chute (1-100):",
            min_value=1,
            max_value=100,
            key="chute_normal",
            value=1  # Valor inicial ajustado a 1
        )

        if st.button("Enviar", key="enviar_normal"):
            if st.session_state.tentativas < 7 and not st.session_state.juego_terminado:  # Solo incrementar si no se alcanzó el límite
                st.session_state.tentativas += 1

                if chute == st.session_state.num_maquina:
                    st.success(f"Parabéns {st.session_state.nickname}! Adivinhou o número em {st.session_state.tentativas} tentativas!")
                    st.session_state.juego_terminado = True
                elif chute < st.session_state.num_maquina:
                    st.session_state.feedback = "Não, é maior!"
                else:
                    st.session_state.feedback = "Não, é menor!"

                # Verificar si el jugador agotó los intentos
                if st.session_state.tentativas >= 7 and not st.session_state.juego_terminado:
                    st.error(f"Tentativas esgotadas, meu número era {st.session_state.num_maquina}, jogue de novo!")
                    st.session_state.juego_terminado = True

            if st.session_state.juego_terminado:
                st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")
                

def conversa_adivinha_hard():
    if not st.session_state.juego_terminado:
        st.write("Escolheu modo hard, os bravos é que comem a sopa... boa sorte!")
        st.write("Faça seu melhor chute e adivinhe meu número!")

        if st.session_state.feedback:
            st.write(st.session_state.feedback)

        # Calculamos los intentos restantes
        tentativas_restantes = 10 - st.session_state.tentativas
        st.write(f"Você tem {tentativas_restantes} tentativas restantes.")

        chute = st.number_input(
            "Digite seu chute (1-1000):",
            min_value=1,
            max_value=1000,
            key="chute_hard",
            value=1  # Valor inicial ajustado a 1
        )

        if st.button("Enviar", key="enviar_hard"):
            if st.session_state.tentativas < 10 and not st.session_state.juego_terminado:  # Solo incrementar si no se alcanzó el límite
                st.session_state.tentativas += 1

                if chute == st.session_state.num_maquina:
                    st.success(f"Parabéns {st.session_state.nickname}! Adivinhou o número em {st.session_state.tentativas} tentativas!")
                    st.session_state.juego_terminado = True
                elif chute < st.session_state.num_maquina:
                    st.session_state.feedback = "Não, é maior!"
                else:
                    st.session_state.feedback = "Não, é menor!"

                # Verificar si el jugador agotó los intentos
                if st.session_state.tentativas >= 10 and not st.session_state.juego_terminado:
                    st.error(f"Tentativas esgotadas, meu número era {st.session_state.num_maquina}, jogue de novo!")
                    st.session_state.juego_terminado = True

            if st.session_state.juego_terminado:
                st.write("Obrigado por jogar! Pressione F5 para reiniciar o jogo.")
                
            else:
                st.rerun()



if __name__ == "__main__":
    main()
