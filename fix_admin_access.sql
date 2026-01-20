-- Make saudallosh@gmail.com an admin
UPDATE users SET is_admin = 1 WHERE email = 'saudallosh@gmail.com';

-- Verify the change
SELECT id, email, is_admin, is_active FROM users WHERE email = 'saudallosh@gmail.com';

-- Show all admins
SELECT id, email, name, is_admin FROM users WHERE is_admin = 1;
