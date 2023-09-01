import tkinter as tk
from tkinter import ttk
import json


class PhoneBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонный справочник")

        self.contacts = []

        self.create_widgets()

    def create_widgets(self):
        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.add_button = ttk.Button(self.buttons_frame, text="Добавить", command=self.add_contact)
        self.delete_button = ttk.Button(self.buttons_frame, text="Удалить", command=self.delete_contact)

        self.add_button.pack(fill=tk.X)
        self.delete_button.pack(fill=tk.X)

        self.contacts_frame = ttk.Frame(self.root)
        self.contacts_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.search_entry = ttk.Entry(self.contacts_frame, width=20)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = ttk.Button(self.contacts_frame, text="Поиск", command=self.search_contacts)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.contacts_listbox = tk.Listbox(self.contacts_frame, selectmode=tk.SINGLE)
        self.contacts_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        scrollbar = tk.Scrollbar(self.contacts_frame, orient=tk.VERTICAL, command=self.contacts_listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.contacts_listbox.config(yscrollcommand=scrollbar.set)

        self.load_contacts()
        self.update_contacts_list()

    def add_contact(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить контакт")

        label_surname = ttk.Label(add_window, text="Фамилия:")
        label_name = ttk.Label(add_window, text="Имя:")
        label_patronymic = ttk.Label(add_window, text="Отчество:")
        label_birthday = ttk.Label(add_window, text="Дата рождения:")
        label_personal_phone = ttk.Label(add_window, text="Телефон (личный):")
        label_home_phone = ttk.Label(add_window, text="Телефон (домашний):")
        label_work_phone = ttk.Label(add_window, text="Телефон (рабочий):")

        self.entry_surname = ttk.Entry(add_window)
        self.entry_name = ttk.Entry(add_window)
        self.entry_patronymic = ttk.Entry(add_window)
        self.entry_birthday = ttk.Entry(add_window)
        self.entry_personal_phone = ttk.Entry(add_window)
        self.entry_home_phone = ttk.Entry(add_window)
        self.entry_work_phone = ttk.Entry(add_window)

        label_surname.grid(row=0, column=0, sticky="w")
        label_name.grid(row=1, column=0, sticky="w")
        label_patronymic.grid(row=2, column=0, sticky="w")
        label_birthday.grid(row=3, column=0, sticky="w")
        label_personal_phone.grid(row=4, column=0, sticky="w")
        label_home_phone.grid(row=5, column=0, sticky="w")
        label_work_phone.grid(row=6, column=0, sticky="w")

        self.entry_surname.grid(row=0, column=1)
        self.entry_name.grid(row=1, column=1)
        self.entry_patronymic.grid(row=2, column=1)
        self.entry_birthday.grid(row=3, column=1)
        self.entry_personal_phone.grid(row=4, column=1)
        self.entry_home_phone.grid(row=5, column=1)
        self.entry_work_phone.grid(row=6, column=1)

        save_button = ttk.Button(add_window, text="Сохранить", command=self.save_contact)
        save_button.grid(row=7, columnspan=2)

    def save_contact(self):
        surname = self.entry_surname.get()
        name = self.entry_name.get()
        patronymic = self.entry_patronymic.get()
        birthday = self.entry_birthday.get()
        personal_phone = self.entry_personal_phone.get()
        home_phone = self.entry_home_phone.get()
        work_phone = self.entry_work_phone.get()

        contact = {
            "Фамилия": surname,
            "Имя": name,
            "Отчество": patronymic,
            "Дата рождения": birthday,
            "Телефон (личный)": personal_phone,
            "Телефон (домашний)": home_phone,
            "Телефон (рабочий)": work_phone
        }

        self.contacts.append(contact)
        self.update_contacts_list()

        self.save_contacts()

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.contacts[index]
            self.update_contacts_list()
            self.save_contacts()

    def update_contacts_list(self):
        self.contacts_listbox.delete(0, tk.END)
        sorted_contacts = sorted(self.contacts, key=lambda x: x.get("Фамилия", ""))
        for contact in sorted_contacts:
            surname = contact.get("Фамилия", "")
            name = contact.get("Имя", "")
            patronymic = contact.get("Отчество", "")
            display_name = surname
            if name:
                display_name += f", {name}"
            if patronymic:
                display_name += f", {patronymic}"
            self.contacts_listbox.insert(tk.END, display_name)

    def save_contacts(self):
        with open("contacts.json", "w", encoding="utf-8") as file:
            json.dump(self.contacts, file, ensure_ascii=False, indent=4)

    def load_contacts(self):
        try:
            with open("contacts.json", "r", encoding="utf-8") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            self.contacts = []

    def search_contacts(self):
        search_text = self.search_entry.get().lower()
        self.contacts_listbox.delete(0, tk.END)
        matching_contacts = [contact for contact in self.contacts if
                             any(value.lower().find(search_text) != -1 for value in contact.values())]
        for contact in matching_contacts:
            surname = contact.get("Фамилия", "")
            name = contact.get("Имя", "")
            patronymic = contact.get("Отчество", "")
            display_name = surname
            if name:
                display_name += f", {name}"
            if patronymic:
                display_name += f", {patronymic}"
            self.contacts_listbox.insert(tk.END, display_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneBook(root)
    root.mainloop()
