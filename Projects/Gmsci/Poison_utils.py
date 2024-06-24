"""
Poison's Utilities
-
Modulo con varie funzionalità creato da Poison_8o8.
"""


import os, sys

from random import randint

from datetime import datetime

# =================================================================================================================== #

class Colors:
	"Funzionalità per la stampa colorata."

	reset = "\033[0m"
	bold = "\033[01m"
	disable = "\033[02m"
	underline = "\033[04m"
	blink = "\033[05m"
	reverse = "\033[07m"
	strike_through = "\033[09m"
	invisible = "\033[08m"

	class fg:
		white = "\033[50m"
		black = "\033[30m"
		red = "\033[31m"
		green = "\033[32m"
		orange = "\033[33m"
		blue = "\033[34m"
		purple = "\033[35m"
		cyan = "\033[36m"
		light_grey = "\033[37m"
		dark_grey = "\033[90m"
		light_red = "\033[91m"
		light_green = "\033[92m"
		yellow = "\033[93m"
		light_blue = "\033[94m"
		pink = "\033[95m"
		light_cyan = "\033[96m"

	class bg:
		black = "\033[40m"
		red = "\033[41m"
		green = "\033[42m"
		orange = "\033[43m"
		blue = "\033[44m"
		purple = "\033[45m"
		cyan = "\033[46m"
		light_grey = "\033[47m"

# =================================================================================================================== #

