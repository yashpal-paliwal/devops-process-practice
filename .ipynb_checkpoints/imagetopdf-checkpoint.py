import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import img2pdf
import os
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=4)

        self.image_path_entry = self.create_entry(row=0, column=0)
        self.select_image_button = self.create_button(text="Select Image", command=self.select_image, row=0, column=1)

        self.output_path_entry = self.create_entry(row=1, column=0)
        self.select_output_button = self.create_button(text="Output Location", command=self.select_output, row=1, column=1)

        self.convert_button = self.create_button(text="Convert to PDF", command=self.convert_to_pdf, row=2, column=0, columnspan=2)

    def create_entry(self, row, column):
        entry = tk.Entry(self, highlightbackground='black', highlightthickness=1, width=100)
        entry.grid(row=row, column=column, sticky="ew")
        return entry

    def create_button(self, text, command, row, column, columnspan=1):
        button = tk.Button(self, text=text, command=command, highlightbackground='black', highlightthickness=1)
        button.grid(row=row, column=column, columnspan=columnspan, sticky="ew")
        return button

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp *.tiff")])
        if self.image_path:
            if not self.image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                messagebox.showinfo("Attention", "Please select an image only!")
                self.image_path = ""
            else:
                self.image_path_entry.delete(0, tk.END)
                self.image_path_entry.insert(0, self.image_path)

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(0, self.output_dir)

    def convert_to_pdf(self):
        if hasattr(self, 'image_path') and hasattr(self, 'output_dir') and self.image_path and self.output_dir:
            image = Image.open(self.image_path)
            pdf_bytes = img2pdf.convert(image.filename)
            output_path = os.path.join(self.output_dir, os.path.splitext(os.path.basename(self.image_path))[0] + '.pdf')
            with open(output_path, "wb") as file:
                file.write(pdf_bytes)
            image.close()
            messagebox.showinfo("Success", "Image converted to PDF successfully!")
root = tk.Tk()
root.title('Image to PDF')
# Set the size of the window
window_width = 720
window_height = 100
root.geometry(f'{window_width}x{window_height}')
root.resizable(0, 0)  # This will disable the maximize button
app = Application(master=root)
app.mainloop()