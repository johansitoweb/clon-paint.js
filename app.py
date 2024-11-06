import tkinter as tk  
from tkinter import colorchooser, filedialog  
from PIL import Image, ImageDraw  


class PaintApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("Clon de Paint.js johansitoweb")  

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')  
        self.canvas.pack()  

        self.button_clear = tk.Button(root, text="Limpiar", command=self.clear_canvas)  
        self.button_color = tk.Button(root, text="Color", command=self.choose_color)  
        self.button_shape_circle = tk.Button(root, text="Círculo", command=self.select_circle)  
        self.button_shape_rectangle = tk.Button(root, text="Rectángulo", command=self.select_rectangle)  
        self.button_shape_square = tk.Button(root, text="Cuadrado", command=self.select_square)  
        self.button_eraser = tk.Button(root, text="Borrador", command=self.use_eraser)  
        self.button_save = tk.Button(root, text="Guardar Imagen", command=self.save_image)  

        self.button_color.pack(side=tk.LEFT)  
        self.button_shape_circle.pack(side=tk.LEFT)  
        self.button_shape_rectangle.pack(side=tk.LEFT)  
        self.button_shape_square.pack(side=tk.LEFT)  
        self.button_eraser.pack(side=tk.LEFT)  
        self.button_clear.pack(side=tk.LEFT)  
        self.button_save.pack(side=tk.RIGHT)  

        self.last_x, self.last_y = None, None  
        self.current_color = "black"  
        self.drawing_shape = None  
        self.shape_start_x = None  
        self.shape_start_y = None  

        self.canvas.bind("<Button-1>", self.press)  
        self.canvas.bind("<B1-Motion>", self.draw)  
        self.canvas.bind("<ButtonRelease-1>", self.release)  

        self.lines = []  # Para almacenar líneas dibujadas  

    def choose_color(self):  
        color = colorchooser.askcolor()[1]  
        if color:  
            self.current_color = color  
            self.drawing_shape = None  # Cuando se selecciona un color, no se dibuja una forma  

    def select_circle(self):  
        self.drawing_shape = "circle"  

    def select_rectangle(self):  
        self.drawing_shape = "rectangle"  

    def select_square(self):  
        self.drawing_shape = "square"  

    def use_eraser(self):  
        self.current_color = "white"  
        self.drawing_shape = None  # Cuando se selecciona el borrador, no se dibuja una forma  

    def clear_canvas(self):  
        self.canvas.delete("all")  
        self.lines = []  # Limpiar la lista de líneas  

    def press(self, event):  
        self.last_x, self.last_y = event.x, event.y  

        if self.drawing_shape in ["rectangle", "square"]:  
            self.shape_start_x = event.x  
            self.shape_start_y = event.y  

    def draw(self, event):  
        if self.last_x is not None and self.last_y is not None:  
            if self.drawing_shape is None:  # Dibujar línea  
                line = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,  
                                                fill=self.current_color, width=2)  
                self.lines.append(line)  
            elif self.drawing_shape == "circle":  
                x0, y0 = self.last_x - 20, self.last_y - 20  
                x1, y1 = self.last_x + 20, self.last_y + 20  
                self.canvas.create_oval(x0, y0, x1, y1, outline=self.current_color)  
            elif self.drawing_shape == "rectangle":  
                if self.shape_start_x is not None and self.shape_start_y is not None:  
                    self.canvas.delete("temp")  
                    self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, event.x, event.y,  
                                                  outline=self.current_color, tags="temp")  
            elif self.drawing_shape == "square":  
                if self.shape_start_x is not None and self.shape_start_y is not None:  
                    side_length = min(abs(event.x - self.shape_start_x), abs(event.y - self.shape_start_y))  
                    self.canvas.delete("temp")  
                    self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y,  
                                                  self.shape_start_x + side_length,  
                                                  self.shape_start_y + side_length,  
                                                  outline=self.current_color, tags="temp")  
        
        self.last_x, self.last_y = event.x, event.y  

    def release(self, event):  
        if self.drawing_shape in ["rectangle", "square"] and self.shape_start_x is not None and self.shape_start_y is not None:  
            if self.drawing_shape == "rectangle":  
                self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y, event.x, event.y,  
                                              outline=self.current_color)  
            elif self.drawing_shape == "square":  
                side_length = min(abs(event.x - self.shape_start_x), abs(event.y - self.shape_start_y))  
                self.canvas.create_rectangle(self.shape_start_x, self.shape_start_y,  
                                              self.shape_start_x + side_length,  
                                              self.shape_start_y + side_length,  
                                              outline=self.current_color)  

        self.shape_start_x = None  
        self.shape_start_y = None  
        self.last_x, self.last_y = None, None  

    def save_image(self):  
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])  
        if file_path:  
            # Crear una imagen de PIL a partir del canvas  
            self.canvas.update()  # Actualiza el canvas  
            x = self.canvas.winfo_rootx()  
            y = self.canvas.winfo_rooty()  
            x1 = x + self.canvas.winfo_width()  
            y1 = y + self.canvas.winfo_height()  
            image = Image.new("RGB", (600, 400), "white")  
            draw = ImageDraw.Draw(image)  

            for item in self.lines:  
                coords = self.canvas.coords(item)  
                draw.line(coords, fill="black", width=2)  

            image.save(file_path)  


if __name__ == "__main__":  
    root = tk.Tk()  
    app = PaintApp(root)  
    root.mainloop()  