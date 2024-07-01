"""
Groups Management System for Console Interfaces
-
Applicazione per la creazione, modifica e creazione di gruppi di lavoro.
Tramite interfaccia a Console.
"""

# Imports

import sys
from os import path, makedirs
from random import randint

from Poison_utils import Console as Cons, Colors as Col

__file__ = "Gmsci.py"

general_directory_name = "pyodide"
ambient_path = path.dirname(path.abspath(__file__))


if not path.basename(ambient_path) == general_directory_name:	# Se il file eseguito non si trova nella cartella giusta:
	Cons.fatal_error(f'''L'eseguibile, o il file eseguito: "{path.basename(__file__)}" dovrebbe trovarsi dentro la cartella: "{general_directory_name}", non "{path.basename(ambient_path)}"''', colored_output=True)


# Configurazione Console
Cons.config()	# Se si desiderano attivare il log e il debug.


# =================================================================================================================== #


# Funzione di pulizia della schermo
def terminal_clear() -> None:

	__terminal__.clear()

# Funzione di pulizia della schermo secondo input
def screen_clear() -> None:

	input(f"\n{Col.bold}{Col.bg.red}|ᐅx{Col.reset} ")
	terminal_clear()


# Funzione d'errore di Input controllato
def controlled_error(error_message: str, bonus_lines: int = 0) -> None:

	print()
	print(error_message)
	input(f"\n{Col.bold}{Col.bg.red}|ᐅx{Col.reset} ")

	Cons.del_lines(6)


# Funzione d'aperture del file
def file_initialization() -> None:

	global register, register_file_path

	register = {}

	register_file_name = "register.txt"
	register_file_path = path.join(ambient_path, register_file_name)

	register = {
	0: {'name': 'Mike', 'surname': 'Bloomfield'},
	1: {'name': 'René', 'surname': 'Descartes'},
	2: {'name': 'Bob', 'surname': 'Dylan'},
	3: {'name': 'Pablo', 'surname': 'Esco al bar'},
	4: {'name': 'Piero', 'surname': 'Guerra'},
	5: {'name': 'Antoine', 'surname': 'Lavoisier'},
	6: {'name': 'Sam', 'surname': 'Lightnin hopkins'}
	}


# Funzione di sovrascrizione del file
def file_overwriting() -> None:
	"""
	Sovrascrizione del registro a file in ordine alfabetico decrescente in base al cognome,
	and then writes the formatted register to a file.

	"""
	global register

	# Riordinamento dell registro in ordine alfabetico decrescente in base al cognome:
	register = dict(sorted(register.items(), key=lambda x: x[1]["surname"]))  # Generato da IA
	register = dict(enumerate(register.values()))  # Generato da IA

	# Scrittura formattata del registro a file:
	with open(register_file_path, "w") as register_file:

		register_file.write("{\n")
		virgin = True

		for key, value in register.items():

			if virgin:	# Per la prima linea nel file di registro
				register_file.write(f"\t{key}: {value}")
				virgin = False
				continue

			register_file.write(f",\n\t{key}: {value}")

		register_file.write("\n}\n")

	Cons.log("Eseguita sovrascrizione del registro a file")


# Funzione di stampa della lista
def register_printing() -> None:

	if register == {}:
		print(f"\n  {Col.bold}{Col.fg.red}Lista vuota.{Col.reset}")
		Cons.log("Registro stampato a terminale (lista vuota)")

	else:
		print(f"\n  {Col.bold}| {Col.fg.blue}Registro{Col.reset}{Col.bold} |{Col.reset}\n")

		for i, a in register.items():
			print(f"  {Col.bold}{Col.fg.dark_grey}", end="")
			print(f"{i + 1}|{Col.reset} {register[i]['name']} {register[i]['surname']}.")

		Cons.log("Registro stampato a terminale")


