-- Incremental migrations — safe to re-run (CREATE IF NOT EXISTS)

USE che_bepazam;

CREATE TABLE IF NOT EXISTS recipe_ratings (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    rating          ENUM('love','good','ok','bad') NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_recipe_rating (user_id, recipe_id),
    INDEX idx_rating_recipe (recipe_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_cooked_recipes (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    cook_count      INT UNSIGNED NOT NULL DEFAULT 1,
    last_cooked_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_cooked (user_id, recipe_id),
    INDEX idx_cooked_user (user_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_disliked_recipes (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_dislike (user_id, recipe_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ingredient_substitutes (
    id                      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ingredient_id           INT UNSIGNED NOT NULL,
    substitute_ingredient_id INT UNSIGNED NOT NULL,
    note                    VARCHAR(256) NULL,
    is_active               TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    FOREIGN KEY (substitute_ingredient_id) REFERENCES ingredients(id),
    UNIQUE KEY uk_substitute_pair (ingredient_id, substitute_ingredient_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_shopping_cart (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    recipe_id       INT UNSIGNED NOT NULL,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    UNIQUE KEY uk_cart_recipe (user_id, recipe_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_screen_state (
    user_id         INT UNSIGNED NOT NULL PRIMARY KEY,
    screen          VARCHAR(64) NOT NULL,
    payload         JSON NULL,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bot_promotions (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    slot            VARCHAR(32) NOT NULL UNIQUE,
    title           VARCHAR(128) NULL,
    body_text       TEXT NOT NULL,
    button_label    VARCHAR(64) NOT NULL,
    link_url        VARCHAR(512) NOT NULL,
    is_active       TINYINT(1) NOT NULL DEFAULT 1,
    sort_order      INT NOT NULL DEFAULT 0,
    updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT IGNORE INTO bot_promotions (slot, title, body_text, button_label, link_url, is_active) VALUES
(
    'main_menu',
    'HyperTunnel VPN',
    'اینترنت سریع و پایدار — اتصال امن با VPN اختصاصی',
    '🛡  HyperTunnel VPN',
    'https://t.me/HyperTunnelbot',
    1
);

-- Seed real ingredient substitutes (existing IDs only)
INSERT IGNORE INTO ingredient_substitutes (ingredient_id, substitute_ingredient_id, note) VALUES
    (37, 95, 'در پخت برخی غذاها'),
    (26, 121, 'برای سالاد'),
    (98, 18, 'در سوپ'),
    (28, 148, 'ترش‌کنندگی'),
    (2, 60, 'در خورش‌ها'),
    (14, 90, 'بلغور');
