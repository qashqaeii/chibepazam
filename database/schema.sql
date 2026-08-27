-- Database schema for «غذا چی بپزم؟» Telegram Bot
-- MySQL 8+

CREATE DATABASE IF NOT EXISTS che_bepazam
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE che_bepazam;

-- ─── Users ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    telegram_id     BIGINT NOT NULL UNIQUE,
    username        VARCHAR(64)  NULL,
    first_name      VARCHAR(128) NULL,
    last_name       VARCHAR(128) NULL,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    is_blocked      TINYINT(1) NOT NULL DEFAULT 0,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_last_seen (last_seen_at)
) ENGINE=InnoDB;

-- ─── Admins ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS admins (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    telegram_id     BIGINT NOT NULL UNIQUE,
    name            VARCHAR(128) NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ─── Ingredient Categories ───────────────────────────────
CREATE TABLE IF NOT EXISTS ingredient_categories (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(64)  NOT NULL,
    slug            VARCHAR(64)  NOT NULL UNIQUE,
    emoji           VARCHAR(8)   NOT NULL DEFAULT '🥕',
    sort_order      INT NOT NULL DEFAULT 0,
    is_active       TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- ─── Ingredients ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ingredients (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_id     INT UNSIGNED NOT NULL,
    name            VARCHAR(128) NOT NULL,
    slug            VARCHAR(128) NOT NULL UNIQUE,
    emoji           VARCHAR(8)   NOT NULL DEFAULT '🥕',
    is_common       TINYINT(1) NOT NULL DEFAULT 0,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    sort_order      INT NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES ingredient_categories(id),
    INDEX idx_ingredients_category (category_id)
) ENGINE=InnoDB;

-- ─── Recipe Categories ───────────────────────────────────
CREATE TABLE IF NOT EXISTS recipe_categories (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(64)  NOT NULL,
    slug            VARCHAR(64)  NOT NULL UNIQUE,
    emoji           VARCHAR(8)   NOT NULL DEFAULT '🍲',
    sort_order      INT NOT NULL DEFAULT 0,
    is_active       TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB;

-- ─── Recipes ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS recipes (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_id     INT UNSIGNED NULL,
    name            VARCHAR(256) NOT NULL,
    slug            VARCHAR(256) NOT NULL UNIQUE,
    emoji           VARCHAR(8)   NOT NULL DEFAULT '🍲',
    description     TEXT NULL,
    prep_time       INT NOT NULL DEFAULT 0,
    cook_time       INT NOT NULL DEFAULT 0,
    servings        INT NOT NULL DEFAULT 4,
    difficulty      ENUM('easy','medium','hard') NOT NULL DEFAULT 'medium',
    cost_level      ENUM('low','medium','high') NOT NULL DEFAULT 'medium',
    is_vegetarian   TINYINT(1) NOT NULL DEFAULT 0,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    rating          DECIMAL(2,1) NOT NULL DEFAULT 4.0,
    image_file_id   VARCHAR(256) NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES recipe_categories(id),
    INDEX idx_recipes_active (is_active),
    FULLTEXT idx_recipes_search (name, description)
) ENGINE=InnoDB;

-- ─── Recipe Ingredients ──────────────────────────────────
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    recipe_id       INT UNSIGNED NOT NULL,
    ingredient_id   INT UNSIGNED NOT NULL,
    amount          VARCHAR(64) NULL,
    unit            VARCHAR(32) NULL,
    importance      TINYINT UNSIGNED NOT NULL DEFAULT 5,
    is_required     TINYINT(1) NOT NULL DEFAULT 0,
    is_optional     TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY uk_recipe_ingredient (recipe_id, ingredient_id),
    INDEX idx_ri_recipe (recipe_id),
    INDEX idx_ri_ingredient (ingredient_id)
) ENGINE=InnoDB;

-- ─── User Pantry (session ingredients) ───────────────────
CREATE TABLE IF NOT EXISTS user_pantry (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    ingredient_id   INT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY uk_user_pantry (user_id, ingredient_id),
    INDEX idx_pantry_user (user_id)
) ENGINE=InnoDB;

-- ─── Permanent Pantry ────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_permanent_ingredients (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    ingredient_id   INT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY uk_user_permanent (user_id, ingredient_id),
    INDEX idx_permanent_user (user_id)
) ENGINE=InnoDB;

-- ─── Favorites ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_favorites (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_favorite (user_id, recipe_id),
    INDEX idx_favorites_user (user_id)
) ENGINE=InnoDB;

-- ─── History ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_history (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    viewed_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    INDEX idx_history_user (user_id, viewed_at DESC)
) ENGINE=InnoDB;

-- ─── User Settings ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_settings (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL UNIQUE,
    servings        INT NOT NULL DEFAULT 4,
    diet_type       ENUM('none','vegetarian','vegan') NOT NULL DEFAULT 'none',
    notifications   TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ─── User Forbidden Ingredients ──────────────────────────
CREATE TABLE IF NOT EXISTS user_forbidden_ingredients (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    ingredient_id   INT UNSIGNED NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY uk_user_forbidden (user_id, ingredient_id)
) ENGINE=InnoDB;

-- ─── Search History ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_search_history (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    query           VARCHAR(256) NOT NULL,
    searched_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_search_user (user_id)
) ENGINE=InnoDB;

-- ─── Bot Events (analytics) ──────────────────────────────
CREATE TABLE IF NOT EXISTS bot_events (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NULL,
    event_type      VARCHAR(64) NOT NULL,
    event_data      JSON NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_events_type_date (event_type, created_at),
    INDEX idx_events_user (user_id)
) ENGINE=InnoDB;

-- ─── User Navigation Stack (for back button) ─────────────
CREATE TABLE IF NOT EXISTS user_nav_stack (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    screen          VARCHAR(64) NOT NULL,
    payload         JSON NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_nav_user (user_id, id DESC)
) ENGINE=InnoDB;

-- ─── Rate Limiting ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS rate_limits (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    telegram_id     BIGINT NOT NULL,
    action          VARCHAR(32) NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rate_telegram (telegram_id, action, created_at)
) ENGINE=InnoDB;