# Funzione di raccolta dati
def info_input():

	print("\n\t| Registrazione |\n\n")

	name = input("Inserire nome: ").strip().capitalize()
	surname = input("Inserire cognome: ").strip().capitalize()

	while True:
		index = input("Numero di registro: ").strip().capitalize()

		if index.isdigit() and int(index) > 0:
			index = int(index)
			break

		else:
			controlled_error("Inserire un numero valido.")

	duplicates_check = True

	for element in register:	# Per ogni elemento nel registro:
		if register[element]["name"] == name and register[element]["surname"] == surname:	# Se la registrazione immessa corrisponde:
			controlled_error(f"Elemento già registrato in precedenza all'indice {element + 1}.")

			duplicates_check = False
			Cons.log(f'''Tentata registrazione di: "{{"nome: {name}; cognome: {surname}; indice: {index - 1}}}", già presente all'indice: {element + 1}''')

			break

	if duplicates_check is True:
		register[index - 1] = {"name": name, "surname": surname}	#* Registrazione.

		Cons.log(f'''Registrato: "{{"nome: {name}; cognome: {surname}; indice: {index - 1}}}"''')

	terminal_clear()


# Funzione di modifica di una registrazione
def item_edit() -> None:

	register_printing()

	if register == {}:
		screen_clear()

	else:
		print('''\nInserire l'elemento che si desidera modificare:\n (se si desidera uscire inserire: "X")\n''')

		while True:
			z = input("ᐅ  ").strip().capitalize()

			if z.isdigit() and int(z) > 0:
				z = int(z) - 1

				if z in register:
					terminal_clear()

					print()

					print(f"Nome attuale: {register[z]['name']}")
					name = input("Inserire nuovo nome: ").strip().capitalize()

					print()

					print(f"Cognome attuale: {register[z]['surname']}")
					surname = input("Inserire nuovo cognome: ").strip().capitalize()

					for i in register:
						if (register[i]["name"] == name and register[i]["surname"] == surname):
							print(f"Elemento già registrato in precedenza all'indice {i + 1}.\n")
							Cons.log(f'''L'utente ha provato ad effettuare una registrazione gia presente all'indice #{i + 1}: "{register[i]}"''')

						else:
							print("\nModifica registrazione effettuata con successo.")
							register[z] = {"name": name, "surname": surname}	#* Modificazione registrazione.
							Cons.log(f'''Registrazione #{z + 1} aggiornata a: "{register[z]}"''')
							break

					screen_clear()
					break

				else:
					controlled_error(f"Non esiste registrazione di indice {z + 1}.")
					Cons.log(f'''L'utente ha provato a modificare una registrazione di indice inesistente (#{z + 1})''')

			elif z == "X":
				terminal_clear()
				break

			else:
				controlled_error("Inserire un numero valido.")
	terminal_clear()


# Funzione di eliminazione di una registrazione
def item_elimination() -> None:

	print("\nEliminazione di une elemento:")
	register_printing()

	if register == {}:
		screen_clear()

	else:
		print("\nInserire l'indice della registrazione che si desidera eliminare")
		print('se si desidera uscire inserire: "X"\n')

		while True:
			z = input("ᐅ  ").strip().capitalize()

			if z.isdigit() and int(z) > 0:
				z = int(z) - 1

				if z in register:
					terminal_clear()

					if Cons.debug is True:
						Cons.log(f'''Registrazione #{z + 1}: "{register[z]}" eliminata''')
					else:
						print(f'''Registrazione #{z + 1}: "{register[z]}" eliminata.''')

					register.pop(z)	#* Eliminazione dell'elemento dal registro.

					screen_clear()
					break

				else:
					controlled_error(f"Non esiste registrazione di indice {z + 1}.")

			elif z == "X":
				Cons.log("L'utente ha deciso di non eliminare nessuna registrazione")
				terminal_clear()
				break

			else:
				controlled_error("Inserire un numero valido.")


# Funzione di stampa dei gruppi casuali
def groups_printing() -> None:

	global groups_list

	terminal_clear()
	print(f"\n  {Col.bold}| {Col.fg.blue}Gruppi{Col.reset}{Col.bold} |{Col.reset}\n")

	for group in groups_list:
		print(f"  {Col.bold}{Col.fg.blue}", end="")
		print(f"Gruppo {Col.fg.green}{groups_list.index(group) + 1}")
		print(f"{Col.reset}", end="")

		for element in group:
			print(f"  {Col.bold}{Col.fg.dark_grey}", end="")
			print(f"{element + 1}|{Col.reset} {register[element]['name']} {register[element]['surname']}")
		print()

	Cons.log("Gruppi stampati")


