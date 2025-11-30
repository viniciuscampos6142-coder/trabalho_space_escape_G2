# trabalho_space_escape_G2
🔄 Fluxo de Funcionamento (Passo a Passo)

Inicialização: O Pygame inicia, carrega imagens (naves, meteoros, fundos) e sons. Define variáveis globais como vidas, pontuação e estado do jogo.

Estado MENU:

Exibe o título e opções.

Aguarda entrada do jogador:

Teclas 1 ou M: Inicia Modo 1 (Teclado ou Mouse).

Tecla 2: Inicia Modo 2 (Multiplayer).

Estado JOGANDO:

Atualização: Move naves, meteoros e tiros a cada frame.

Colisão: Checa se tiros acertam meteoros (ganha pontos) ou se meteoros acertam naves (perde vida).

Esquiva: Se um meteoro normal sai da tela sem bater, o jogador ganha 5 pontos.

Fases: Aumenta a dificuldade e muda o cenário conforme a pontuação sobe (350 e 700 pontos).

Estado TELA FINAL (Game Over/Victory):

Para a música e sons.

Exibe "GAME OVER" em vermelho (conforme sua alteração específica).

Mostra quem venceu (no Modo 2) ou a pontuação final (no Modo 1).

Aguarda qualquer tecla para voltar ao Menu.

🕹️ Modos de Jogo e Funcionalidades
1. Modo 1 Jogador (Single Player)
Objetivo: Sobreviver o máximo de tempo possível e acumular a maior pontuação (High Score).

Controles:

Teclado (Opção '1'): Setas direcionais para mover, Espaço ou RCTRL para atirar.

Mouse (Opção 'M'): A nave segue o cursor do mouse, atira com teclado.

Características:

O jogador começa com 3 vidas.

O jogo termina apenas quando as vidas chegam a zero.

Acumula pontos destruindo meteoros (+10) ou desviando deles (+5).

2. Modo 2 Jogadores (Competitivo / Eliminação)
Objetivo: Vencer o oponente, seja por Eliminação (ser o último vivo) ou por Pontuação (chegar a 1500 pontos primeiro).

Controles:

Player 1: Setas direcionais e RCTRL (Atirar).

Player 2: Teclas WASD e LCTRL (Atirar).

Características:

Vidas Separadas: Cada jogador tem seu próprio contador de 3 vidas.

Condição de Vitória 1 (Eliminação): Se um jogador perder todas as vidas, o jogo para e o outro é declarado vencedor.

Condição de Vitória 2 (Corrida de Pontos): Se alguém atingir 1500 pontos (Score Limite), o jogo para. Ganha quem tiver mais pontos no placar individual.

Tela Final: Sempre exibe "GAME OVER" no topo, mas detalha o vencedor ("Vencedor: Player X") abaixo.

🌟 Funcionalidades Gerais (Comuns a todos os modos)
Sistema de Fases:

Fase 1 (Selva): Velocidade normal.

Fase 2 (Céu - >350 pontos): Velocidade aumenta, fundo azul, novos meteoros.

Fase 3 (Espaço - >700 pontos): Velocidade máxima, meteoros finais, música intensa.

Meteoros Especiais (Power-ups): Existem meteoros coloridos que, ao serem destruídos ou colididos (dependendo da lógica de colisão), dão habilidades:

Tipo 3 (Magenta - Arma): Ativa tiro triplo rápido por 5 segundos.

Tipo 1 (Ciano - Teleporte): Move a nave para local aleatório e dá invencibilidade temporária.

Tipo 2 (Verde - Escudo): Dá invencibilidade temporária contra danos.

Correção de Pontuação:

Desviar de meteoros normais concede 5 pontos que aparecem no placar em tempo real.

Meteoros especiais não dão pontos de esquiva para evitar "farmar" itens sem pegá-los.

HUD (Interface):

Exibe Vidas, Pontuação Individual e Fase atual no topo da tela.

Mostra cronômetro regressivo quando uma arma especial está ativa.


https://youtu.be/Mj04-tDu32c?si=B-044NOzNZ9UFaXo
