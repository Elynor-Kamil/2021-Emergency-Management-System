import volunteer

def createVolunteerAccount():
    volunteerAccount_file = open('volunteerAccount.txt', 'a')
    volunteerAccount_dict = {}
    volunteerAccount_dict_newUsername = input('New Volunteer Username: ')
    volunteerAccount_dict[volunteerAccount_dict_newUsername] = input('New Volunteer Password: ')
    for k, v in volunteerAccount_dict.items():
        volunteerAccount_file.write(str(k)+' '+str(v)+'\n')
    volunteerAccount_file.close()
    volunteerAccount_file = open('volunteerAccount.txt', 'r')
    for line in volunteerAccount_file:
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        volunteerAccount_dict[k] = v
    volunteerAccount_file.close()
    name = input('Volunteer Name: ')
    phone = input('Volunteer Phone Number: ')
    volunteer = Volunteer(name, phone, volunteercamp="UCL", availability=True)
    print(volunteer)

if __name__ == "__main__":
    createVolunteerAccount()