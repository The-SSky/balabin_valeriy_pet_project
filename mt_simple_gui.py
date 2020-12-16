import sys
import subprocess
import tkinter as tk
from tkinter import filedialog
from myclasses.text_widget_modified import *


class Gui_app():
    def __init__(self, master=None):
        self.master = master
        self.master.geometry('640x480')
        self.master.title('mimetex Simple Gui')

        self.path_to_mimetex = sys.argv[0][:sys.argv[0].rfind(
            '\\')] + '\mimetex\\'
        self.font = '6'

        self.main_frame = FrameTable(self.master)

        self.input_wd = TextE(self.main_frame.input_row_frame, outer=self.auto_refresh,
                              undo=True, autoseparators=True, maxundo=-1, font=("Helvetica", 14))
        self.input_wd.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.output_label = tk.Label(self.main_frame.output_row_frame, text='')
        self.output_label.pack(anchor=tk.NW, expand=tk.YES, padx=20)

        self.save_image_button = tk.Button(self.main_frame.buttons_row_frame, text='Save Equation',
                                           command=self.save_file)
        self.save_image_button.pack(side=tk.RIGHT, padx=20)

        self.font_label = tk.Label(self.main_frame.buttons_row_frame, text='Font',
                                   font=("Helvetica", 12))
        self.font_label.pack(side=tk.LEFT)
        self.font_entry = EntryM(
            self.main_frame.buttons_row_frame, width=5, justify='right')
        self.font_entry.text = '6'
        self.font_entry.pack(side=tk.LEFT, padx=5)

        self.blank_frame = tk.Frame(
            self.main_frame.buttons_row_frame, width=100)
        self.blank_frame.pack(side=tk.LEFT)
        self.edit_tex_button = tk.Button(
            self.main_frame.buttons_row_frame, text='Open tex file', command=self.open_notepad)
        self.edit_tex_button.pack(side=tk.LEFT, padx=5)

        self.create_image_button = tk.Button(self.main_frame.buttons_row_frame, 
            text='Create Image from tex file', command=self.convert_text_file_to_img)
        self.create_image_button.pack(side=tk.LEFT, padx=5)
        self.input_wd.focus_set()
        self.auto_refresh()

    # if result.gif is empty, blank.gif is used instead
    def refresh_output_label(self):
        try:
            img = tk.PhotoImage(file=f'{self.path_to_mimetex}result.gif')
        except:
            img = tk.PhotoImage(file=f'{self.path_to_mimetex}blank.gif')
        if img:
            self.output_label.config(image=img)
            self.output_label.image = img

    # /mimetex/result.gif
    def refresh_result_gif(self):
        equation_path = f'{self.path_to_mimetex}equation.tex'
        result_path = f'{self.path_to_mimetex}result.gif'
        with open(result_path, 'wb') as w:
            equation_text = str(self.input_wd.get('1.0', 'end-1c'))
            path_args = f'{self.path_to_mimetex}mimetex.exe -d "{equation_text}" -s {self.font}'
            subprocess.call(path_args, stdout=w, shell=False)

    def auto_refresh(self):
        self.font = self.font_entry.text
        self.refresh_result_gif()
        self.refresh_output_label()

    def open_notepad(self):
        subprocess.Popen(
            ['notepad.exe', f'{self.path_to_mimetex}equation.tex'])

    # converts 'mimetex/equation.tex'
    def convert_text_file_to_img(self):
        equation_path = f'{self.path_to_mimetex}equation.tex'
        result_path = f'{self.path_to_mimetex}result.gif'
        self.font = self.font_entry.text
        with open(result_path, 'wb') as w:
            path_args = f'{self.path_to_mimetex}mimetex.exe ' \
                + f'-f {self.path_to_mimetex}equation.tex > result.gif -s {self.font}'
            print(path_args)
            subprocess.call(path_args, stdout=w, shell=False, timeout=None)
        self.refresh_output_label()

    def save_file(self):
        f = filedialog.asksaveasfile(mode='wb', initialfile="equation.gif",
                                     title="Save Equation", filetypes=(("gif image", "*.gif"),))
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        with open(f'{self.path_to_mimetex}result.gif', 'rb') as r:
            f.write(r.read())
        f.close()


class FrameTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        self.input_row_frame = tk.Frame(self, height=180)
        self.input_row_frame.propagate(0)
        self.input_row_frame.pack(fill='x', side=tk.TOP, pady=5)

        self.output_row_frame = tk.Frame(self)
        self.output_row_frame.pack(
            fill=tk.BOTH, side=tk.TOP, expand=tk.YES, pady=5)

        self.buttons_row_frame = tk.Frame(self, height=30)
        self.buttons_row_frame.propagate(0)
        self.buttons_row_frame.pack(fill='x', side=tk.BOTTOM, pady=5)


class EntryM(tk.Entry):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.master = master

    @property
    def text(self):
        return self.get()

    @text.setter
    def text(self, val):
        self.delete(0, tk.END)
        self.insert(0, val)


def main():
    root = tk.Tk()
    main_window = Gui_app(root)
    root.mainloop()


if __name__ == "__main__":
    main()
