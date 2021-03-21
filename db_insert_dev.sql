INSERT INTO "main"."sqlalchemy_app_user" ("id", "username", "email", "password_hash", "about_me", "last_seen") VALUES ('3', 'marc', 'test@test.com', 'pbkdf2:sha256:150000$mQxIVU2r$b30bf932d42b1e62bf7a5e8d25253a2791a2e7e4ad8df9f7eef0aca73361d676', 'Hello Hello Hello
My dear', '2021-03-21 15:52:40.992035');
INSERT INTO "main"."sqlalchemy_app_user" ("id", "username", "email", "password_hash", "about_me", "last_seen") VALUES ('4', 'susan', 'supi@super.com', 'pbkdf2:sha256:150000$ZIqdAvlg$5a6505f4413b74ae4ba80f96bed83fcbd952f3fd6d2a72c227d2a288e5526184', '', '2020-10-29 13:50:12.083333');
INSERT INTO "main"."sqlalchemy_app_city" ("id", "name") VALUES ('1', 'London');
INSERT INTO "main"."sqlalchemy_app_teams" ("id", "name", "city_id", "create_user_id", "create_timestamp") VALUES ('1', 'FC London', '1', '3', '2020-10-29 15:41:28.011446');
INSERT INTO "main"."sqlalchemy_app_players" ("id", "team_id", "name", "position") VALUES ('1', '1', 'John Cusack', 'Center');