class Console:
	"Funzionalità per facilitare l'interazione con il terminale."

	debug = None
	logs = None
	logs_file_path = None
	screen_cleaning_method = None
	colored_output = None
	logs_file_path = None


	def error(error_message: str, *, show_to_console: bool = False, colored_output: bool = False, time_stamp: bool = True) -> None:
		'''Metodo per la presentazione degli errori non fatali.
		Per presentare errori fatali usare: "Console.fatal_error()".'''

		colored_output = Console.colored_output	# Sovrascrizione della variabile locale con la variabile della classe.
		time_stamp_value = datetime.now().strftime("%H:%M:%S")	# Time stamp per i log.

		if Console.logs is True :
			with open(Console.logs_file_path, "a") as logs_file:
				logs_file.write(f"\t[{time_stamp_value}] - Errore: {error_message}.\n")

		if Console.debug is True or show_to_console is True:
			if Console.colored_output is True or colored_output is True:
				if time_stamp is True:
					print(f"\n{Colors.bold}{Colors.bg.orange}  >{Colors.reset} {Colors.fg.green}[{time_stamp_value}] - {error_message}.{Colors.reset}\n")

				else:
					print(f"\n{Colors.bold}{Colors.bg.orange}  >{Colors.reset} {Colors.fg.green}{error_message}.{Colors.reset}\n")

			else:	# Se la stampa colorato non è attiva:
				if time_stamp is True:
					print(f"\n  > [{time_stamp_value}] - {error_message}.\n")

				else:
					print(f"\n  > {error_message}.\n")


	def fatal_error(error_message: str, *, colored_output: bool = False) -> None:
		time_stamp_value = datetime.now().strftime("%H:%M:%S")	# Time stamp per i log.
		if Console.logs is True :
			with open(Console.logs_file_path, "a") as logs_file:
				logs_file.write(f"\t[{time_stamp_value}] - FATAL ERROR: {error_message}.\n")

		if Console.colored_output is True or colored_output is True:	# Se l'output colorato è stato abilitato in generale o per questo errore:
			raise Exception(f"{Colors.underline}{Colors.fg.red}{error_message}{Colors.reset}{Colors.fg.red}.{Colors.reset}\n")	#* Lancio dell errore.

		else:
			raise Exception(f"{error_message}.\n")


	def config(*, debug: bool = False,  logs: bool = False, logs_file_path: str = "", screen_cleaning_method: str = "auto", colored_output: bool = True) -> None:
		"""Metodo di configurazione della funzionalità Console.

		- È possibile attivare il debug: "Console.config(debug=True)".
		- È possibile attivare i logs: "Console.config(logs=True)".
		- È possibile specificare il percorso presso il quale si desidera venga creata la cartella contenente i file edi log: "Console.config(logs_file_path="*")".
		- È possibile specificare il metodo di pulizia dello schermo compatibile con la console: "Console.config(screen_cleaning_method="*")", (sono disponibili "auto", "cls" e "clear").
		- È possibile attivare l'output colorato: "Console.config(colored_output=True)"."""

		if screen_cleaning_method in ("auto", "cls", "clear"):	# Se il metodo di pulizia dello schermo è fra i supportati:
			Console.screen_cleaning_method = screen_cleaning_method

		else:	# Se il metodo di pulizia dello schermo non è fra i supportati:
			Console.fatal_error(f"""Errore durante l'esecuzione del metodo: "Console.config()":
Sono supportati solo i parametri "auto", "cls" e "clear", non "{screen_cleaning_method}" inserito dall'utente""")

		if logs is True:
			initial_time_stamp = datetime.now().strftime("%d/%m/%Y - %H:%M")

			logs_directory_name = "logs"
			logs_file_name = "logs.txt"

			if logs_file_path == None:	# Se il metodo "Console.config()" non è stato eseguito:
				Console.fatal_error('Mancata esecuzione del metodo: "Console.config(logs_file_path=...)"')

			if logs_file_path == "":	# Se il percorso file dei log non è stato impostato:
				Console.fatal_error('Specificare il percorso del file di log presso il metodo: "Console.config(logs_file_path=...)"')

			if not os.path.exists(logs_file_path):	# Se il percorso file dei log non esiste:
				Console.fatal_error(f'''Il percorso: "{logs_file_path}" non esiste, specificarne un altro a: "Console.config(logs_file_path=...)''')

			if not os.path.exists(os.path.join(logs_file_path, logs_directory_name)):	# Se la cartella dei logs non esiste:
					os.makedirs(os.path.join(logs_file_path, logs_directory_name))	#* Crea la cartella dei logs.

			logs_file_path = os.path.join(logs_file_path, logs_directory_name, logs_file_name)

			time_header = f'''\n< ==== | {initial_time_stamp} | ==== >\nEsecuzione del file: "{os.path.realpath(__file__)}".\n\n'''	#TODO: Se esiste un metodo mostrare il file principale, non la libreria.

			if not os.path.exists(logs_file_path):	# Se il file di log non esiste:
				time_stamp_value = datetime.now().strftime("%H:%M:%S")
				time_header = time_header + f'''\t[{time_stamp_value}] - File dei logs creato.\n'''

			with open(logs_file_path, "a") as logs_file:	#* Creazione del file dei log.
				logs_file.write(time_header)	#* Scrittura dell'intestazione temporale nel file dei log.

			Console.logs_file_path = logs_file_path


		Console.debug = debug
		Console.logs = logs
		Console.colored_output = colored_output


	def clear() -> None:
		"Metodo per la pulizia del terminale."

		if Console.screen_cleaning_method == None:
			Console.fatal_error('Specificare il metodo di pulizia della schermo presso il metodo: "Console.config(screen_cleaning_method=...)"')

		elif Console.screen_cleaning_method == "auto":
			if os.name == 'posix':
				os.system('clear')	# Metodo di pulizia per sistemi Unix/Linux/macOS.

			elif os.name == 'nt':
				os.system('cls')	# Metodo di pulizia per sistemi Windows.

		elif Console.screen_cleaning_method == "clear":
			os.system("clear")

		elif Console.screen_cleaning_method == "cls":
			os.system("cls")

		else:
			Console.fatal_error(f'Errore: Il parametro: "{Console.screen_cleaning_method}" impostato in: "Console.config(screen_cleaning_method=...)" non è supportato')


	def log(console_message: str, *, show_to_console: bool = False, time_stamp: bool = False) -> None:
		"""Funzionalità per la stampa di informazioni utili a terminale a fini di debug, abilitatile con "Console.config(debug=True)".

		Il parametro "show_to_console" sovrascriverà la configurazione solo per l'istanza dove la sua funzione è stata chiamata."""

		time_stamp_value = datetime.now().strftime("%H:%M:%S")

		if Console.debug == None:
			Console.fatal_error('Mancata esecuzione del metodo: "Console.config()"')

		elif Console.debug is True or show_to_console is True:

			if Console.colored_output is True:

				if time_stamp is True:
					print(f"\n{Colors.bold}{Colors.bg.orange}  >{Colors.reset} {Colors.fg.green}[{time_stamp_value}] - {console_message}.{Colors.reset}\n")	#* Stampa colorata con intestazione temporale.

				else:
					print(f"\n{Colors.bold}{Colors.bg.orange}  >{Colors.reset} {Colors.fg.green}{console_message}.{Colors.reset}\n")

			else:

				if time_stamp is True:
					print(f"\n  > [{time_stamp_value}] - {console_message}.\n")

				else:
					print(f"\n  > {console_message}.\n")

			input("> ")
			Console.clear()

		if Console.logs is True:

			with open(Console.logs_file_path, "a") as logs_file:
				logs_file.write(f"\t[{time_stamp_value}] - {console_message}.\n")

		elif Console.logs == None:
			Console.fatal_error('Mancata esecuzione del metodo: "Console.config()"')


	def stop() -> None:
		'''Funzionalità per arrestare il programma'''
		Console.log("Il programma è stato terminato tramite istruzione")
		sys.exit()


	def del_lines(lines_number: int = 2) -> None:
		"Eliminazione di un numero dato di linee dal terminale."

		if lines_number < 1:
			Console.fatal_error(f'Il minimo di line eliminabili è 1, non "{lines_number}"')

		for i in range(lines_number):
			sys.stdout.write("\033[F")
			sys.stdout.write("\033[K")
			sys.stdout.flush()


	def function_timer(_function: callable) -> None:
		"Funzionalità per la misurazione del tempo di esecuzione di una funzione."

		def wrapper(*args, **kwargs):
			start_time = datetime.now()

			function_results = _function(*args, **kwargs)

			end_time = datetime.now()

			execution_time = end_time - start_time

			Console.log(f'La funzione "{_function.__name__}({_function(*args, **kwargs)})" ha impiegato {execution_time:.6f} secondi per eseguire')

			return function_results
		return wrapper


# =================================================================================================================== #


"""
Ain't it hard to stumble
and land in the wrong side of the lagoon,
ain't it hard to stumble
and hope that death didn't get you so soon.

- Poison_8o8
"""
