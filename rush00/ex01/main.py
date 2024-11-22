#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, filedialog
import checkmate  # Import logic

def change_piece(button):
    """ฟังก์ชันที่ใช้สำหรับเปลี่ยนตัวหมากในช่องที่กด"""
    current_text = button.cget("text")  # อ่านค่าของข้อความจากปุ่ม
    pieces = ["⠀", "♕", "♚", "♖", "♗", "♙"]

    # นับจำนวนตัวหมากบนกระดาน
    board = []
    for row in buttons:
        board_row = []
        for b in row:
            board_row.append(b.cget("text"))
        board.append("".join(board_row))
    
    piece_counts = {piece: sum(row.count(piece) for row in board) for piece in pieces}

 
    max_pieces = {
        "♕": 1,  # King
        "♚": 1,  # Queen 
        "♖": 2,  # Rook
        "♗": 2,  # Bishop
        "♙": 8   # Pawn
    }

    # ค้นหาตัวหมากถัดไปที่สามารถเลือกได้   q   
    next_index = pieces.index(current_text)
    for _ in range(len(pieces)):
        next_index = (next_index + 1) % len(pieces)  # หมุนไปยังตัวหมากถัดไป
        next_piece = pieces[next_index]
        if next_piece == "⠀" or piece_counts.get(next_piece, 0) < max_pieces.get(next_piece, float("inf")):
            button.config(text=next_piece, font=("Arial", 16,))  # เปลี่ยนเป็นตัวหมากใหม่
            return

def check_board():
    """ตรวจสอบสถานะกระดานหมากรุก"""
    try:
        board = []
        for row in buttons:
            board_row = []
            for button in row:
                board_row.append(button.cget("text"))
            board.append("".join(board_row))

        # ตรวจสอบว่ากระดานถูกต้อง
        if not checkmate.validate_board(board):
            messagebox.showerror("Error", "ตารางหมากรุกไม่ถูกต้อง (ต้องเป็นสี่เหลี่ยมจัตุรัส)")
            return

        # ค้นหาและตรวจสอบสถานะ King
        king_position = checkmate.find_king(board)
        king_status = "Checked" if checkmate.is_king_checked(board) else "Safe"
        result_label.config(
            text=f"Result: King is {king_status} at {king_position}", 
            fg="green" if king_status == "Checked" else "red"
        )

    except Exception as e:
        messagebox.showerror("Error", f"เกิดข้อผิดพลาด: {e}")

def clear_board():
    """ล้างกระดาน"""
    for row in buttons:
        for button in row:
            button.config(text="⠀")  # รีเซ็ตตัวหมากกลับเป็น "⠀"

def save_board():
    """บันทึกกระดานลงไฟล์"""
    try:
        # ให้ผู้ใช้เลือกตำแหน่งและชื่อไฟล์
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:  # ถ้าผู้ใช้กดยกเลิก
            return

        # บันทึกสถานะกระดาน
        with open(file_path, "w", encoding="utf-8") as file:  # เพิ่ม encoding="utf-8"
            for row in buttons:
                file.write("".join([button.cget("text") for button in row]) + "\n")

        messagebox.showinfo("Save", "บันทึกกระดานสำเร็จ!")
    except Exception as e:
        messagebox.showerror("Error", f"ไม่สามารถบันทึกกระดานได้: {e}")

def load_board():
    """โหลดกระดานจากไฟล์"""
    try:
        # ให้ผู้ใช้เลือกไฟล์ที่ต้องการโหลด
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:  # ถ้าผู้ใช้กดยกเลิก
            return

        with open(file_path, "r", encoding="utf-8") as file:  # เพิ่ม encoding="utf-8"
            lines = file.readlines()

            # ตรวจสอบว่ามี 8 แถวและแต่ละแถวมี 8 คอลัมน์
            if len(lines) != 8 or any(len(line.strip()) != 8 for line in lines):
                messagebox.showerror("Error", "ไฟล์ที่โหลดไม่ใช่กระดานหมากรุก 8x8 ที่ถูกต้อง!")
                return

            # ล้างกระดานก่อนโหลดข้อมูลใหม่
            clear_board()

            for i, line in enumerate(lines):
                for j, piece in enumerate(line.strip()):
                    buttons[i][j].config(text=piece)

        messagebox.showinfo("Load", "โหลดกระดานสำเร็จ!")
    except FileNotFoundError:
        messagebox.showerror("Error", "ไม่พบไฟล์บันทึกกระดาน!")
    except Exception as e:
        messagebox.showerror("Error", f"ไม่สามารถโหลดกระดานได้: {e}")

def center_window(window, width, height):
    """จัดหน้าต่างให้อยู่ตรงกลางจอ"""
    screen_width = window.winfo_screenwidth()  # ความกว้างของหน้าจอ
    screen_height = window.winfo_screenheight()  # ความสูงของหน้าจอ
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")



root = tk.Tk()
root.title("Checkmate Checker")
root.configure(bg="#2C2C2C")  # พื้นหลังสีเทาเข้ม
center_window(root, 700, 700) 
board_size = 8  # ขนาดกระดาน 8x8
buttons = []

# กรอบกระดาน
board_frame = tk.Frame(root, bg="#2C2C2C")
board_frame.pack(pady=10)   

# สีช่องกระดาน
color1 = "#DCDCDC"  # สีครีมอ่อน
color2 = "#769656"  # สีเขียวหมากรุก

# สร้างตารางหมากรุก
for i in range(board_size):
    row_buttons = []
    for j in range(board_size):
        color = color1 if (i + j) % 2 == 0 else color2
        button = tk.Button(
            board_frame, 
            text="⠀", 
            width=4, 
            height=2, 
            font=("Arial", 16), 
            bg=color, 
            relief="flat", 
            highlightthickness=0
        )
        button.grid(row=i, column=j, padx=2, pady=2)
        button.config(command=lambda b=button: change_piece(b))
        row_buttons.append(button)
    buttons.append(row_buttons)
    


root.configure(bg="#333333") 

# สีกรอบ
button_frame = tk.Frame(root, bg="#333333")
button_frame.pack(pady=10)


button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#444444",      # สีพื้นหลังปุ่ม (เทาเข้ม)
    "fg": "#FFFFFF",      # สีข้อความ (ขาว)
    "activebackground": "#555555",  # สีเมื่อกดปุ่ม
    "activeforeground": "#FFFFFF"   # สีข้อความเมื่อกดปุ่ม
}


check_button = tk.Button(
    button_frame, 
    text="ตรวจสอบ", 
    command=check_board, 
    **button_style, 
    relief="raised", 
    padx=10, 
    pady=5
)
check_button.grid(row=0, column=0, padx=10)


clear_button = tk.Button(
    button_frame, 
    text="ล้างข้อมูล", 
    command=clear_board, 
    **button_style, 
    relief="raised", 
    padx=10, 
    pady=5
)
clear_button.grid(row=0, column=1, padx=10)


save_button = tk.Button(
    button_frame, 
    text="บันทึก", 
    command=save_board, 
    **button_style, 
    relief="raised", 
    padx=10, 
    pady=5
)
save_button.grid(row=0, column=2, padx=10)


load_button = tk.Button(
    button_frame, 
    text="โหลด", 
    command=load_board, 
    **button_style, 
    relief="raised", 
    padx=10, 
    pady=5
)
load_button.grid(row=0, column=3, padx=10)


result_label = tk.Label(root, text="Result: ", font=("Arial", 12), bg="#333333", fg="#FFFFFF")
result_label.pack(pady=10)

root.mainloop()
