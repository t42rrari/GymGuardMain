
INSERT OR IGNORE INTO auth_user
(username, password, is_superuser, first_name, last_name, email,
 is_staff, is_active, date_joined)
VALUES
('admin', 'pbkdf2_sha256$1500000$3iKQi91XDCvaeKLtn7KuC8$JyaQVq7bxkjycGcM6FVASHan+iZGSWDlfE8ah8sRyBk=', 0, 'Gym', 'Admin', 'admin@gymguard.local', 0, 1, CURRENT_TIMESTAMP),

('trainer1', 'pbkdf2_sha256$1500000$8nnlXRLnGcJDDnWetrlnP0$yCq6peQIw7TFsTdK1t+0KQ0qDoRrsLYPgXkcwr5fB8o=', 0, 'John', 'Trainer', 'trainer@gymguard.local', 0, 1, CURRENT_TIMESTAMP),

('receptionist1', 'pbkdf2_sha256$1500000$yGCHf7Or8WF5MIaHHOB0Vg$6AET3brn4Zd8wLkQ8tk6eARkFO0cnWrDWf7bStp0qcw=', 0, 'Jane', 'Receptionist', 'reception@gymguard.local', 0, 1, CURRENT_TIMESTAMP),

('member1', 'pbkdf2_sha256$1500000$weHVUNnLbqiEgknhMajOKu$3GGP6ingJWgV9nIiB2PFL1qoDG/VkfL12UTepDbHn3M=', 0, 'Alex', 'Member', 'member@gymguard.local', 0, 1, CURRENT_TIMESTAMP);


INSERT OR IGNORE INTO users_profile
(user_id, role, phone, specialty, active)
SELECT id, 'admin', '', '', 1
FROM auth_user WHERE username = 'admin';

INSERT OR IGNORE INTO users_profile
(user_id, role, phone, specialty, active)
SELECT id, 'trainer', '', 'General Fitness', 1
FROM auth_user WHERE username = 'trainer1';

INSERT OR IGNORE INTO users_profile
(user_id, role, phone, specialty, active)
SELECT id, 'receptionist', '', '', 1
FROM auth_user WHERE username = 'receptionist1';

INSERT OR IGNORE INTO users_profile
(user_id, role, phone, specialty, active)
SELECT id, 'member', '', '', 1
FROM auth_user WHERE username = 'member1';
