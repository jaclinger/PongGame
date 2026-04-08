import arcade
import random
import time

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong 2: The ponging"

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 15
BALL_BASE_SPEED_X = 4
BALL_BASE_SPEED_Y = 3
BALL_SPEED_INCREMENT = 0.5  # speed up after each paddle hit

# Winning score
WINNING_SCORE = 5

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Game state
        self.game_started = False
        self.game_over = False
        self.winner = None
        self.ball_moving = False  # used for delayed ball launch

        # Player paddle
        self.player_y = SCREEN_HEIGHT // 2

        # AI paddle
        self.ai_y = SCREEN_HEIGHT // 2

        # Ball
        self.reset_ball()

        # Movement flags
        self.up_pressed = False
        self.down_pressed = False

        # Score
        self.player_score = 0
        self.ai_score = 0

    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = random.choice([-BALL_BASE_SPEED_X, BALL_BASE_SPEED_X])
        self.ball_dy = random.choice([-BALL_BASE_SPEED_Y, BALL_BASE_SPEED_Y])
        self.ball_moving = False
        arcade.schedule(self.launch_ball, 1)  # launch after 1 second

    def launch_ball(self, delta_time):
        self.ball_moving = True
        arcade.unschedule(self.launch_ball)

    def on_draw(self):
        self.clear()

        if not self.game_started:
            arcade.draw_text(
                "PONG 2: The Ponging",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 50,
                arcade.color.WHITE,
                50,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to Start",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 20,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )
            return

        if self.game_over:
            arcade.draw_text(
                f"{self.winner} Wins!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                40,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to Restart",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 50,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )
            return

        # Draw paddles
        arcade.draw_lbwh_rectangle_filled(
            45,
            self.player_y - (PADDLE_HEIGHT // 2),
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            arcade.color.BLUE
        )
        arcade.draw_lbwh_rectangle_filled(
            SCREEN_WIDTH - 55,
            self.ai_y - (PADDLE_HEIGHT // 2),
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            arcade.color.RED
        )

        # Draw ball
        arcade.draw_circle_filled(
            self.ball_x,
            self.ball_y,
            BALL_SIZE,
            arcade.color.WHITE
        )

        # Draw score
        score_text = f"{self.player_score}   {self.ai_score}"
        arcade.draw_text(
            score_text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def on_update(self, delta_time):
        if not self.game_started or self.game_over or not self.ball_moving:
            return

        # Move player paddle
        if self.up_pressed:
            self.player_y += PADDLE_SPEED
        if self.down_pressed:
            self.player_y -= PADDLE_SPEED

        # Keep player paddle on screen
        self.player_y = max(PADDLE_HEIGHT // 2, self.player_y)
        self.player_y = min(SCREEN_HEIGHT - PADDLE_HEIGHT // 2, self.player_y)

        # AI movement (weaker AI)
        AI_SPEED = 3
        if abs(self.ball_y - self.ai_y) > 20:
            if self.ball_y > self.ai_y:
                self.ai_y += AI_SPEED
            elif self.ball_y < self.ai_y:
                self.ai_y -= AI_SPEED

        # Move ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Bounce off top/bottom
        if self.ball_y <= 0 or self.ball_y >= SCREEN_HEIGHT:
            self.ball_dy *= -1

        # Player paddle collision
        if (self.ball_x <= 55 and
            self.player_y - 50 < self.ball_y < self.player_y + 50):
            offset = (self.ball_y - self.player_y) / (PADDLE_HEIGHT / 2)
            self.ball_dx *= -1.1
            self.ball_dy = offset * abs(self.ball_dx)

        # AI paddle collision
        if (self.ball_x >= SCREEN_WIDTH - 55 and
            self.ai_y - 50 < self.ball_y < self.ai_y + 50):
            offset = (self.ball_y - self.ai_y) / (PADDLE_HEIGHT / 2)
            self.ball_dx *= -1.1
            self.ball_dy = offset * abs(self.ball_dx)

        # Scoring
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_after_score()
        if self.ball_x > SCREEN_WIDTH:
            self.player_score += 1
            self.reset_after_score()

    def reset_after_score(self):
        # Reset paddles
        self.player_y = SCREEN_HEIGHT // 2
        self.ai_y = SCREEN_HEIGHT // 2

        # Reset ball
        self.reset_ball()

        # Check winner
        self.check_winner()

    def check_winner(self):
        if self.player_score >= WINNING_SCORE:
            self.winner = "Player"
            self.game_over = True
        elif self.ai_score >= WINNING_SCORE:
            self.winner = "AI"
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if not self.game_started:
                self.game_started = True
            elif self.game_over:
                # Restart game
                self.player_score = 0
                self.ai_score = 0
                self.game_over = False
                self.winner = None
                self.reset_after_score()
        if key == arcade.key.UP:
            self.up_pressed = True
        if key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        if key == arcade.key.DOWN:
            self.down_pressed = False


def main():
    game = PongGame()
    arcade.run()


if __name__ == "__main__":
    main()