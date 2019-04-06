import tkinter as tk


main = tk.Tk()
main.title('TifaCrypt')

frame = tk.Frame(main)
frame.pack(side = 'left', expand = 'true', fill = 'both')

rightFrame = tk.Frame(main)
rightFrame.pack(side='right', expand = 'true', fill = 'both')

fileList = tk.Listbox(frame)
fileList.pack(padx = 10, pady = 10, expand = 'true', fill = 'both')

add = tk.Button(rightFrame, text = 'Add', width = 10)
add.pack(padx = 10, pady = 5, expand = 'false', fill = 'both')

remove = tk.Button(rightFrame, text = 'Remove', width = 10)
remove.pack(padx = 10, pady = 5, expand = 'false', fill = 'both')

encrypt = tk.Button(rightFrame, text = 'Encrypt', width = 10)
encrypt.pack(padx = 10, pady = 5, expand = 'false', fill = 'both')

decrypt = tk.Button(rightFrame, text = 'Decrypt', width = 10)
decrypt.pack(padx = 10, pady = 5, expand = 'false', fill = 'both')

main.mainloop()
