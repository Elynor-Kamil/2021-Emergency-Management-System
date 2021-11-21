from models.admin import Admin
from models.volunteer import Volunteer

root_user = Admin('root', 'root')
volunteer_test = Volunteer('volroot', 'volroot')
users_catalog = {
    root_user.username: root_user,
    volunteer_test.username: volunteer_test

}
