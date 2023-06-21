from PyQt6.QtCore import QAbstractListModel, Qt


class UserListModel(QAbstractListModel):
    def __init__(self, user_list):
        super().__init__()
        self.user_list = user_list

    def rowCount(self, parent):
        return len(self.user_list)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            name = self.user_list[index.row()]['name']
            return name
