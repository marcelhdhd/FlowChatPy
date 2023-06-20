class UserList:
    def __init__(self):
        self.users = []

    def add_user(self, name):
        if name in self.users:
            print(f"{name} is already in the list.")
        else:
            self.users.append(name)
            print(f"{name} added successfully.")

    def get_users(self):
        return self.users

    def remove_user(self, name):
        if name in self.users:
            self.users.remove(name)
            print(f"{name} removed successfully.")
        else:
            print(f"{name} is not in the list.")