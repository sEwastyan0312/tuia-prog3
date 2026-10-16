"""
Programa principal para el juego de Tateti con algoritmo minimax
Interfaz gráfica moderna usando pygame
"""
import pygame
import sys
from typing import Tuple, Optional, List
from tateti import Tateti
from estrategias import estrategia_aleatoria, estrategia_minimax

# Configuración de colores (paleta moderna)
COLORS = {
    'background': (248, 249, 250),      # Gris muy claro
    'grid': (52, 58, 64),               # Gris oscuro
    'x_color': (220, 53, 69),           # Rojo moderno
    'o_color': (13, 110, 253),          # Azul moderno
    'button': (108, 117, 125),          # Gris medio
    'button_hover': (73, 80, 87),       # Gris más oscuro
    'button_text': (255, 255, 255),     # Blanco
    'text': (33, 37, 41),               # Gris muy oscuro
    'accent': (111, 66, 193),           # Morado moderno
    'success': (25, 135, 84),           # Verde
    'warning': (255, 193, 7),           # Amarillo
}

# Configuración de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 630  # Aumentado para que se vea todo el texto
GRID_SIZE = 400
CELL_SIZE = GRID_SIZE // 3
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_SIZE) // 2
GRID_OFFSET_Y = 120  # Menos espacio arriba sin título

# Configuración de la barra superior
TOOLBAR_HEIGHT = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10

# Configuración de fuentes
pygame.font.init()
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 32)
FONT_SMALL = pygame.font.Font(None, 24)

class ModernTatetiGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tateti - Algoritmo Minimax")
        self.clock = pygame.time.Clock()
        
        # Estado del juego
        self.tateti = Tateti()
        self.current_state = self.tateti.estado_inicial
        
        # Configuración de juego
        self.game_mode = 'human_vs_ai'  # Modo por defecto
        self.ai_strategy = 'aleatoria'  # Estrategia por defecto
        self.human_player = 'X'  # Humano siempre es X
        self.game_active = True  # Juego activo por defecto
        self.game_over = False
        self.winner = None
        
        # UI elements
        self.buttons = self._create_buttons()
        self.dropdowns = self._create_dropdowns()
        self.hovered_element = None
        self.dropdown_open = None  # 'mode' o 'strategy' si hay uno abierto
        self.thinking = False
        
    def _create_buttons(self):
        """Crea los botones de la barra superior"""
        button_width = 200  # Botones aún más largos
        button_y = 20
        spacing = 20  # Espacio entre botones
        
        # El botón del medio (game_mode) está centrado en la ventana
        middle_x = WINDOW_WIDTH // 2 - button_width // 2
        
        return {
            'new_game': pygame.Rect(middle_x - button_width - spacing, button_y, button_width, BUTTON_HEIGHT),
            'game_mode': pygame.Rect(middle_x, button_y, button_width, BUTTON_HEIGHT),
            'ai_strategy': pygame.Rect(middle_x + button_width + spacing, button_y, button_width, BUTTON_HEIGHT),
        }
    
    def _create_dropdowns(self):
        """Crea las áreas de los menús desplegables"""
        dropdowns = {}
        
        # Dropdown para modo de juego
        mode_rect = self.buttons['game_mode']
        dropdowns['mode'] = {
            'rect': pygame.Rect(mode_rect.x, mode_rect.bottom, mode_rect.width, 3 * (BUTTON_HEIGHT + 2)),
            'options': [
                ('human_vs_human', 'Humano vs Humano'),
                ('human_vs_ai', 'Humano vs IA'),
                ('ai_vs_ai', 'IA vs IA')
            ]
        }
        
        # Dropdown para estrategia de IA
        strategy_rect = self.buttons['ai_strategy']
        dropdowns['strategy'] = {
            'rect': pygame.Rect(strategy_rect.x, strategy_rect.bottom, strategy_rect.width, 2 * (BUTTON_HEIGHT + 2)),
            'options': [
                ('aleatoria', 'Estrategia Aleatoria'),
                ('minimax', 'Algoritmo Minimax')
            ]
        }
        
        return dropdowns
    
    def _get_cell_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Convierte coordenadas de pantalla a posición de celda"""
        x, y = pos
        if (GRID_OFFSET_X <= x <= GRID_OFFSET_X + GRID_SIZE and 
            GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + GRID_SIZE):
            
            col = (x - GRID_OFFSET_X) // CELL_SIZE
            row = (y - GRID_OFFSET_Y) // CELL_SIZE
            return (row, col)
        return None
    
    def _draw_background(self):
        """Dibuja el fondo de la ventana"""
        self.screen.fill(COLORS['background'])
    
    def _draw_title(self):
        """Dibuja el título del juego (removido)"""
        pass
    
    def _draw_toolbar(self):
        """Dibuja la barra de herramientas superior"""
        # Fondo de la barra de herramientas
        toolbar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['grid'], toolbar_rect)
        
        # Botón Nueva Partida
        new_game_rect = self.buttons['new_game']
        color = COLORS['success'] if self.hovered_element == 'new_game' else COLORS['button']
        pygame.draw.rect(self.screen, color, new_game_rect, border_radius=12)
        text = FONT_SMALL.render('Nueva Partida', True, COLORS['button_text'])
        text_rect = text.get_rect(center=new_game_rect.center)
        self.screen.blit(text, text_rect)
        
        # Botón Modo de Juego (desplegable)
        mode_rect = self.buttons['game_mode']
        color = COLORS['accent'] if self.hovered_element == 'game_mode' or self.dropdown_open == 'mode' else COLORS['button']
        pygame.draw.rect(self.screen, color, mode_rect, border_radius=12)
        
        mode_texts = {
            'human_vs_human': 'Humano vs Humano',
            'human_vs_ai': 'Humano vs IA',
            'ai_vs_ai': 'IA vs IA'
        }
        text = FONT_SMALL.render(mode_texts[self.game_mode], True, COLORS['button_text'])
        text_rect = text.get_rect(center=(mode_rect.centerx - 8, mode_rect.centery))
        self.screen.blit(text, text_rect)
        
        # Flecha desplegable
        arrow_x = mode_rect.right - 15
        arrow_y = mode_rect.centery
        points = [(arrow_x, arrow_y - 4), (arrow_x + 8, arrow_y - 4), (arrow_x + 4, arrow_y + 4)]
        pygame.draw.polygon(self.screen, COLORS['button_text'], points)
        
        # Botón Estrategia IA (desplegable)
        strategy_rect = self.buttons['ai_strategy']
        color = COLORS['accent'] if self.hovered_element == 'ai_strategy' or self.dropdown_open == 'strategy' else COLORS['button']
        pygame.draw.rect(self.screen, color, strategy_rect, border_radius=12)
        
        strategy_texts = {
            'aleatoria': 'Estrategia Aleatoria',
            'minimax': 'Algoritmo Minimax'
        }
        text = FONT_SMALL.render(strategy_texts[self.ai_strategy], True, COLORS['button_text'])
        text_rect = text.get_rect(center=(strategy_rect.centerx - 8, strategy_rect.centery))
        self.screen.blit(text, text_rect)
        
        # Flecha desplegable
        arrow_x = strategy_rect.right - 15
        arrow_y = strategy_rect.centery
        points = [(arrow_x, arrow_y - 4), (arrow_x + 8, arrow_y - 4), (arrow_x + 4, arrow_y + 4)]
        pygame.draw.polygon(self.screen, COLORS['button_text'], points)
    
    def _draw_dropdowns(self):
        """Dibuja los menús desplegables si están abiertos"""
        if self.dropdown_open == 'mode':
            dropdown = self.dropdowns['mode']
            # Fondo del dropdown
            pygame.draw.rect(self.screen, COLORS['background'], dropdown['rect'], border_radius=12)
            pygame.draw.rect(self.screen, COLORS['grid'], dropdown['rect'], 2, border_radius=12)
            
            # Opciones
            for i, (value, label) in enumerate(dropdown['options']):
                option_rect = pygame.Rect(
                    dropdown['rect'].x + 2,
                    dropdown['rect'].y + 2 + i * (BUTTON_HEIGHT + 2),
                    dropdown['rect'].width - 4,
                    BUTTON_HEIGHT
                )
                
                # Resaltar opción seleccionada o hover
                if value == self.game_mode:
                    pygame.draw.rect(self.screen, COLORS['accent'], option_rect, border_radius=8)
                elif self.hovered_element == f'mode_{value}':
                    pygame.draw.rect(self.screen, COLORS['button_hover'], option_rect, border_radius=8)
                
                # Texto de la opción
                text_color = COLORS['button_text'] if (value == self.game_mode or self.hovered_element == f'mode_{value}') else COLORS['text']
                text = FONT_SMALL.render(label, True, text_color)
                text_rect = text.get_rect(center=option_rect.center)
                self.screen.blit(text, text_rect)
        
        elif self.dropdown_open == 'strategy':
            dropdown = self.dropdowns['strategy']
            # Fondo del dropdown
            pygame.draw.rect(self.screen, COLORS['background'], dropdown['rect'], border_radius=12)
            pygame.draw.rect(self.screen, COLORS['grid'], dropdown['rect'], 2, border_radius=12)
            
            # Opciones
            for i, (value, label) in enumerate(dropdown['options']):
                option_rect = pygame.Rect(
                    dropdown['rect'].x + 2,
                    dropdown['rect'].y + 2 + i * (BUTTON_HEIGHT + 2),
                    dropdown['rect'].width - 4,
                    BUTTON_HEIGHT
                )
                
                # Resaltar opción seleccionada o hover
                if value == self.ai_strategy:
                    pygame.draw.rect(self.screen, COLORS['accent'], option_rect, border_radius=8)
                elif self.hovered_element == f'strategy_{value}':
                    pygame.draw.rect(self.screen, COLORS['button_hover'], option_rect, border_radius=8)
                
                # Texto de la opción
                text_color = COLORS['button_text'] if (value == self.ai_strategy or self.hovered_element == f'strategy_{value}') else COLORS['text']
                text = FONT_SMALL.render(label, True, text_color)
                text_rect = text.get_rect(center=option_rect.center)
                self.screen.blit(text, text_rect)
    
    def _draw_grid(self):
        """Dibuja la grilla del tateti"""
        # Mostrar siempre la grilla, no solo cuando el juego está activo
        
        # Fondo de la grilla
        grid_rect = pygame.Rect(GRID_OFFSET_X - 10, GRID_OFFSET_Y - 10, GRID_SIZE + 20, GRID_SIZE + 20)
        pygame.draw.rect(self.screen, COLORS['grid'], grid_rect, border_radius=12)
        
        # Líneas de la grilla
        line_width = 4
        for i in range(1, 3):
            # Líneas verticales
            start_pos = (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y)
            end_pos = (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y + GRID_SIZE)
            pygame.draw.line(self.screen, COLORS['background'], start_pos, end_pos, line_width)
            
            # Líneas horizontales
            start_pos = (GRID_OFFSET_X, GRID_OFFSET_Y + i * CELL_SIZE)
            end_pos = (GRID_OFFSET_X + GRID_SIZE, GRID_OFFSET_Y + i * CELL_SIZE)
            pygame.draw.line(self.screen, COLORS['background'], start_pos, end_pos, line_width)
    
    def _draw_symbols(self):
        """Dibuja las X y O en el tablero"""
        # Mostrar siempre los símbolos del estado actual
        
        for i in range(3):
            for j in range(3):
                symbol = self.current_state[i][j]
                if symbol != '-':
                    center_x = GRID_OFFSET_X + j * CELL_SIZE + CELL_SIZE // 2
                    center_y = GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE // 2
                    
                    if symbol == 'X':
                        self._draw_x(center_x, center_y)
                    elif symbol == 'O':
                        self._draw_o(center_x, center_y)
    
    def _draw_x(self, center_x: int, center_y: int):
        """Dibuja una X moderna"""
        size = 40
        thickness = 6
        
        # Línea diagonal 1
        start1 = (center_x - size, center_y - size)
        end1 = (center_x + size, center_y + size)
        pygame.draw.line(self.screen, COLORS['x_color'], start1, end1, thickness)
        
        # Línea diagonal 2
        start2 = (center_x + size, center_y - size)
        end2 = (center_x - size, center_y + size)
        pygame.draw.line(self.screen, COLORS['x_color'], start2, end2, thickness)
    
    def _draw_o(self, center_x: int, center_y: int):
        """Dibuja una O moderna"""
        radius = 40
        thickness = 6
        pygame.draw.circle(self.screen, COLORS['o_color'], (center_x, center_y), radius, thickness)
    
    def _draw_game_info(self):
        """Dibuja información del juego"""
        if not self.game_active:
            return
            
        info_y = GRID_OFFSET_Y + GRID_SIZE + 30
        
        # Turno actual
        if not self.game_over:
            current_player = self.tateti.jugador(self.current_state)
            if self.thinking:
                text = "IA pensando..."
                color = COLORS['warning']
            elif (self.game_mode == 'human_vs_ai' and 
                  current_player != self.human_player):
                text = f"Turno: IA ({current_player})"
                color = COLORS['accent']
            else:
                text = f"Turno: {current_player}"
                color = COLORS['text']
        else:
            if self.winner:
                text = f"¡Ganador: {self.winner}!"
                color = COLORS['success']
            else:
                text = "¡Empate!"
                color = COLORS['warning']
        
        rendered_text = FONT_MEDIUM.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(WINDOW_WIDTH // 2, info_y))
        self.screen.blit(rendered_text, text_rect)
        
        # Información del modo y estrategia
        if self.game_active:
            mode_text = {
                'human_vs_human': 'Humano vs Humano',
                'human_vs_ai': f'Humano (X) vs IA (O)',
                'ai_vs_ai': 'IA vs IA'
            }
            
            strategy_text = {
                'aleatoria': 'Estrategia: Aleatoria',
                'minimax': 'Estrategia: Minimax'
            }
            
            mode_info = FONT_SMALL.render(mode_text[self.game_mode], True, COLORS['text'])
            mode_rect = mode_info.get_rect(center=(WINDOW_WIDTH // 2, info_y + 35))
            self.screen.blit(mode_info, mode_rect)
            
            if self.game_mode in ['human_vs_ai', 'ai_vs_ai']:
                strategy_info = FONT_SMALL.render(strategy_text[self.ai_strategy], True, COLORS['text'])
                strategy_rect = strategy_info.get_rect(center=(WINDOW_WIDTH // 2, info_y + 55))
                self.screen.blit(strategy_info, strategy_rect)
    
    def _handle_button_click(self, pos: Tuple[int, int]):
        """Maneja los clics en botones y dropdowns"""
        # Verificar clics en botones principales
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_name == 'new_game':
                    self._start_game()
                elif button_name == 'game_mode':
                    self.dropdown_open = 'mode' if self.dropdown_open != 'mode' else None
                elif button_name == 'ai_strategy':
                    self.dropdown_open = 'strategy' if self.dropdown_open != 'strategy' else None
                return
        
        # Verificar clics en dropdowns abiertos
        if self.dropdown_open == 'mode':
            dropdown = self.dropdowns['mode']
            if dropdown['rect'].collidepoint(pos):
                # Determinar qué opción se clickeó
                rel_y = pos[1] - dropdown['rect'].y - 2
                option_index = rel_y // (BUTTON_HEIGHT + 2)
                if 0 <= option_index < len(dropdown['options']):
                    value, _ = dropdown['options'][option_index]
                    self.game_mode = value
                    self.dropdown_open = None
                return
            else:
                self.dropdown_open = None
        
        elif self.dropdown_open == 'strategy':
            dropdown = self.dropdowns['strategy']
            if dropdown['rect'].collidepoint(pos):
                # Determinar qué opción se clickeó
                rel_y = pos[1] - dropdown['rect'].y - 2
                option_index = rel_y // (BUTTON_HEIGHT + 2)
                if 0 <= option_index < len(dropdown['options']):
                    value, _ = dropdown['options'][option_index]
                    self.ai_strategy = value
                    self.dropdown_open = None
                return
            else:
                self.dropdown_open = None
        else:
            # Cerrar dropdowns si se hace clic fuera
            self.dropdown_open = None
    
    def _start_game(self):
        """Inicia una nueva partida"""
        self.game_active = True
        self.game_over = False
        self.winner = None
        self.current_state = self.tateti.estado_inicial
        self.dropdown_open = None
        
        # Configurar jugador humano según el modo
        if self.game_mode == 'human_vs_ai':
            self.human_player = 'X'  # Humano siempre es X
        else:
            self.human_player = None
    
    def _reset_game(self):
        """Reinicia el juego"""
        self.game_active = False
        self.game_over = False
        self.winner = None
        self.current_state = self.tateti.estado_inicial
        self.thinking = False
    
    def _handle_cell_click(self, pos: Tuple[int, int]):
        """Maneja los clics en las celdas del tablero"""
        if not self.game_active or self.game_over or self.thinking:
            return
            
        cell = self._get_cell_from_pos(pos)
        if cell is None:
            return
            
        # Verificar si es turno del humano
        current_player = self.tateti.jugador(self.current_state)
        if (self.game_mode == 'human_vs_ai' and 
            current_player != self.human_player):
            return
            
        # Verificar si la acción es válida
        if cell in self.tateti.acciones(self.current_state):
            self._make_move(cell)
    
    def _make_move(self, action: Tuple[int, int]):
        """Ejecuta una jugada"""
        self.current_state = self.tateti.resultado(self.current_state, action)
        
        # Verificar si el juego terminó
        if self.tateti.test_terminal(self.current_state):
            self.game_over = True
            
            # La función utilidad siempre es desde la perspectiva de MAX (X)
            utility = self.tateti.utilidad(self.current_state)
            if utility == 1.0:
                self.winner = 'X'  # MAX ganó
            elif utility == 0.0:
                self.winner = 'O'  # MIN ganó
            # Si utility == 0.5, es empate (winner queda None)
    
    def _ai_move(self):
        """Ejecuta una jugada de la IA"""
        if (not self.game_active or self.game_over or 
            self.thinking or self.game_mode == 'human_vs_human'):
            return
            
        current_player = self.tateti.jugador(self.current_state)
        
        # Verificar si es turno de la IA
        if (self.game_mode == 'human_vs_ai' and 
            current_player == self.human_player):
            return
            
        self.thinking = True
        pygame.display.flip()  # Actualizar pantalla para mostrar "pensando"
        
        # Pequeña pausa para efecto visual
        pygame.time.wait(500)
        
        # Elegir acción usando la estrategia seleccionada
        if self.ai_strategy == 'aleatoria':
            action = estrategia_aleatoria(self.tateti, self.current_state)
        else:  # minimax
            try:
                action = estrategia_minimax(self.tateti, self.current_state)
            except NotImplementedError as e:
                # Si minimax no está implementado, mostrar mensaje y cerrar
                print(str(e))
                pygame.quit()
                sys.exit(1)
        
        if action:
            self._make_move(action)
            
        self.thinking = False
    
    def _update_hover(self, pos: Tuple[int, int]):
        """Actualiza el elemento que está siendo hover"""
        self.hovered_element = None
        
        # Verificar hover en botones principales
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.hovered_element = button_name
                return
        
        # Verificar hover en dropdowns abiertos
        if self.dropdown_open == 'mode':
            dropdown = self.dropdowns['mode']
            if dropdown['rect'].collidepoint(pos):
                rel_y = pos[1] - dropdown['rect'].y - 2
                option_index = rel_y // (BUTTON_HEIGHT + 2)
                if 0 <= option_index < len(dropdown['options']):
                    value, _ = dropdown['options'][option_index]
                    self.hovered_element = f'mode_{value}'
        
        elif self.dropdown_open == 'strategy':
            dropdown = self.dropdowns['strategy']
            if dropdown['rect'].collidepoint(pos):
                rel_y = pos[1] - dropdown['rect'].y - 2
                option_index = rel_y // (BUTTON_HEIGHT + 2)
                if 0 <= option_index < len(dropdown['options']):
                    value, _ = dropdown['options'][option_index]
                    self.hovered_element = f'strategy_{value}'
    
    def run(self):
        """Loop principal del juego"""
        running = True
        
        while running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click izquierdo
                        self._handle_button_click(event.pos)
                        self._handle_cell_click(event.pos)
                        
                elif event.type == pygame.MOUSEMOTION:
                    self._update_hover(event.pos)
            
            # Lógica de la IA
            self._ai_move()
            
            # Dibujar todo
            self._draw_background()
            self._draw_toolbar()
            self._draw_title()
            self._draw_grid()
            self._draw_symbols()
            self._draw_game_info()
            self._draw_dropdowns()  # Los dropdowns se dibujan al final para estar encima
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
