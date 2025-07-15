// Game variables
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const healthBar = document.getElementById('healthBar');
const scoreElement = document.getElementById('score');
const enemyCountElement = document.getElementById('enemyCount');
const gameOverElement = document.getElementById('gameOver');
const gameOverText = document.getElementById('gameOverText');

// Game state
let gameRunning = true;
let score = 0;
let mouseX = 0;
let mouseY = 0;

// Input handling
const keys = {};
let mouseDown = false;

// Game objects
let player;
let enemies = [];
let bullets = [];
let obstacles = [];

// Game settings
const TANK_SIZE = 30;
const BULLET_SIZE = 4;
const BULLET_SPEED = 8;
const TANK_SPEED = 3;
const ENEMY_SPAWN_COUNT = 5;

// Tank class
class Tank {
    constructor(x, y, color, isPlayer = false) {
        this.x = x;
        this.y = y;
        this.angle = 0;
        this.turretAngle = 0;
        this.health = 100;
        this.maxHealth = 100;
        this.color = color;
        this.isPlayer = isPlayer;
        this.size = TANK_SIZE;
        this.lastShot = 0;
        this.shootCooldown = 300; // milliseconds
        
        // AI properties
        if (!isPlayer) {
            this.targetX = Math.random() * canvas.width;
            this.targetY = Math.random() * canvas.height;
            this.lastTargetUpdate = 0;
        }
    }
    
    update() {
        if (this.isPlayer) {
            this.updatePlayer();
        } else {
            this.updateAI();
        }
        
        // Keep tank in bounds
        this.x = Math.max(this.size/2, Math.min(canvas.width - this.size/2, this.x));
        this.y = Math.max(this.size/2, Math.min(canvas.height - this.size/2, this.y));
    }
    
    updatePlayer() {
        // Movement
        let dx = 0, dy = 0;
        if (keys['w'] || keys['W']) dy = -TANK_SPEED;
        if (keys['s'] || keys['S']) dy = TANK_SPEED;
        if (keys['a'] || keys['A']) dx = -TANK_SPEED;
        if (keys['d'] || keys['D']) dx = TANK_SPEED;
        
        if (dx !== 0 || dy !== 0) {
            this.x += dx;
            this.y += dy;
            this.angle = Math.atan2(dy, dx);
        }
        
        // Turret aiming
        this.turretAngle = Math.atan2(mouseY - this.y, mouseX - this.x);
        
        // Shooting
        if (mouseDown && Date.now() - this.lastShot > this.shootCooldown) {
            this.shoot();
        }
    }
    
    updateAI() {
        const now = Date.now();
        
        // Update target occasionally
        if (now - this.lastTargetUpdate > 2000) {
            if (Math.random() > 0.5) {
                // Target player
                this.targetX = player.x;
                this.targetY = player.y;
            } else {
                // Random movement
                this.targetX = Math.random() * canvas.width;
                this.targetY = Math.random() * canvas.height;
            }
            this.lastTargetUpdate = now;
        }
        
        // Move towards target
        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 50) {
            const moveX = (dx / distance) * TANK_SPEED * 0.7;
            const moveY = (dy / distance) * TANK_SPEED * 0.7;
            this.x += moveX;
            this.y += moveY;
            this.angle = Math.atan2(moveY, moveX);
        }
        
        // Aim at player
        const playerDx = player.x - this.x;
        const playerDy = player.y - this.y;
        const playerDistance = Math.sqrt(playerDx * playerDx + playerDy * playerDy);
        
        if (playerDistance < 300) {
            this.turretAngle = Math.atan2(playerDy, playerDx);
            
            // Shoot at player
            if (now - this.lastShot > this.shootCooldown * 1.5 && Math.random() > 0.7) {
                this.shoot();
            }
        }
    }
    
    shoot() {
        this.lastShot = Date.now();
        const bulletX = this.x + Math.cos(this.turretAngle) * this.size/2;
        const bulletY = this.y + Math.sin(this.turretAngle) * this.size/2;
        
        bullets.push(new Bullet(
            bulletX, bulletY,
            this.turretAngle,
            this.isPlayer
        ));
    }
    
    takeDamage(damage) {
        this.health -= damage;
        if (this.health <= 0) {
            this.health = 0;
            if (this.isPlayer) {
                endGame(false);
            } else {
                score += 100;
                updateUI();
            }
            return true; // Tank destroyed
        }
        return false;
    }
    
    draw() {
        ctx.save();
        
        // Draw tank body
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);
        ctx.fillStyle = this.color;
        ctx.fillRect(-this.size/2, -this.size/3, this.size, this.size*2/3);
        
        // Draw tank tracks
        ctx.fillStyle = '#2c3e50';
        ctx.fillRect(-this.size/2, -this.size/3 - 3, this.size, 6);
        ctx.fillRect(-this.size/2, this.size/3 - 3, this.size, 6);
        
        ctx.restore();
        
        // Draw turret
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.turretAngle);
        ctx.fillStyle = this.color;
        ctx.fillRect(0, -8, this.size * 0.8, 16);
        ctx.restore();
        
        // Draw health bar for enemies
        if (!this.isPlayer) {
            const healthPercent = this.health / this.maxHealth;
            ctx.fillStyle = 'red';
            ctx.fillRect(this.x - this.size/2, this.y - this.size/2 - 10, this.size, 4);
            ctx.fillStyle = 'green';
            ctx.fillRect(this.x - this.size/2, this.y - this.size/2 - 10, this.size * healthPercent, 4);
        }
    }
}

