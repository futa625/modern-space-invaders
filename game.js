let player;
let enemies = [];
let bullets = [];
let score = 0;
let level = 1;
let gameStarted = false;
let menu = document.getElementById('menu');

// Player class
function Player() {
    this.x = width / 2;
    this.y = height - 50;
    this.width = 60;
    this.height = 60;
    this.speed = 8;
    this.health = 100;

    this.show = function() {
        fill(0, 255, 0);
        rect(this.x, this.y, this.width, this.height);
    };

    this.move = function(dir) {
        this.x += dir * this.speed;
        this.x = constrain(this.x, 0, width - this.width);
    };
}

// Enemy class
function Enemy(x, y) {
    this.x = x;
    this.y = y;
    this.width = 50;
    this.height = 50;
    this.health = 3;
    this.direction = 1;
    this.speed = 3;

    this.show = function() {
        fill(255, 0, 0);
        rect(this.x, this.y, this.width, this.height);
    };

    this.move = function() {
        this.x += this.direction * this.speed;
        if (this.x <= 0 || this.x >= width - this.width) {
            this.direction *= -1;
            this.y += this.height;
        }
    };

    this.takeDamage = function() {
        this.health--;
        if (this.health <= 0) {
            score += 10;
            return true;
        }
        return false;
    };
}

// Bullet class
function Bullet(x, y) {
    this.x = x;
    this.y = y;
    this.width = 4;
    this.height = 20;
    this.speed = 12;

    this.show = function() {
        fill(255, 255, 0);
        rect(this.x, this.y, this.width, this.height);
    };

    this.move = function() {
        this.y -= this.speed;
    };
}

function setup() {
    createCanvas(1200, 800);
    player = new Player();
}

function draw() {
    background(0);
    
    if (!gameStarted) {
        return;
    }

    // Game logic
    if (frameCount % 60 === 0) {
        createEnemies();
    }

    // Player movement
    if (keyIsDown(LEFT_ARROW)) {
        player.move(-1);
    }
    if (keyIsDown(RIGHT_ARROW)) {
        player.move(1);
    }

    // Bullets
    for (let i = bullets.length - 1; i >= 0; i--) {
        bullets[i].move();
        bullets[i].show();

        if (bullets[i].y < 0) {
            bullets.splice(i, 1);
        }
    }

    // Enemies
    for (let i = enemies.length - 1; i >= 0; i--) {
        enemies[i].move();
        enemies[i].show();

        // Check collision with bullets
        for (let j = bullets.length - 1; j >= 0; j--) {
            if (collideRectRect(bullets[j].x, bullets[j].y, bullets[j].width, bullets[j].height,
                enemies[i].x, enemies[i].y, enemies[i].width, enemies[i].height)) {
                if (enemies[i].takeDamage()) {
                    enemies.splice(i, 1);
                }
                bullets.splice(j, 1);
                break;
            }
        }

        // Check collision with player
        if (collideRectRect(player.x, player.y, player.width, player.height,
            enemies[i].x, enemies[i].y, enemies[i].width, enemies[i].height)) {
            player.health -= 10;
            enemies.splice(i, 1);
        }
    }

    // Player
    player.show();

    // UI
    fill(255);
    textSize(32);
    text(`Score: ${score}`, 20, 40);
    text(`Level: ${level}`, 20, 80);
    text(`Health: ${player.health}`, 20, 120);

    // Game over condition
    if (player.health <= 0) {
        fill(255, 0, 0);
        textSize(64);
        textAlign(CENTER, CENTER);
        text('Game Over!', width / 2, height / 2);
        gameStarted = false;
    }
}

function keyPressed() {
    if (keyCode === 32 && gameStarted) {
        let bullet = new Bullet(player.x + player.width / 2 - 2, player.y);
        bullets.push(bullet);
    }
}

function startGame() {
    menu.style.display = 'none';
    gameStarted = true;
}

function createEnemies() {
    let cols = 10;
    let spacing = 100;
    let startX = (width - (cols * spacing)) / 2;
    
    for (let i = 0; i < cols; i++) {
        let enemy = new Enemy(startX + i * spacing, 50);
        enemies.push(enemy);
    }
    level++;
}
