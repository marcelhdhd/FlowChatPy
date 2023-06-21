class UserList:
    def __init__(self):
        self.users = []

    def add_user(self, name, ip):
        for user in self.users:
            if user['ip'] == ip:
                if user['name'] == name:
                    print(f"{name} is already in the list.")
                else:
                    user['name'] = name
                    print(f"Name for IP {ip} updated to {name}.")
                break
        else:
            user = {'name': name, 'ip': ip}
            self.users.append(user)
            print(f"{name} added successfully.")

    def get_users(self):
        return self.users

    def remove_user(self, name):
        for user in self.users:
            if user['name'] == name:
                self.users.remove(user)
                print(f"{name} removed successfully.")
                break
        else:
            print(f"{name} is not in the list.")


    def extractnames(self):
        return [entry['name'] for entry in self.users]