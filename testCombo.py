class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self._data.iat[index.row(), self._data.shape[1]-1] = value
            self.dataChanged.emit(index, index)
            return True

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self._changed = False
        self.view().pressed.connect(self.handleItemPressed)
        self.checked_item=[]
        
        for i in range(len(dept_list)):
            self.addItem(dept_list[i])
            self.setItemChecked(i, False)


    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn())  # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)

        else:
            item.setCheckState(Qt.Unchecked)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
            if item.text() in self.checked_item:


                self.checked_item.remove(item.text())
            print(self.checked_item)

        else:
            item.setCheckState(Qt.Checked)
            self.checked_item.append(item.text())
            print(self.checked_item)
        self._changed = True
        
        self.check_items()

    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False


    def item_checked(self, index):
  
        # getting item at index
        item = self.model().item(index, 0)
  
        # return true if checked else false
        return item.checkState() == Qt.Checked
    
    def check_items(self):
        # blank list
        checkedItems = []
  
        # traversing the items
        for i in range(self.count()):
  
            # if item is checked add it to the list
            if self.item_checked(i):
                checkedItems.append(i)
                # checkedItems.append(self.model().item(i, 0).text())
  
        # call this method
        self.update_labels(checkedItems)
  
    # method to update the label
    def update_labels(self, item_list):
  
        n = ''
        count = 0
  
        # traversing the list
        for i in item_list:
  
            # if count value is 0 don't add comma
            if count == 0:
                n += ' % s' % i
            # else value is greater then 0
            # add comma
            else:
                n += ', % s' % i
  
            # increment count
            count += 1
  
  
        # loop
        for i in range(self.count()):
  
            # getting label
            text_label = self.model().item(i, 0).text()
  
            # default state
            if text_label.find('-') >= 0:
                text_label = text_label.split('-')[0]
  
            # shows the selected items
            item_new_text_label = text_label + ',' + n
  
           # setting text to combo box
            self.setItemText(i, item_new_text_label)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.combo_box_list=[]
        import pandas as pd
        df = pd.read_excel(r"E:\092021-12 2022 1001.xlsx", skiprows=7)

        # data = pd.DataFrame([[1, 9, 2], [1, 0, -1], [3, 5, 2], [3, 3, 2], [5, 8, 9],],
        #                     columns=["A", "B", "C"],
        #                     index=["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"],)

        df['Allocation Selection'] = ''
        df['Allocation']=''

        self.model = TableModel(df)
        self.table.setModel(self.model)
        # combo = CheckableComboBox()
        # for i in range(len(dept_list)):
        #     combo.addItem(dept_list[i])
        #     combo.setItemChecked(i, False)

        for i in range(df.shape[0]):
            combo = CheckableComboBox()
            self.combo_box_list.append(combo)
            # pix = QPersistentModelIndex(index)
            # combo.currentIndexChanged[str].connect(lambda txt, pix=pix: self.tableView.model().setData(QModelIndex(pix), txt))
            self.table.setIndexWidget(self.model.index(i, df.shape[1] - 2), combo)
        self.setCentralWidget(self.table)
        self.setGeometry(600, 100, 400, 200)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()