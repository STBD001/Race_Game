import pyglet
import random

class GameObject:
    def __init__(self, sprite):
        self.sprite = sprite
        self.update_bbox()

    def update_bbox(self):
        self.bbox = (
            self.sprite.x,
            self.sprite.y,
            self.sprite.x + self.sprite.width,
            self.sprite.y + self.sprite.height
        )

    def intersects(self, other):
        ax1, ay1, ax2, ay2 = self.bbox
        bx1, by1, bx2, by2 = other.bbox
        return (ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1)


class Game_Logic(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=600, caption="Race Game")
        self.player = self.load_player()
        self.obstacles = self.create_obstacles()
        self.keys_pressed = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys_pressed)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.background = pyglet.shapes.Rectangle(0, 0, self.width, self.height, color=(0, 100, 0))
        self.game_over = False

    def load_player(self):
        car_image = pyglet.image.load("P1.png")
        car_image.width = 50
        car_image.height = 100
        player_sprite = pyglet.sprite.Sprite(car_image, x=self.width // 2, y=50)
        return GameObject(player_sprite)

    def create_obstacles(self):
        obstacles = []
        for i in range(5):
            obstacle_image = pyglet.image.load("P2.jpg")
            obstacle_image.width = 60
            obstacle_image.height = 120
            x_position = random.randint(0, self.width - obstacle_image.width)
            obstacle_sprite = pyglet.sprite.Sprite(obstacle_image, x=x_position, y=600 + i * 150)
            obstacles.append(GameObject(obstacle_sprite))
        return obstacles

    def on_draw(self):
        self.clear()
        self.draw_background()
        self.player.sprite.draw()
        for obstacle in self.obstacles:
            obstacle.sprite.draw()

        if self.game_over:
            self.draw_game_over()

    def draw_background(self):
        self.background.draw()

    def draw_game_over(self):
        game_over_label = pyglet.text.Label(
            "Game Over",
            font_name="Arial",
            font_size=36,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 0, 0, 255)
        )
        game_over_label.draw()

    def update(self, dt):
        if self.game_over:
            return

        if self.keys_pressed[pyglet.window.key.LEFT]:
            self.player.sprite.x -= 200 * dt
        if self.keys_pressed[pyglet.window.key.RIGHT]:
            self.player.sprite.x += 200 * dt

        self.player.update_bbox()

        for obstacle in self.obstacles:
            obstacle.sprite.y -= 200 * dt  
            if obstacle.sprite.y < -50:
                obstacle.sprite.y = 600
                obstacle.sprite.x = random.randint(0, self.width - obstacle.sprite.width)  # Losowe generowanie x
            obstacle.update_bbox()

            if self.player.intersects(obstacle):
                self.game_over = True
                pyglet.clock.unschedule(self.update)


if __name__ == "__main__":
    game = Game_Logic()
    pyglet.app.run()
