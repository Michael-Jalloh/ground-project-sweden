# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask_script import Manager, Server, Command
from app import application
from manager import main_loop

class Main(Command):
	def run(self):
		main_loop()

manager = Manager(application)

# Turn on debugger by defaul and reloader
manager.add_command("runserver", Server(
	use_debugger = True,
	use_reloader = True,
	host = '0.0.0.0')
)
manager.add_command('config', Main())

if __name__ == '__main__':
	manager.run()
