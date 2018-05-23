from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from os.path import isdir
from pathlib import Path

class FileDirInput(QWidget):
	
	def __init__(self, parent, camera):
		super(FileDirInput, self).__init__(parent)
		
		# announce camera
		self.camera = camera

		# init UI
		self.initUI()
		
	def initUI(self):
		# section layout
		sublayout_filedir = QHBoxLayout()
		
		# initialise widgets
		self.dirlabel = QLabel('Save Directory:')
		
		self.dirinput = QLineEdit(self.camera.savedir, self)
		self.dirinput.setFixedWidth(165)
		self.dirinput.textChanged.connect(self.ontextchange)
		
		self.dirupdate = QPushButton(QIcon('resources/done-all.svg'), 'Apply', self)
		self.dirupdate.clicked.connect(self.applytextchange)
		self.dirupdate.setEnabled(False)

		# add widgets to vertical box layout
		sublayout_filedir.addWidget(self.dirlabel)
		sublayout_filedir.addWidget(self.dirinput)
		sublayout_filedir.addWidget(self.dirupdate)

		# set sublayout as widget layout
		self.setLayout(sublayout_filedir)
		
	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.savedir)
		
		if same:
			self.dirupdate.setEnabled(False)
			
		elif not same:
			self.dirupdate.setEnabled(True)
			
	@pyqtSlot()
	def applytextchange(self):
		# get text from box
		textbox_mod = self.dirinput.text()
		
		# ensure directory string ends and starts with '/' if not append
		if len(textbox_mod)>0 and textbox_mod[-1]!='/':
			textbox_mod = textbox_mod + '/'
			
		if len(textbox_mod)>0 and textbox_mod[0]!='/':
			textbox_mod = '/' + textbox_mod
			
		if len(textbox_mod)==0:
			textbox_mod = '/'
			
		# check directory exists, if not raise question box
		if isdir(textbox_mod):
			self.camera.savedir = textbox_mod
			
		elif not isdir(textbox_mod):
			dir_question = QMessageBox.question(self, 'Non-existent Directory', 
												'Directory: "' + textbox_mod + '" does not exist.\nDo you want to create it?', 
												QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Yes)
					
			if dir_question == QMessageBox.Yes:
				Path(textbox_mod).mkdir(parents=True, exist_ok=True)
				self.camera.savedir = textbox_mod

		# update text in box
		self.dirinput.setText(textbox_mod) 
		
		# make sure apply button updates
		self.ontextchange(textbox_mod)

class NameFormatInput(QWidget):
	
	def __init__(self, parent, camera):
		super(NameFormatInput, self).__init__(parent)
		
		# announce camera
		self.camera = camera

		# init UI
		self.initUI()
		
	def initUI(self):
		# section layout
		sublayout_filedir = QHBoxLayout()
		
		# initialise widgets
		self.namelabel = QLabel('Name Format:')
		
		self.nameinput = QLineEdit(self.camera.nameformat, self)
		self.nameinput.setFixedWidth(165)
		self.nameinput.textChanged.connect(self.ontextchange)
		
		self.nameupdate = QPushButton(QIcon('resources/done-all.svg'), 'Apply', self)
		self.nameupdate.clicked.connect(self.applytextchange)
		self.nameupdate.setEnabled(False)

		# add widgets to vertical box layout
		sublayout_filedir.addWidget(self.namelabel)
		sublayout_filedir.addWidget(self.nameinput)
		sublayout_filedir.addWidget(self.nameupdate)

		# set sublayout as widget layout
		self.setLayout(sublayout_filedir)
		
	@pyqtSlot(str)	
	def ontextchange(self, textbox_in):
		# check whether text in box different to current save directory
		# and make apply button active/inactive as appropriate
		same = (textbox_in == self.camera.nameformat)
		
		if same:
			self.nameupdate.setEnabled(False)
			
		elif not same:
			self.nameupdate.setEnabled(True)
			
	@pyqtSlot()
	def applytextchange(self):
		# set file name format 
		self.camera.nameformat = self.nameinput.text()
		
		# update apply button
		self.ontextchange(self.nameinput.text())
		
class FileManagementSection(QGroupBox):
	
	def __init__(self, parent, camera):
		super(FileManagementSection, self).__init__(parent)
		
		# announce camera handle
		self.camera = camera
		
		# init UI
		self.initUI()
		
	def initUI(self):
		# general settings
		self.setTitle('File Management')
		
		# section layout
		sublayout_fileman = QVBoxLayout()
		
		# initialise widgets
		self.dirinput = FileDirInput(self, self.camera)
		self.nameformat = NameFormatInput(self, self.camera)
		#~ self.fileformat = 

		# add widgets to vertical box layout
		sublayout_fileman.addWidget(self.dirinput)
		sublayout_fileman.addWidget(self.nameformat)
		#~ sublayout_fileman.addWidget(self.fileformat)

		# set sublayout as widget layout
		self.setLayout(sublayout_fileman)

	