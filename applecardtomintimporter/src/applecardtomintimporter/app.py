"""
Import your CSV Apple Card statements to Mint to properly track transactions!
"""
import toga
from toga import style
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, TEXT_ALIGN_CHOICES
import json
from toga import validators
from subprocess import call
import os
import os.path

from travertino.constants import CENTER



class AppleCardtoMintImporter(toga.App):	
		def action_open_file_dialog(self, widget):
				try:
						fname = self.main_window.open_file_dialog(
							title="Choose the Apple Card statement you'd like to import",
							multiselect=False
						)
						if fname is not None:
							self.label.text = "File to open:" + fname
						else:
							self.label.text = "No file selected!"
				except ValueError:
						self.label.text = "Open file dialog was canceled"
				self.csv_name = fname

		def import_statement(self, widget):
			data = {}
			data['changes'] = []
			data['changes'].append({
				'cookie': self.cookie_input.value,
				'token': self.token_input.value,
				'csv_name': self.csv_name,
			})

			with open(os.path.join(os.path.dirname(__file__), 'changes.txt'), 'w+') as outfile:
				json.dump(data, outfile)

			with open(os.path.join(os.path.dirname(__file__), 'changes.txt')) as json_file:
				data = json.load(json_file)
				for p in data['changes']:
					cook = p['cookie']
					toke = p['token']
					CSV = p['csv_name']

			self.label.text = CSV + cook + toke
			#call(["python", "import_script.py"])

		def set_variables(self,widget):
			data = {}
			data['permanent_vars'] = []
			data['permanent_vars'].append({
				'account': self.account_input.value,
				'tag1': self.tag1_input.value,
				'tag2': self.tag2_input.value,
				'tag3': self.tag3_input.value
			})

			with open(os.path.join(os.path.dirname(__file__), 'perm.txt'), 'w+') as outfile:
				json.dump(data, outfile)

			self.label.text = "Info has been updated! Please close this window to continue."
		
		def perm_variables(self,widget):
			main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
			info = toga.Label(
				"Please add the requested info from Mint after getting info from the transaction event in your browser.\n" + 
				"If you have previously entered this information, you shouldn't have to do it again,\nbut if you have issues running the program, try updating ALL fields again!", style=Pack(text_align=CENTER))
			main_box.add(info)
			self.perm_window = toga.Window(
				title="Setting Mint Account Data",
				size=(500, 250),
				resizeable=False,)
			self.perm_window.content = main_box
			self.perm_window.show()

			account_label = toga.Label(
				'Account #: ',
				style=Pack(padding=(0))
			)

			self.account_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='Can be found in the POST request form body in your browser devtools',
				validators=[
					validators.MinLength(1)
					]
				)

			account_box = toga.Box(style=Pack(direction=ROW, padding=5))
			account_box.add(account_label)
			account_box.add(self.account_input)

			tag1_label = toga.Label(
				'Tag 1: ',
				style=Pack(padding=(0))
			)
			self.tag1_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='tagXXXXXXX',
				validators=[
					validators.MinLength(1)
					]
				)

			tag2_label = toga.Label(
				'Tag 2: ',
				style=Pack(padding=(0))
			)
			self.tag2_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='tagXXXXXXX',
				validators=[
					validators.MinLength(1)
					]
				)

			tag3_label = toga.Label(
				'Tag 3: ',
				style=Pack(padding=(0))
			)
			self.tag3_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='tagXXXXXXX',
				validators=[
					validators.MinLength(1)
					]
				)

			tag1_box = toga.Box(style=Pack(direction=ROW, padding=5))
			tag1_box.add(tag1_label)
			tag1_box.add(self.tag1_input)
			tag2_box = toga.Box(style=Pack(direction=ROW, padding=5))
			tag2_box.add(tag2_label)
			tag2_box.add(self.tag2_input)
			tag3_box = toga.Box(style=Pack(direction=ROW, padding=5))
			tag3_box.add(tag3_label)
			tag3_box.add(self.tag3_input)

			main_box.add(account_box)
			main_box.add(tag1_box)
			main_box.add(tag2_box)
			main_box.add(tag3_box)

			#btnClose = toga.Button(
			#	'Close this window',
			#	on_press=self.perm_window.show(),
			#	style=Pack(padding=5)

			#)
			#main_box.add(btnClose)

			update_info_btn = toga.Button(
				'Save Info',
				on_press=self.set_variables,
				style=Pack(padding=5)
			)

			main_box.add(update_info_btn)

			self.label = toga.Label('', style=Pack(padding=(0), text_align=CENTER))
			main_box.add(self.label)

		def startup(self):
			main_box = toga.Box(style=Pack(direction=COLUMN))

			set_account_tags = toga.Button(
			'Initial Set Up', on_press=self.perm_variables, style=Pack(direction=ROW, padding=5))
			#self.main_window = toga.MainWindow(title=self.formal_name)
			#self.main_window.content = main_box
			#self.main_window.show()
			main_box.add(set_account_tags)


			# Input of Mint cookie and token here
			cookie_label = toga.Label(
				'Cookie: ',
				style=Pack(padding=(0))
			)

			self.cookie_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='Enter cookie here',
				validators=[
					validators.MinLength(1)
					]
				)

			cookie_box = toga.Box(style=Pack(direction=ROW, padding=5))
			cookie_box.add(cookie_label)
			cookie_box.add(self.cookie_input)

			token_label = toga.Label(
				'Token: ',
				style=Pack(padding=(0))
			)
			self.token_input = toga.TextInput(
				style=Pack(flex=1),
				placeholder='Enter token here',
				validators=[
					validators.MinLength(1)
					]
				)

			token_box = toga.Box(style=Pack(direction=ROW, padding=5))
			token_box.add(token_label)
			token_box.add(self.token_input)

			open_file = toga.Button(
				'Choose CSV Statement',
				on_press=self.action_open_file_dialog,
				style=Pack(padding=5)
			)

			import_statement_button = toga.Button(
				'Import',
				on_press=self.import_statement,
				style=Pack(padding=5)
			)

			self.label = toga.Label('Choose a CSV file to import!', style=Pack(padding=(0)))

			main_box.add(set_account_tags)
			main_box.add(cookie_box)
			main_box.add(token_box)
			main_box.add(self.label)
			main_box.add(open_file)
			main_box.add(import_statement_button)

			self.main_window = toga.MainWindow(
				title="Apple Card Mint Importer",
				size=(500, 220),
				resizeable=False,
				minimizable=False)
			self.main_window.content = main_box
			self.main_window.show()




def main():
    return AppleCardtoMintImporter('TextInput')
