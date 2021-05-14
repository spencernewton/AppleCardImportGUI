"""
Import your CSV Apple Card statements to Mint to properly track transactions!
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import json
from toga import validators
from subprocess import call

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
			cookie = self.cookie_input.value
			print("Cookie is " + cookie)
			token = self.token_input.value
			print("Token is " + token)
			fname = self.csv_name
			print("File is " + fname)

			data = {}
			data['changes'] = []
			data['changes'].append({
				'cookie': self.cookie_input.value,
				'token': self.token_input.value,
				'csv_name': self.csv_name,
			})

			with open('changes.txt', 'w+') as outfile:
				json.dump(data, outfile)
			#call(["python", "import_script.py"])

		def startup(self):
			main_box = toga.Box(style=Pack(direction=COLUMN))

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

			main_box.add(cookie_box)
			main_box.add(token_box)
			main_box.add(self.label)
			main_box.add(open_file)
			main_box.add(import_statement_button)

			self.main_window = toga.MainWindow(title=self.formal_name)
			self.main_window.content = main_box
			self.main_window.show()




def main():
    return AppleCardtoMintImporter('TextInput')