# Funzione di creazione di gruppi casuali
def groups_creation() -> None:

	global groups_list
	groups_list = []

	if register == {}:
		register_printing()

	elif len(register) == 1:
		groups_list = [[0]]

	else:
		random_list = []

		while len(random_list) < len(register):
			item = randint(0, len(register.values()) - 1)

			if item not in random_list:
				random_list.append(item)

		while True:
			groups_size = input("Numero di elementi per gruppo: ").strip().capitalize()

			if groups_size.isdigit() and 0 < int(groups_size) < len(register):
				groups_size = int(groups_size)
				break

			else:
				controlled_error("Inserire un numero valido.")

		group_number = len(register) // groups_size	#? Reliquia
		rest = len(register) % groups_size

		if rest != 0:

			while True:
				print(f"""{Col.bold}{Col.fg.blue}
Cosa dovremmo fare del resto?{Col.reset}
{Col.fg.green}{Col.bold}1){Col.reset} Isolarlo nel primo gruppo
{Col.fg.green}{Col.bold}2){Col.reset} Accodarlo all'ultimo gruppo

""")

				menu_2 = input("ᐅ ").strip().capitalize()	#TODO: da migliorare
				terminal_clear()

				if menu_2 == "1" or menu_2 == "2":
					break

				else:
					controlled_error("Opzione non valida")

		while random_list != []:
			group = []

			for i in range(0, groups_size):

				if random_list == []:
					break

				group.append(random_list[0])	#* Inserimento del numero nella lista.
				random_list.pop(0)

				if rest != 0 and menu_2 == "2":
					group.append(random_list[0])
					random_list.pop(0)
					rest = rest - 1

			groups_list.append(group)

		groups_list.reverse()

		Cons.log(f'Creati gruppi: "{groups_list}"')
		groups_printing()	#* Stampa dei gruppi creati.


# Funzione di stampa della pagina del menu
def print_menu_page() -> None:

	print(f"""
  {Col.bold}{Col.fg.blue}Groups Management System for Console Interfaces

                  By Poison_8o8{Col.reset}

  ===============================================

  {Col.bold}{Col.fg.blue}Inserire:{Col.reset}
 
  {Col.fg.green}{Col.bold}1){Col.reset} Per stampare la lista degli elementi registrati.
  {Col.fg.green}{Col.bold}2){Col.reset} Per effettuare una nuova registrazione.
  {Col.fg.green}{Col.bold}3){Col.reset} Per modificare una registrazione.
  {Col.fg.green}{Col.bold}4){Col.reset} Per eliminare una registrazione.
  {Col.fg.green}{Col.bold}5){Col.reset} Per generare dei gruppi casuali.

  {Col.fg.green}{Col.bold}0){Col.reset} Se si vuole arrestare il programma.{Col.reset}

""")

# =================================================================================================================== #

# Funzione principale
def main() -> None:

	terminal_clear()
	file_initialization()

	# Main Loop
	while True:

		print_menu_page()

		menu = input("  ᐅ ")
		menu = menu.strip().capitalize()
		terminal_clear()

		# Arrestare il programma
		if menu == "0":
			Cons.log(f'''Input utente: "{menu}", l'utente ha terminato il programma''')
			break

		# Stampa della lista
		elif menu == "1":
			Cons.log(f'''Input utente: "{menu}" (stampa della lista)''')
			register_printing()
			screen_clear()

		# Aggiungere
		elif menu == "2":
			Cons.log(f'''Input utente: "{menu}" (aggiunta di un elemento alla list lista)''')
			info_input()

		# Modificare
		elif menu == "3":
			Cons.log(f'''Input utente: "{menu}" (modifica di un elemento della list lista)''')
			item_edit()

		# Eliminare
		elif menu == "4":
			Cons.log(f'''Input utente: "{menu}" (eliminazione di un elemento dalla list lista)''')
			item_elimination()

		# Creazione e stampa dei gruppi
		elif menu == "5":
			Cons.log(f'''Input utente: "{menu}" (creazione di gruppi casuali)''')
			groups_creation()
			screen_clear()

		else:
			print("Opzione non valida.")
			Cons.log(f'''Input utente: "{menu}", (opzione non valida)''')
			screen_clear()

		file_overwriting()

# =================================================================================================================== #

if __name__ == "__main__":
	Cons.log("Programma avviato")
	main()

else:
	Cons.log("Programma non avviato come principale", show_to_console = True)
	screen_clear()

# -Poison_8o8
