import threading
import tkinter as tk

def foo():
	print('Hello, there.')



t1 = threading.Thread(target = foo)
t1.start()
t1.join()


root = tk.Tk()
root.mainloop()
