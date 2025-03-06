import pygame
import random


class CartesianMatrix:
    def __init__(self):
        """
        Classe para controle da Matrix Cartesiana, mantém as informacoes referentes a tela, fonte, possiveis cores e possiveis forma.
        args:
            None
        """
        pygame.init()

        self.cell_width = 60
        self.max_size = 10
        self.screen_height = self.max_size * self.cell_width
        self.screen_width = self.max_size * self.cell_width

        # Cores
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (220, 220, 220),
            "green": (0, 255, 0),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
        }

        self.shapes = ["circle", "square", "triangle", "diamond", "cross"]

        self.matrix = None
        self.height = None
        self.width = None

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Matriz Cartesiana com Figuras Geométricas")

        self.font = pygame.font.SysFont("Arial", 18)

        self.running = True

    def create_matrix(self, height, width):
        """
        Função para criar a matriz com as dimensões especificadas.
        Args:
            height: Número de linhas da matriz (máximo 10)
            width: Número de colunas da matriz (máximo 10)
        """
        # Validar as dimensões
        if height <= 0 or height > self.max_size or width <= 0 or width > self.max_size:
            print(f"Erro: As dimensões devem estar entre 1 e {self.max_size}.")
            return False

        self.height = height
        self.width = width

        self.matrix = [
            [
                {"color": "gray", "shape": random.choice(self.shapes)}
                for _ in range(width)
            ]
            for _ in range(height)
        ]

        self.matrix[0][0] = {"color": "green", "shape": "circle"}

        return True

    def draw_shape(self, shape, x, y, color):
        """
        Desenha uma figura geométrica específica na posição dada.
        Args:
            shape: Tipo de figura ('circle', 'square', 'triangle', 'diamond', 'cross')
            x: Posição x no centro da célula
            y: Posição y no centro da célula
            color: Cor da figura
        """
        size = self.cell_width // 3  # Tamanho padrão para as figuras

        if shape == "circle":
            pygame.draw.circle(self.screen, color, (x, y), size)

        elif shape == "square":
            rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            pygame.draw.rect(self.screen, color, rect)

        elif shape == "triangle":
            points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
            pygame.draw.polygon(self.screen, color, points)

        elif shape == "diamond":
            points = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
            pygame.draw.polygon(self.screen, color, points)

        elif shape == "cross":
            thickness = max(int(size / 3), 3)
            pygame.draw.rect(
                self.screen, color, (x - size, y - thickness // 2, size * 2, thickness)
            )
            pygame.draw.rect(
                self.screen, color, (x - thickness // 2, y - size, thickness, size * 2)
            )

    def display_matrix(self):
        """
        Função para exibir a matriz.
        """
        if self.matrix is None:
            print("Erro: A matriz ainda não foi criada.")
            return

        self.screen.fill(self.colors["white"])

        for i in range(self.height):
            for j in range(self.width):
                x = j * self.cell_width
                y = i * self.cell_width

                # Desenhar a borda da célula
                pygame.draw.rect(
                    self.screen,
                    self.colors["gray"],
                    (x, y, self.cell_width, self.cell_width),
                    1,
                )

                # Desenhar a figura geométrica
                cell_data = self.matrix[i][j]
                center_x = x + self.cell_width // 2
                center_y = y + self.cell_width // 2

                cor = self.colors.get(cell_data["color"], self.colors["black"])
                self.draw_shape(cell_data["shape"], center_x, center_y, cor)

                # Mostrar as coordenadas
                texto = f"({i},{j})"
                texto_superficie = self.font.render(texto, True, self.colors["black"])
                self.screen.blit(texto_superficie, (x + 5, y + 5))

        pygame.display.flip()

    def change_point(self, x, y, color):
        """
        Função para mudar um ponto na matriz.
        Args:
            x: Coordenada da linha (altura)
            y: Coordenada da coluna (largura)
            color: Cor do ponto a ser inserido
            shape: Forma geométrica (opcional, mantém a atual se não especificada)
        """
        if self.matrix is None:
            print("Erro: A matriz ainda não foi criada.")
            return False

        if x < 0 or x >= self.height or y < 0 or y >= self.width:
            print(
                f"Erro: Coordenadas fora dos limites da matriz ({self.height}x{self.width})."
            )
            return False

        if color not in self.colors:
            print(
                f"Erro: Cor '{color}' não reconhecida. Cores disponíveis: {list(self.colors.keys())}"
            )
            return False

        current_shape = "circle"

        self.matrix[x][y] = {"color": color, "shape": current_shape}

        self.display_matrix()

        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    column = pos_x // self.cell_width
                    row = pos_y // self.cell_width

                    if 0 <= row < self.height and 0 <= column < self.width:
                        self.change_point(row, column, "green")

    def run(self):
        """
        Método principal para executar o programa.
        """
        while self.running:
            self.handle_events()
            self.display_matrix()
            pygame.time.Clock().tick(30)

        pygame.quit()


def main():
    app = CartesianMatrix()

    if app.create_matrix(4, 5):
        print("Matriz 4x5 criada com sucesso!")

        app.change_point(2, 1, "green")
        app.change_point(1, 3, "red")
        app.change_point(
            3,
            4,
            "blue",
        )

        app.run()


if __name__ == "__main__":
    main()
