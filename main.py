import pyglet

class Game_Logic(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=600, caption="Race Game")
        self.player = self.load_player()
        self.obstacles = self.create_obstacles()
        self.keys_pressed = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys_pressed)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.background = pyglet.shapes.Rectangle(0, 0, self.width, self.height, color=(0, 100, 0))

    def load_player(self):
        car_image = pyglet.image.load("P1.png")
        car_image.width = 50
        car_image.height = 100
        player_sprite = pyglet.sprite.Sprite(car_image, x=self.width // 2, y=50)
        return player_sprite

    def create_obstacles(self):
        obstacles = []
        for i in range(5):
            obstacle_image = pyglet.image.load("P2.jpg")
            obstacle_image.width = 60
            obstacle_image.height = 120
            obstacle_sprite = pyglet.sprite.Sprite(obstacle_image, x=self.width // 2, y=600 + i * 150)
            obstacles.append(obstacle_sprite)
        return obstacles

    def on_draw(self):
        self.clear()
        self.draw_background()
        self.player.draw()
        for obstacle in self.obstacles:
            obstacle.draw()

    def draw_background(self):
        self.background.draw()

    def update(self, dt):
        if self.keys_pressed[pyglet.window.key.LEFT]:
            self.player.x -= 200 * dt
        if self.keys_pressed[pyglet.window.key.RIGHT]:
            self.player.x += 200 * dt

        for obstacle in self.obstacles:
            obstacle.y -= 150 * dt
            if obstacle.y < -50:
                obstacle.y = 600

if __name__ == "__main__":
    game = Game_Logic()
    pyglet.app.run()
