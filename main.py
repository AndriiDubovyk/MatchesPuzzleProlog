import tkinter as tk
import time
from PIL import Image,ImageTk # pip install Pillow

from Expression import Expression
from Symbol import FREE_SPACE as s_fs
from Match import MATCH_LENGTH as m_l
from Expression import FREE_SPACE as e_fs
from pyswip import Prolog

GAME_NAME = "Matches Puzzle"

# matches_puzzle_random(-N1In, -OpIn, -N2In, -N3In, -N1Out, -OpOut, -N2Out, -N3Out)
prolog_query = "matches_puzzle_random(N1In, OpIn, N2In, N3In, N1Out, OpOut, N2Out, N3Out)"

frame_time = 0.033
show_time = 1.0
win = None
new_puzzle_btn = show_answer_btn = quit_btn = canvas = None
exp_in_str = exp_out_str = None, None
exp_in = None
bg_img_src = (Image.open("copybook_bg.png"))

# calculate size to place expression in the centre of the canvas
exp_width = m_l * 5 + s_fs * 10 + e_fs * 4
exp_height = m_l * 3 + s_fs * 4

# generete new puzzle and show it
def generate_new_puzzle():
    global canvas, exp_in, exp_in_str, exp_out_str
    clear_canvas()
    is_solution_found = False
    n1_in = n2_in = n3_in = op_in = None
    n1_out = n2_out = n3_out = op_out = None
    while not is_solution_found:
        res = prolog.query(prolog_query)
        for sol in res:
            if not is_solution_found:
                is_solution_found = True
                n1_in, n1_out = sol["N1In"], sol["N1Out"]
                n2_in, n2_out = sol["N2In"], sol["N2Out"]
                n3_in, n3_out = sol["N3In"], sol["N3Out"]
                op_in, op_out = sol["OpIn"], sol["OpOut"]
    exp_in_str = f"{n1_in}{op_in}{n2_in}={n3_in}" # get start puzzle expression
    exp_out_str = f"{n1_out}{op_out}{n2_out}={n3_out}" # get end puzzle expression
    exp_in = Expression(canvas, exp_x(), exp_y(), exp_in_str)
    create_show_answer_btn()

# clear expression on canvas
def clear_canvas():
   global bg_img, canvas
   canvas.delete("all")
   canvas.create_image(0, 0, image = bg_img, anchor = "nw")

# show puzzle answer
def show_answer():
    global canvas, show_answer_btn, win, exp_in, exp_out_str
    exp_in.set_target_exp(exp_out_str)
    is_show_case_over = False
    while not exp_in.is_in_target:
        exp_in.move_to_target()
        win.update()
        if exp_in.is_in_showcase and not is_show_case_over:
            time.sleep(show_time)
            is_show_case_over = True
        else:
            time.sleep(frame_time)
    destroy_show_answer_btn()

# get x-coordinate to place expression at the center of the canvas
def exp_x():
    global win, exp_with
    return (win.winfo_screenwidth() - exp_width) / 2 

# get y-coordinate to place expression at the center of the canvas
def exp_y():
    global win, exp_height
    return (win.winfo_screenheight() - exp_height) / 2 

# destoy "Show Answer" btn
def destroy_show_answer_btn():
    global show_answer_btn
    show_answer_btn.destroy()
    show_answer_btn = None

# add canvas with puzzlet to window
def create_canvas():
    global bg_img, canvas
    bg_img = bg_img_src.resize((win.winfo_screenwidth(), win.winfo_screenheight()), Image.ANTIALIAS)
    bg_img = ImageTk.PhotoImage(bg_img)
    canvas = tk.Canvas(win, width = win.winfo_screenwidth(), height=win.winfo_screenheight())
    canvas.pack(fill = "both", expand = True)
    canvas.create_image(0, 0, image = bg_img, anchor = "nw")
    
# add "New Puzzle" btn to window
def create_new_puzzle_btn():
    global new_puzzle_btn
    new_puzzle_btn = tk.Button(win, text="New Puzzle", bg="#42f569", command=generate_new_puzzle, padx=15, pady=10)
    new_puzzle_btn.place(relx=0.3, rely=0.9, anchor=tk.CENTER)

# add "Show Answer" btn to window
def create_show_answer_btn():
    global show_answer_btn
    if show_answer_btn == None: # don't create multiple buttons   
        show_answer_btn = tk.Button(win, text="Show Answer", bg="#42c5f5", command=show_answer, padx=15, pady=10)
        show_answer_btn.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# add "Quit" btn to window
def create_quit_btn():
    global quit_btn
    quit_btn = tk.Button(win, text="Quit", bg="#e6535a", command=quit, padx=15, pady=10)
    quit_btn.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

# close game
def quit():
    global win
    win.quit()
    
if __name__ == "__main__":
    # load prolog file with game logic
    prolog = Prolog()
    prolog.consult("matches_game_logic.pl")

    # create window with canvas and buttons
    win = tk.Tk()
    win.attributes('-fullscreen', True)
    win.title(GAME_NAME)
    
    create_canvas()
    create_new_puzzle_btn()
    create_show_answer_btn()
    create_quit_btn()
      
    # generate new puzzle and place it on canvas
    generate_new_puzzle()

    win.mainloop()
