from models.admin import Admin

root_user = Admin('root', 'root')
users_catalog = {
    root_user.username: root_user
}
