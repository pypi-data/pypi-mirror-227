from src.simpleusers.users import usermgr

u = usermgr()

u.make_user("testuser", "testpass")

u.set_auth_token("testuser", "1.1.1.1", "testtoken")

print(u.get_user("testuser"))

print(u.auth_user_with_token("testuser", "testtoken"))
