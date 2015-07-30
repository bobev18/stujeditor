import sys
from PyQt5 import QtGui, QtCore, QtWidgets


class TreeWidget(QtWidgets.QTreeWidget):
     def __init__(self, parent=None):
         QtWidgets.QTreeWidget.__init__(self, parent)
         self.header().setHidden(True)
         self.setSelectionMode(self.ExtendedSelection)
         self.setDragDropMode(self.InternalMove)
         self.setDragEnabled(True)
         self.setDropIndicatorShown(True)
         def add(num):
             item = QtWidgets.QTreeWidgetItem(self, ['Item(' + str(num) + ')'])
             for i in range(1, 4):
                 QtWidgets.QTreeWidgetItem(item, ['Child(' + str(num) + ',' + str(i) + ')'])
             item.setExpanded(True)
         for i in range(1, 3):
             add(i)

     def dropEvent(self, event):
         if event.source() == self:
             QtWidgets.QAbstractItemView.dropEvent(self, event)

     def dropMimeData(self, parent, row, data, action):
         if action == QtCore.Qt.MoveAction:
             return self.moveSelection(parent, row)
         return False

     def moveSelection(self, parent, position):
	# save the selected items
         selection = [QtCore.QPersistentModelIndex(i)
                      for i in self.selectedIndexes()]
         parent_index = self.indexFromItem(parent)
         if parent_index in selection:
             return False
         # save the drop location in case it gets moved
         target = self.model().index(position, 0, parent_index).row()
         if target < 0:
             target = position
         # remove the selected items
         taken = []
         for index in reversed(selection):
             item = self.itemFromIndex(QtCore.QModelIndex(index))
             if item is None or item.parent() is None:
                 taken.append(self.takeTopLevelItem(index.row()))
             else:
                 taken.append(item.parent().takeChild(index.row()))
         # insert the selected items at their new positions
         while taken:
             if position == -1:
                 # append the items if position not specified
                 if parent_index.isValid():
                     parent.insertChild(
                         parent.childCount(), taken.pop(0))
                 else:
                     self.insertTopLevelItem(
                         self.topLevelItemCount(), taken.pop(0))
             else:
		# insert the items at the specified position
                 if parent_index.isValid():
                     parent.insertChild(min(target,
                         parent.childCount()), taken.pop(0))
                 else:
                     self.insertTopLevelItem(min(target,
                         self.topLevelItemCount()), taken.pop(0))
         return True


if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     tree = TreeWidget()
     tree.resize(200, 300)
     tree.move(300, 300)
     tree.show()
     sys.exit(app.exec_())