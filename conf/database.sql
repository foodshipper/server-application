CREATE TABLE IF NOT EXISTS rec_recipes (
  id           SERIAL PRIMARY KEY,
  external_id  INTEGER UNIQUE,
  title        VARCHAR(150),
  image        VARCHAR(255),
  duration     INTEGER,
  servings     INTEGER,
  vegetarian   BOOLEAN,
  vegan        BOOLEAN,
  cheap        BOOLEAN,
  instructions TEXT
);

CREATE TABLE IF NOT EXISTS product_types (
  id          SERIAL PRIMARY KEY,
  external_id INTEGER UNIQUE,
  category    VARCHAR(40),
  "name"      VARCHAR(40),
  image       VARCHAR(255)
);

INSERT INTO product_types (id, "name") VALUES (1, 'undefined');
ALTER SEQUENCE product_types_id_seq RESTART WITH 2;

CREATE TABLE IF NOT EXISTS products (
  ean  VARCHAR(13) PRIMARY KEY,
  name VARCHAR(100),
  type SERIAL REFERENCES product_types(id)
);


CREATE TABLE IF NOT EXISTS rec_ingredients (
  id         SERIAL PRIMARY KEY,
  product_id SERIAL REFERENCES product_types (id),
  recipe_id  SERIAL REFERENCES rec_recipes (id),
  amount     REAL,
  unit       VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS users (
  id             SERIAL PRIMARY KEY,
  token          VARCHAR(64),
  firebase_token VARCHAR(255) DEFAULT NULL,
  longitude      DOUBLE PRECISION,
  latitude       DOUBLE PRECISION,
  geom           GEOGRAPHY(POINT, 4326),
  name           VARCHAR(30)  DEFAULT NULL
);

CREATE OR REPLACE FUNCTION set_user_geom()
  RETURNS TRIGGER AS $set_user_geom$ BEGIN NEW.geom := st_makepoint(NEW.latitude, NEW.longitude);
  RETURN NEW;
END;$set_user_geom$ LANGUAGE plpgsql;

CREATE TRIGGER user_geom
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE PROCEDURE set_user_geom();

CREATE TABLE IF NOT EXISTS fridge_items (
  id      SERIAL PRIMARY KEY,
  ean     VARCHAR(13) REFERENCES products (ean),
  user_id SERIAL REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS groups (
  id  SERIAL PRIMARY KEY,
  day DATE
);

CREATE TABLE IF NOT EXISTS groups_rel (
  id       SERIAL PRIMARY KEY,
  user_id  SERIAL REFERENCES users (id),
  group_id SERIAL REFERENCES groups (id),
  invited  BOOL DEFAULT FALSE,
  accepted BOOL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS group_recipes (
  id        SERIAL PRIMARY KEY,
  group_id  SERIAL REFERENCES groups (id),
  recipe_id SERIAL REFERENCES rec_recipes (id)
);

CREATE TABLE IF NOT EXISTS group_recipe_vote_log (
  id        SERIAL PRIMARY KEY ,
  grecipe_id SERIAL REFERENCES group_recipes(id),
  user_id   SERIAL REFERENCES users(id),
  action    VARCHAR(10),
  time      TIMESTAMP
);

CREATE OR REPLACE FUNCTION unique_recipe_vote()
  RETURNS TRIGGER AS $unique_recipe_vote$ BEGIN
  WITH votes AS
    (SELECT SUM((action='upvote')::INT) as upvotes, SUM((action='veto')::INT) > 0 as veto FROM
      (SELECT DISTINCT ON (user_id) action FROM group_recipe_vote_log WHERE grecipe_id = NEW.grecipe_id ORDER BY user_id, time DESC) as vote_log)
  UPDATE group_recipes SET
    upvotes=(SELECT upvotes FROM votes),
    veto=(SELECT veto FROM votes)
    WHERE group_recipes.id = NEW.grecipe_id;
  RETURN NEW;
END; $unique_recipe_vote$ LANGUAGE plpgsql;

CREATE TRIGGER group_recipe_votes
AFTER INSERT OR UPDATE ON group_recipe_vote_log
FOR EACH ROW EXECUTE PROCEDURE unique_recipe_vote();

CREATE OR REPLACE FUNCTION unique_group_member()
  RETURNS TRIGGER AS $unique_group_member$ BEGIN IF EXISTS(SELECT TRUE
                                                           FROM groups_rel
                                                             LEFT JOIN groups ON groups_rel.group_id = groups.id
                                                           WHERE day = CURRENT_DATE AND user_id = NEW.user_id)
THEN RAISE EXCEPTION 'Group Member can not be in two groups on the same day'; END IF;
  RETURN NEW;
END; $unique_group_member$ LANGUAGE plpgsql;

CREATE TRIGGER groups_rel_unique
BEFORE INSERT ON groups_rel
FOR EACH ROW EXECUTE PROCEDURE unique_group_member();

CREATE TABLE IF NOT EXISTS notification_log (
  id      SERIAL PRIMARY KEY,
  user_id SERIAL REFERENCES users (id),
  type    VARCHAR(15),
  time    TIMESTAMP DEFAULT NOW(),
  success BOOL      DEFAULT FALSE,
  msg     TEXT
);

INSERT INTO product_types(external_id, name, category, image) VALUES (10123, 'bacon', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/raw-bacon.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11090, 'broccoli', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/broccoli.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1001, 'butter', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1123, 'eggs', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/egg.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (20081, 'flour', 'Baking', 'https://spoonacular.com/cdn/ingredients_100x100/flour.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (1082047, 'kosher salt', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1077, 'milk', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/milk.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11282, 'onion', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/brown-onion.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11353, 'russet potatoes', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/russet-or-Idaho-potatoes.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1031009, 'sharp cheddar cheese', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/cheddar-cheese.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11529, 'tomato', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/tomato.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (4513, 'vegetable oil', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/vegetable-oil.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (14412, 'water', 'Beverages', 'https://spoonacular.com/cdn/ingredients_100x100/water.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (42130, 'turkey bacon', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/bacon-turkey.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1011, 'colby monterey jack cheese', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/cheddar-cheese.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1085, 'fat-free milk', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/milk.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (31015, 'green chilies', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/chili-peppers-green.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (4053, 'olive oil', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/olive-oil.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1002030, 'pepper', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/pepper.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10411529, 'plum tomatoes', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/plum-tomatoes.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (10011355, 'red potatoes', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/red-potatoes.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11821, 'red sweet pepper', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/red-bell-pepper.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (2047, 'salt', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11294, 'sweet onion', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/sweet-onion.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2053, 'white vinegar', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/vinegar-(white).jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2027, 'dried oregano', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/oregano.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (14097, 'dry red wine', 'Alcoholic Beverages', 'https://spoonacular.com/cdn/ingredients_100x100/red-wine.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1125, 'egg yolk', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/hard-boiled-egg.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11209, 'eggplants', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/eggplant.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11297, 'fresh parsley leaves', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/parsley-curly.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11215, 'garlic', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/garlic.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10023572, 'ground beef', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/fresh-ground-beef.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (17224, 'ground lamb', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/meat-ground.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1033, 'parmesan', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/parmesan-or-romano.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11887, 'tomato paste', 'Pasta and Rice', 'https://spoonacular.com/cdn/ingredients_100x100/tomato-paste.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1145, 'unsalted butter', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (13926, 'beef tenderloin', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/beef-tenderloin.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (18064, 'bread', 'Bakery/Bread', 'https://spoonacular.com/cdn/ingredients_100x100/white-bread.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (18079, 'bread crumbs', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/breadcrumbs.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1053, 'cream', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/fluid-cream.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11206, 'cucumber', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/cucumber.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10111529, 'grape tomatoes', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/cherry-tomatoes.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (19296, 'honey', 'Health Foods', 'https://spoonacular.com/cdn/ingredients_100x100/honey.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1022027, 'italian seasoning', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/Herbes-de-Provence.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (9152, 'lemon juice', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/lemon-juice.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (9160, 'lime juice', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/lime-juice.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11362, 'potato', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/potatoes-yukon-gold.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10011282, 'red onion', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/red-onion.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10011457, 'spinach', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/spinach.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10211362, 'yukon gold potatoes', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/potatoes-yukon-gold.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2004, 'bay leaves', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/bay-leaves.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (13147, 'beef short ribs', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/beef-short-ribs.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10011693, 'canned tomatoes', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/tomatoes-canned.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11124, 'carrot', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/carrots.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11143, 'celery', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/celery.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2038, 'fresh sage', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/sage.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2049, 'fresh thyme', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/thyme.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1002028, 'hungarian sweet paprika', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/paprika.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (6970, 'low-salt chicken broth', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/broth.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11298, 'parsnips', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/parsnip.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10111282, 'pearl onions', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/pearl-onions.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10210123, 'slab bacon', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/bacon.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11564, 'turnips', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/turnips.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (11531, 'canned diced tomatoes', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/tomatoes-canned.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (9085, 'currants', 'Dried Fruits', 'https://spoonacular.com/cdn/ingredients_100x100/blueberries-dried.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11165, 'fresh cilantro', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/cilantro.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (1029003, 'granny smith apple', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apples.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2012, 'ground coriander', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/ground-coriander.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1002014, 'ground cumin', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/ground-cumin.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (4025, 'mayonnaise', 'Condiments', 'https://spoonacular.com/cdn/ingredients_100x100/mayonnaise.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2046, 'mustard', 'Condiments', 'https://spoonacular.com/cdn/ingredients_100x100/mustard.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11982, 'pasilla pepper', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/guajillo-chiles.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1007063, 'pork links', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/raw-pork-sausage.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1012047, 'sea salt', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (4615, 'shortening', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/shortening.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1056, 'sour cream', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/sour-cream.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11507, 'sweet potato', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/sweet-potato.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (6168, 'tabasco sauce', 'Condiments', 'https://spoonacular.com/cdn/ingredients_100x100/hot-sauce-or-tabasco.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (2032, 'white pepper', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/white-pepper.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1011004, 'gorgonzola cheese', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/gorgonzola.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (93625, 'natural cane sugar', 'Health Foods', 'https://spoonacular.com/cdn/ingredients_100x100/evaporated-cane-juice.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (2025, 'nutmeg', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/ground-nutmeg.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10020080, 'whole wheat pastry flour', 'Baking', 'https://spoonacular.com/cdn/ingredients_100x100/flour.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (1004073, 'stick margarine', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11955, 'sun-dried tomatoes', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/sundried-tomatoes.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (5006, 'chicken', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (19334, 'brown sugar', 'Baking', 'https://spoonacular.com/cdn/ingredients_100x100/brown-sugar-dark.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (4582, 'canola oil', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/vegetable-oil.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (6972, 'chili sauce', 'Ethnic Foods', 'https://spoonacular.com/cdn/ingredients_100x100/tomato-sauce-or-pasta-sauce.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11333, 'green bell pepper', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/green-bell-pepper.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1002024, 'ground mustard', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/dry-mustard.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (98940, 'submarine sandwich buns', 'Bakery/Bread', 'https://spoonacular.com/cdn/ingredients_100x100/kaiser-roll.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11435, 'rutabaga', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/rutabaga.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (18371, 'baking powder', 'Baking', 'https://spoonacular.com/cdn/ingredients_100x100/white-powder.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11109, 'cabbage', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/cabbage.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (2005, 'caraway seeds', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/caraway-seeds.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10088, 'pork spareribs', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/spare-ribs.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (18060, 'rye bread', 'Bakery/Bread', 'https://spoonacular.com/cdn/ingredients_100x100/rye-bread.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10165, 'salt pork', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/pork-belly.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11439, 'sauerkraut', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/sauerkraut.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11533, 'stewed tomatoes', 'Canned and Jarred', 'https://spoonacular.com/cdn/ingredients_100x100/tomatoes-canned.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10011090, 'broccoli florets', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/broccoli.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1001009, 'shredded cheddar cheese', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/shredded-cheese-cheddar.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (2007, 'celery seed', 'Spices and Seasonings', 'https://spoonacular.com/cdn/ingredients_100x100/celery-seed.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11583, 'stew vegetables', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/mixed-vegetables.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (15076, 'salmon', 'Seafood', 'https://spoonacular.com/cdn/ingredients_100x100/salmon.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (23562, '90% lean ground beef', 'Meat', 'https://spoonacular.com/cdn/ingredients_100x100/meat-ground-red.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11011, 'asparagus', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/asparagus.png');
INSERT INTO product_types(external_id, name, category, image) VALUES (1034053, 'extra virgin olive oil', 'Oil, Vinegar, Salad Dressing', 'https://spoonacular.com/cdn/ingredients_100x100/olive-oil.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10211529, 'roma tomato', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/roma-tomatoes.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11951, 'yellow bell pepper', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/yellow-bell-pepper.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11477, 'zucchini', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/zucchini.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (10020444, 'basmati rice', 'Pasta and Rice', 'https://spoonacular.com/cdn/ingredients_100x100/rice-white-long-grain-or-basmatii-cooked.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1009, 'cheddar cheese', 'Cheese', 'https://spoonacular.com/cdn/ingredients_100x100/cheddar-cheese.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (11291, 'green onions', 'Produce', 'https://spoonacular.com/cdn/ingredients_100x100/green-onion.jpg');
INSERT INTO product_types(external_id, name, category, image) VALUES (1174, 'low fat milk', 'Milk, Eggs, Other Dairy', 'https://spoonacular.com/cdn/ingredients_100x100/milk.jpg');