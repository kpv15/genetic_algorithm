import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox


class GUI:
    current_row = 0

    def __init__(self, program, selection_methods_names, mutation_methods_names, crossing_methods_names):
        self.program = program
        self.window = tk.Tk()
        self.window.title("Genetic")

        self.lb_min_val = self.__new_label("minimal value:")
        self.entry_min_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_min_val, self.entry_min_val)

        self.lb_max_val = self.__new_label("maximal value:")
        self.entry_max_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_max_val, self.entry_max_val)

        self.lb_dx_val = self.__new_label("dx value:")
        self.entry_dx_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_dx_val, self.entry_dx_val)

        self.lb_population_size = self.__new_label("population size:")
        self.entry_population_size = self.__new_entry(self.__validate_entry_int)
        self.__add_row(self.lb_population_size, self.entry_population_size)

        self.lb_generations_number = self.__new_label("generations number:")
        self.entry_generations_number = self.__new_entry(self.__validate_entry_int)
        self.__add_row(self.lb_generations_number, self.entry_generations_number)

        self.lb_elite_strategy_val = self.__new_label("elite strategy %:")
        self.entry_elite_strategy_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_elite_strategy_val, self.entry_elite_strategy_val)

        self.lb_inversion_operator_val = self.__new_label("inversion probability %:")
        self.entry_inversion_operator_probability = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_inversion_operator_val, self.entry_inversion_operator_probability)

        self.lb_crossing_probability_val = self.__new_label("crossing probability %:")
        self.entry_crossing_probability_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_crossing_probability_val, self.entry_crossing_probability_val)

        self.lb_mutation_probability_val = self.__new_label("mutation probability %:")
        self.entry_mutation_probability_val = self.__new_entry(self.__validate_entry_float)
        self.__add_row(self.lb_mutation_probability_val, self.entry_mutation_probability_val)

        self.lb_selection_method = self.__new_label("selection method:")
        self.selected_selection_method_name = tk.StringVar(self.window)
        self.combobox_selection_method = self.__new_combobox(selection_methods_names,
                                                             self.selected_selection_method_name)
        self.combobox_selection_method.current(0)
        self.__add_row(self.lb_selection_method, self.combobox_selection_method)
        self.combobox_selection_method.bind("<<ComboboxSelected>>", self.show_tournament_box)

        self.lb_tournament_size = self.__new_label("tournament size:")
        self.entry_tournament_size = self.__new_entry(self.__validate_entry_int)
        self.__add_row(self.lb_tournament_size, self.entry_tournament_size)
        self.show_tournament_box()

        self.lb_mutation_method = self.__new_label("mutation method:")
        self.selected_mutation_method_name = tk.StringVar(self.window)
        self.combobox_mutation_method = self.__new_combobox(mutation_methods_names, self.selected_mutation_method_name)
        self.combobox_mutation_method.current(0)
        self.__add_row(self.lb_mutation_method, self.combobox_mutation_method)

        self.lb_crossing_method = self.__new_label("crossing method:")
        self.lb_crossing_method.grid(row=9, column=0)
        self.selected_crossing_method_name = tk.StringVar(self.window)
        self.combobox_crossing_method = self.__new_combobox(crossing_methods_names, self.selected_crossing_method_name)
        self.combobox_crossing_method.current(0)
        self.__add_row(self.lb_crossing_method, self.combobox_crossing_method)

        self.start_button = tk.Button(text="Start", command=self.__call_start)
        self.start_button.grid(row=self.current_row, columnspan=self.current_row)
        self.current_row += 1

    def show_tournament_box(self, *args):
        if self.selected_selection_method_name.get() == "Tournament Selection":
            self.entry_tournament_size.config(state='normal')
        else:
            self.entry_tournament_size.config(state='disabled')


    def __call_start(self):
        try:
            min_val = float(self.entry_min_val.get())
        except:
            messagebox.showerror('error', "incorrect min val")
            return

        try:
            max_val = float(self.entry_max_val.get())
        except:
            messagebox.showerror('error', "incorrect max val")
            return

        try:
            dx_val = float(self.entry_dx_val.get())
        except:
            messagebox.showerror('error', "incorrect dx val")
            return

        try:
            population_size = int(self.entry_population_size.get())
        except:
            messagebox.showerror('error', "incorrect population size")
            return

        try:
            generations_number = int(self.entry_generations_number.get())
        except:
            messagebox.showerror('error', "incorrect generation number")
            return

        try:
            elite_strategy_val = float(self.entry_elite_strategy_val.get()) / 100
        except:
            messagebox.showerror('error', "incorrect elite strategy val")
            return

        try:
            inversion_operator_probability = float(self.entry_inversion_operator_probability.get()) / 100
        except:
            messagebox.showerror('error', "incorrect inversion operator probability")
            return

        try:
            crossing_probability = float(self.entry_crossing_probability_val.get()) / 100
        except:
            messagebox.showerror('error', "incorrect crossing probability")
            return

        try:
            mutation_probability = float(self.entry_mutation_probability_val.get()) / 100
        except:
            messagebox.showerror('error', "incorrect mutation probability")
            return

        try:
            if self.selected_selection_method_name.get() == "Tournament Selection":
                tournament_size = int(self.entry_tournament_size.get())
            else:
                tournament_size = 0
        except:
            messagebox.showerror('error', "incorrect tournament size")
            return

        self.program.start_work(
            min_val,
            max_val,
            dx_val,
            population_size,
            generations_number,
            elite_strategy_val,
            inversion_operator_probability,
            crossing_probability,
            mutation_probability,
            self.selected_selection_method_name.get(),
            tournament_size,
            self.selected_mutation_method_name.get(),
            self.selected_crossing_method_name.get(),
        )

    def __add_row(self, label, input_item):
        label.grid(row=self.current_row, column=0)
        input_item.grid(row=self.current_row, column=1)
        self.current_row += 1

    def __new_entry(self, validator):
        return tk.Entry(self.window, justify=tk.RIGHT, validate='all',
                        validatecommand=(self.window.register(validator), "%P"))

    @staticmethod
    def __validate_entry_float(val):
        try:
            float(val)
        except ValueError:
            if val != "" and val != "-":
                return False
        return True

    @staticmethod
    def __validate_entry_int(val):
        try:
            int(val)
        except ValueError:
            if val != "" and val != "-":
                return False
        return True

    def __new_label(self, text):
        return tk.Label(self.window, text=text)

    def __new_combobox(self, values, string_var):
        return tkk.Combobox(self.window, textvariable=string_var, values=values, state='readonly')

    def show(self):
        self.window.mainloop()


if __name__ == "__main__":
    window = GUI(1, ["roulette selection", "one", "two"], ["one", "two"], ["one", "two"])
    window.show()
