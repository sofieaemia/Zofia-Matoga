from psychopy import visual, event, core, gui
import os

def user_data(): # zbieranie danych osoby badanej - okno dialogowe nie działa za dobrze, w sensie wpływa na rozmiar gry później, nie udało nam się znależć rozwiązania problemu, więc dla wygodniejszej gry polecamy zakomentować ten fragment programu 
    data = dict()
    data['płeć'] = ['k', 'm', 'i']
    data['wiek'] = ' '
    data['ID'] = ' '
    dlg = gui.DlgFromDict(data)
    if not dlg.OK:
        core.quit()
    return data
    
def draw_disk(win, peg_x, y, width, height, color, outline=False): #generalne tworzenie dysków 
    if outline:
        outline_rect = visual.Rect(win, width=width + 4, height=height + 4, fillColor=None, lineColor='white', lineWidth=2)
        outline_rect.pos = (peg_x, y)
        outline_rect.draw()
    rect = visual.Rect(win, width=width, height=height, fillColor=color, lineColor=color)
    rect.pos = (peg_x, y)
    rect.draw()

# rysowanie dysków na wieżach 
def draw_all_disks(win, pegs, current_peg):
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black']
    disk_height = 20
    for peg in range(3):
        peg_x = -200 + peg * 200
        for i, disk in enumerate(pegs[peg]):
            y = -200 + i * disk_height
            if peg == current_peg and i == len(pegs[peg]) - 1:
                draw_disk(win, peg_x, y, disk * 20, disk_height, colors[disk-1], outline=True)
            else:
                draw_disk(win, peg_x, y, disk * 20, disk_height, colors[disk-1])

# Funkcja sprawdzająca, czy ruch jest dozwolony
def is_move_valid(pegs, from_peg, to_peg):
    if len(pegs[from_peg]) == 0:
        return False
    if len(pegs[to_peg]) == 0 or pegs[from_peg][-1] < pegs[to_peg][-1]:
        return True
    return False

# Funkcja do wykonania ruchu
def make_move(pegs, from_peg, to_peg):
    if is_move_valid(pegs, from_peg, to_peg):
        disk = pegs[from_peg].pop()
        pegs[to_peg].append(disk)

# stawrzanie wież
def initialize_pegs(num_disks):
    pegs = [[] for _ in range(3)] #tworzymy tablicę trzech tablic, dyski stają się elementami tych tablic w trakcie gry  
    pegs[0] = [i for i in range(num_disks, 0, -1)]
    return pegs


def check_win(pegs, num_disks):
    return len(pegs[2]) == num_disks # gra kończy się gdy wszystkie dyski dołączone są do ostatniej wieży

data = user_data()
win = visual.Window(size=(800, 600), color="#808080", units="pix")


num_disks = 3  # liczba dysków dla 1 lvl

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
file_path = os.path.join(desktop_path, "game_results1.txt") #plik na pulpicie 

core.wait(5)
visual.TextStim(win, text = "Przed tobą pięć etapów gry Wieża Hanoi, gry polegającej na przekładaniu określonej ilości dysków pomiędzy trzema prętami.", color = 'white', height = 30).draw()
win.flip()
core.wait(5)
visual.TextStim(win, text = "Zasady gry są proste, wolno Ci kłaść jedynie dyski mniejsze na większych, na pustym pręcie położyć możesz dowolny dysk.", color = "white", height = 30).draw() 
win.flip()
core.wait(7)
while True:
    # tworzymy wieże
    pegs = initialize_pegs(num_disks)

    # zmienne wieży oraz dysku 
    current_peg = 0
    held_disk = None

    #zmienna zbierająca ruchy 
    moves = 0
    # teskt dla osoby badanej 
    start_time = core.getTime() # mierzymy czas gry od tego momentu 
    # gra sama w sobie 
    while True:
        win.clearBuffer()
        draw_all_disks(win, pegs, current_peg)

        # wyświetlanie dysków nad wieżą, wraz z obwódką 
        if held_disk is not None:
            colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black']
            peg_x = -200 + current_peg * 200
            draw_disk(win, peg_x, 100, held_disk * 20, 20, colors[held_disk-1], outline=True)

        win.flip()

        # sprawdzanie wygranej i przechodzenie do nastęnego etapu
        if check_win(pegs, num_disks):
            end_time = core.getTime()
            elapsed_time = end_time - start_time

            win.clearBuffer()
            win.flip()
            core.wait(5)
            num_disks += 1  #zmienianie etapu na następny - zwiększanie liczby dysków
            with open(file_path, "a") as file:
                file.write(f"Ilość ruchów dla {num_disks-1} dysków: {moves}\n")  #liczba ruchów dla danego etapu 
                file.write(f"Czas gry dla {num_disks-1} dysków: {elapsed_time:.2f} sekund\n")  #czas gry 
                file.write(f"ID = {data['ID']}, płeć = {data['płeć']}, wiek = {data['wiek']}\n") #drukowanie dancyh dla prób określonych osób
            if num_disks > 7: #ograniczenie liczby dysków do 7 
                visual.TextStim(win, text="Dziękujemy za udział w badaniu!", color="white", height=40).draw()
                win.flip()
                core.wait(5)
                win.close()
                core.quit()
            break

        keys = event.waitKeys(keyList=['left', 'right', 'up', 'down', 'f7'])

        if 'f7' in keys: 
            win.close()
            core.quit()

        if 'left' in keys:
            current_peg = (current_peg - 1) % 3 
        elif 'right' in keys:
            current_peg = (current_peg + 1) % 3 
        elif 'up' in keys:
            if held_disk is None and len(pegs[current_peg]) > 0:
                held_disk = pegs[current_peg].pop()
        elif 'down' in keys:
            if held_disk is not None:
                if len(pegs[current_peg]) == 0 or held_disk < pegs[current_peg][-1]:
                    pegs[current_peg].append(held_disk)
                    held_disk = None
                    moves += 1  # licznik ruchów zwiększający się po każdym odłożeniu dysku 
# Zamknięcie okna
win.close()
core.quit()