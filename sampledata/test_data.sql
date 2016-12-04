TRUNCATE TABLE public.fridge_items, public.products, public.groups_rel, public.groups, public.notification_log, public.users;

INSERT INTO public.users (id, token, longitude, latitude) VALUES (1, 'zellescherweg', 13.750865, 51.028659);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (2, 'wasaplatz', 13.759448, 51.027947);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (3, 'stadion', 13.748923, 51.040867);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (4, 'albertplatz', 13.745956, 51.062852);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (5, 'rosis', 13.747716, 51.070161);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (6, 'bischofsplatz', 13.750688, 51.071368);
INSERT INTO public.users (id, token, longitude, latitude) VALUES (7, 'alaunpark', 13.760054, 51.070256);

INSERT INTO public.groups (id, day) VALUES (3, '2016-12-04');
INSERT INTO public.groups (id, day) VALUES (4, '2016-12-04');

INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (8, 4, 3, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (9, 5, 3, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (10, 6, 3, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (11, 7, 3, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (12, 1, 4, true, false);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (13, 2, 4, true, true);
INSERT INTO public.groups_rel (id, user_id, group_id, invited, accepted) VALUES (14, 3, 4, true, false);

COMMIT;
