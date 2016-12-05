TRUNCATE TABLE public.fridge_items, public.products, public.groups_rel, public.groups, public.notification_log, public.users, public.group_recipes;

INSERT INTO public.users (id, token, longitude, latitude) VALUES (1, 'zellescherweg', 13.750865, 51.028659);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (2, 'wasaplatz', 13.759448, 51.027947);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (3, 'stadion', 13.748923, 51.040867);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (4, 'albertplatz', 13.745956, 51.062852);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (5, 'rosis', 13.747716, 51.070161);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (6, 'bischofsplatz', 13.750688, 51.071368);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (7, 'alaunpark', 13.760054, 51.070256);
ALTER SEQUENCE users_id_seq RESTART WITH 8;
INSERT INTO public.groups (id, day) VALUES (3, '2016-12-04');
INSERT INTO public.groups (id, day) VALUES (4, '2016-12-04');

INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (8, 4, 3, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (9, 5, 3, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (10, 6, 3, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (11, 7, 3, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (12, 1, 4, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (13, 2, 4, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (14, 3, 4, true, false);

INSERT INTO products (ean, name, type) VALUES (123, 'Butter', 4);
INSERT INTO products (ean, name, type) VALUES (321, 'Eggs', 5);
INSERT INTO products (ean, name, type) VALUES (231, 'Milk', 8);
INSERT INTO products (ean, name, type) VALUES (121, 'Flour',6);
INSERT INTO products (ean, name, type) VALUES (222, 'Tomato', 12);

INSERT INTO fridge_items (ean, user_id) VALUES (123, 1), (231, 1), (222, 1), (321, 2), (121, 2), (222, 3), (123, 3), (123, 4), (321, 4), (231, 4), (121, 5), (231, 5), (321, 5), (123, 6), (321, 6), (231, 6), (121, 6), (222, 7);
COMMIT;