// Bullet class
class Bullet {
    constructor(x, y, angle, fromPlayer) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = BULLET_SPEED;
        this.fromPlayer = fromPlayer;
        this.size = BULLET_SIZE;
        this.damage = 25;
    }
    
    update() {
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;
    }
    
    isOutOfBounds() {
        return this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height;
    }
    
    draw() {
        ctx.fillStyle = this.fromPlayer ? '#f39c12' : '#e74c3c';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Obstacle class
class Obstacle {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    
    draw() {
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        ctx.strokeStyle = '#654321';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
    }
}

// Collision detection
function checkCollision(obj1, obj2) {
    const dx = obj1.x - obj2.x;
    const dy = obj1.y - obj2.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    return distance < (obj1.size || obj1.width) / 2 + (obj2.size || obj2.width) / 2;
}

function checkBulletObstacleCollision(bullet, obstacle) {
    return bullet.x > obstacle.x && bullet.x < obstacle.x + obstacle.width &&
           bullet.y > obstacle.y && bullet.y < obstacle.y + obstacle.height;
}

// Game initialization
function initGame() {
    // Create player tank
    player = new Tank(canvas.width / 2, canvas.height / 2, '#3498db', true);
    
    // Create enemies
    enemies = [];
    for (let i = 0; i < ENEMY_SPAWN_COUNT; i++) {
        let x, y;
        do {
            x = Math.random() * (canvas.width - TANK_SIZE) + TANK_SIZE/2;
            y = Math.random() * (canvas.height - TANK_SIZE) + TANK_SIZE/2;
        } while (Math.sqrt((x - player.x) ** 2 + (y - player.y) ** 2) < 150);
        
        enemies.push(new Tank(x, y, '#e74c3c'));
    }
    
    // Create obstacles
    obstacles = [];
    for (let i = 0; i < 8; i++) {
        obstacles.push(new Obstacle(
            Math.random() * (canvas.width - 80),
            Math.random() * (canvas.height - 80),
            60 + Math.random() * 40,
            60 + Math.random() * 40
        ));
    }
    
    bullets = [];
    score = 0;
    gameRunning = true;
    updateUI();
}

// Update UI
function updateUI() {
    healthBar.style.width = (player.health / player.maxHealth * 200) + 'px';
    scoreElement.textContent = score;
    enemyCountElement.textContent = enemies.length;
}

// Game loop
function gameLoop() {
    if (!gameRunning) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Update game objects
    player.update();
    
    enemies.forEach(enemy => enemy.update());
    bullets.forEach(bullet => bullet.update());
    
    // Handle collisions
    bullets = bullets.filter(bullet => {
        // Check bullet-tank collisions
        if (bullet.fromPlayer) {
            for (let i = enemies.length - 1; i >= 0; i--) {
                if (checkCollision(bullet, enemies[i])) {
                    if (enemies[i].takeDamage(bullet.damage)) {
                        enemies.splice(i, 1);
                    }
                    return false; // Remove bullet
                }
            }
        } else {
            if (checkCollision(bullet, player)) {
                player.takeDamage(bullet.damage);
                updateUI();
                return false; // Remove bullet
            }
        }
        
        // Check bullet-obstacle collisions
        for (let obstacle of obstacles) {
            if (checkBulletObstacleCollision(bullet, obstacle)) {
                return false; // Remove bullet
            }
        }
        
        // Remove bullets that are out of bounds
        return !bullet.isOutOfBounds();
    });
    
    // Draw everything
    obstacles.forEach(obstacle => obstacle.draw());
    player.draw();
    enemies.forEach(enemy => enemy.draw());
    bullets.forEach(bullet => bullet.draw());
    
    // Check win condition
    if (enemies.length === 0) {
        endGame(true);
    }
    
    requestAnimationFrame(gameLoop);
}

// End game
function endGame(won) {
    gameRunning = false;
    gameOverText.textContent = won ? 'Victory!' : 'Defeated!';
    gameOverElement.style.display = 'block';
}

// Restart game
function restartGame() {
    gameOverElement.style.display = 'none';
    initGame();
    gameLoop();
}

// Event listeners
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if (e.key === 'r' || e.key === 'R') {
        restartGame();
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
});

canvas.addEventListener('mousedown', (e) => {
    if (e.button === 0) { // Left click
        mouseDown = true;
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (e.button === 0) { // Left click
        mouseDown = false;
    }
});

// Prevent context menu on right click
canvas.addEventListener('contextmenu', (e) => {
    e.preventDefault();
});

// Start the game
initGame();
gameLoop();