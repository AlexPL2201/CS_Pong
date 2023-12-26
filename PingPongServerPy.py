import random
import math
import socket
import serv_settings


class Ball:
    def __init__(self, x, y, sx, sy, r):
        self.x = x
        self.y = y
        self.speed_x = sx
        self.speed_y = sy
        self.radius = r

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # шарик коснулся верхней или нижней грани
        if self.y + self.radius >= Game.screen_height or self.y - self.radius <= 0:
            self.speed_y *= -1

        # шарик коснулся левой или правой грани
        if self.x + self.radius >= Game.screen_width:
            Game.player1_score += 1
            self.reset_ball()

        if self.x - self.radius <= 0:
            Game.player2_score += 1
            self.reset_ball()

    def reset_ball(self):
        self.x = Game.screen_width / 2
        self.y = Game.screen_height / 2
        speed_choices = [-1, 1]
        self.speed_x *= random.choice(speed_choices)
        self.speed_y *= random.choice(speed_choices)


class Paddle:
    def __init__(self, w, h, x, y, s):
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.speed = s

    def update(self, up_key_pressed, down_key_pressed):
        if up_key_pressed:
            self.y -= self.speed

        if down_key_pressed:
            self.y += self.speed

        self.limit_movement()

    def limit_movement(self):
        if self.y <= 0:
            self.y = 0

        if self.y + self.height >= Game.screen_height:
            self.y = Game.screen_height - self.height


def check_collision_circle_rect(circle_center, circle_radius, rect):
    # Вычисляем ближайную точку в прямоугольнике к центру круга
    closest_x = max(rect.x, min(circle_center.x, rect.x + rect.width))
    closest_y = max(rect.y, min(circle_center.y, rect.y + rect.height))

    # Вычисляем расстояние между центром круга и ближайшей точкой в прямоугольнике
    distance_x = circle_center.x - closest_x
    distance_y = circle_center.y - closest_y

    # Проверяем, если расстояние меньше радиуса круга, то есть есть столкновение
    return math.sqrt(distance_x**2 + distance_y**2) < circle_radius


class CPUPaddle(Paddle):
    def __init__(self, w, h, x, y, s):
        super().__init__(w, h, x, y, s)

    def update(self, ball_y):
        if self.y + self.height / 2 > ball_y:
            self.y -= self.speed
        if self.y + self.height / 2 <= ball_y:
            self.y += self.speed
        self.limit_movement()


class Game:
    player1_score = 0
    player2_score = 0
    screen_width = 1280
    screen_height = 800


    @staticmethod
    def play():
        try:
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.bind((serv_settings.ip, serv_settings.game_port))
            serv_settings.game_port += 1
            print(f'[GAME] The server is running. IP: {serv_settings.ip} Port {serv_settings.game_port}.')

        except socket.error as e:
            print(f"[GAME_ERR] Socket binding error: {e}.")
            sock2.close()

        sock2.listen(1)
        client_sock, client_address = sock2.accept()
        print(f'[GAME] Connected! Client`s address: {client_address}')
        ball = Ball(Game.screen_width / 2, Game.screen_height / 2, 7, 7, 20)
        player = Paddle(25, 120, Game.screen_width - 35, Game.screen_height / 2 - 60, 6)
        cpu = CPUPaddle(25, 120, 10, Game.screen_height / 2 - 60, 6)

        while True:
            data = client_sock.recv(1024)
            print(f'[GAME] Message received {data.decode()}')
            ball.update()
            player.update(False, False)
            cpu.update(ball.y)

            if check_collision_circle_rect(ball, ball.radius, player):
                ball.speed_x *= -1

            if check_collision_circle_rect(ball, ball.radius, player):
                ball.speed_x *= -1

            client_sock.send(f'{ball.x}, {ball.y}, {player.x}, {player.y}, {cpu.x}, {cpu.y}'.encode())





