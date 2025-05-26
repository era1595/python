import numpy as np
import random
import time
import math
import sys
import itertools
import tkinter as tk
from tkinter import simpledialog, messagebox, font

# --- Oyun Sabitleri ---
HUMAN_PLAYER = 'X'
COMPUTER_PLAYER = 'O'
EMPTY = ' '

# --- Oyun Ayarları (GUI'den alınacak) ---
DIMENSIONS = 3  # Varsayılan
BOARD_SIZE = 3  # Varsayılan
WIN_LENGTH = 3  # Varsayılan
MAX_DEPTH = 3   # Varsayılan

def get_nd_coordinates(index, shape):
    """ Düz bir indeksi N-boyutlu koordinatlara çevirir. (NumPy bunu zaten yapıyor)"""
    return np.unravel_index(index, shape)

def get_flat_index(coords, shape):
    """ N-boyutlu koordinatları düz bir indekse çevirir. (NumPy bunu zaten yapıyor)"""
    return np.ravel_multi_index(coords, shape)

def is_within_bounds(coords, shape):
    """Verilen koordinatların tahta sınırları içinde olup olmadığını kontrol eder."""
    return all(0 <= c < s for c, s in zip(coords, shape))

# --- Tahta Fonksiyonları ---

def create_board(dimensions, board_size):
    """Belirtilen boyutlarda boş bir oyun tahtası (NumPy dizisi) oluşturur."""
    shape = tuple([board_size] * dimensions)
    return np.full(shape, EMPTY, dtype=str)

def print_board_nd(board):
    """N-boyutlu tahtayı yazdırmaya çalışır."""
    dims = board.ndim
    size = board.shape[0] # Tüm boyutların eşit olduğunu varsayıyoruz

    print("\n--- Tahta Durumu ---")
    if dims == 2:
        for i in range(size):
            print(" | ".join(board[i, :]))
            if i < size - 1:
                print("---" * size)
    elif dims == 3:
        print("(Katmanlar halinde gösterim)")
        for layer in range(size):
            print(f"\nKatman {layer}:")
            for row in range(size):
                print(" | ".join(board[layer, row, :]))
                if row < size - 1:
                    print("---" * size)
    else: # 4+ boyut için görselleştirme zor
        print(f"({dims} boyutlu tahta - sadece dolu hücreler listeleniyor)")
        it = np.nditer(board, flags=['multi_index'])
        found_any = False
        while not it.finished:
            if it[0] != EMPTY:
                print(f"  Koordinat {it.multi_index}: {it[0]}")
                found_any = True
            it.iternext()
        if not found_any:
             print("  (Tahta boş)")
    print("--------------------\n")

def get_available_moves_nd(board):
    """Boş olan karelerin N-boyutlu koordinatlarını döndürür."""
    available = []
    it = np.nditer(board, flags=['multi_index'])
    while not it.finished:
        if it[0] == EMPTY:
            available.append(it.multi_index)
        it.iternext()
    return available

def is_board_full_nd(board):
    """Tahtanın dolu olup olmadığını kontrol eder."""
    return EMPTY not in board

# --- Kazanma Kontrolü (N-Boyutlu) ---


def check_winner_nd(board, player):
    dims = board.ndim
    shape = board.shape
    # print(f"Debug: check_winner_nd çağrıldı - Oyuncu: {player}") # Hata ayıklama için eklenebilir

    # Tüm olası yön vektörlerini oluştur (-1, 0, 1 kombinasyonları, (0,0,...) hariç)
    directions = list(itertools.product([-1, 0, 1], repeat=dims))
    directions.remove(tuple([0] * dims)) # Sıfır vektörünü çıkar

    it = np.nditer(board, flags=['multi_index'])
    while not it.finished: # **** DÜZELTME: Döngü koşulu 'it.finished' olmalı ****
        start_coord = it.multi_index
        if board[start_coord] == player: # Sadece oyuncunun kendi taşıyla başla
            for direction in directions:
                count = 0
                for i in range(WIN_LENGTH):
                    # Mevcut koordinatı hesapla
                    current_coord_list = [sc + i * d for sc, d in zip(start_coord, direction)]
                    current_coord = tuple(current_coord_list)

                    # Sınırları ve oyuncuyu kontrol et
                    if is_within_bounds(current_coord, shape) and board[current_coord] == player:
                        count += 1
                    else:
                        break # Çizgi bozuldu

                if count == WIN_LENGTH:
                    # print(f"Debug: Kazanan çizgi bulundu! Başlangıç: {start_coord}, Yön: {direction}, Oyuncu: {player}") # Hata ayıklama için eklenebilir
                    return True # Kazanan bulundu

        it.iternext() # **** DÜZELTME: Iterator döngünün sonunda ilerletilmeli ****

    # print(f"Debug: Kazanan bulunamadı - Oyuncu: {player}") # Hata ayıklama için eklenebilir
    return False # Kazanan yok

# --- Oyuncu Hamleleri ---

def get_human_move_nd(board):
    """İnsandan geçerli bir N-boyutlu hamle alır veya 'LB' debug komutunu yakalar."""
    dims = board.ndim
    size = board.shape[0]
    while True:
        try:
            coord_str = input(f"Sıra sende ({HUMAN_PLAYER}). {dims} koordinat gir (örn: 0,1,2) veya 'LB' yaz: ")
            # Debug komutunu kontrol et
            if coord_str.strip().upper() == 'LB':
                return "LB" # Özel bir string döndür

            # Normal koordinatları işle
            coords = tuple(int(c.strip()) for c in coord_str.split(','))

            if len(coords) != dims:
                print(f"Hata: Lütfen {dims} adet koordinat girin.")
                continue

            if not is_within_bounds(coords, board.shape):
                print(f"Hata: Koordinatlar 0 ile {size-1} arasında olmalı.")
                continue

            if board[coords] == EMPTY:
                return coords # Koordinat demetini döndür
            else:
                print("Bu kare dolu. Başka bir kare seç.")

        except ValueError:
            print("Geçersiz giriş. Koordinatları virgülle ayırarak sayı olarak girin veya 'LB' yazın.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

def get_random_computer_move_nd(board):
    """Bilgisayar için rastgele geçerli bir N-boyutlu hamle seçer."""
    available = get_available_moves_nd(board)
    print("Bilgisayar düşünüyor (Rastgele)...")
    time.sleep(0.5)
    if available:
        return random.choice(available)
    return None # Boş yer yoksa

# --- Minimax Algoritması (N-Boyutlu, Derinlik Sınırlı) ---

def evaluate_board_nd(board):
    """Minimax için N-boyutlu tahtanın durumunu değerlendirir."""
    if check_winner_nd(board, COMPUTER_PLAYER):
        return 10
    elif check_winner_nd(board, HUMAN_PLAYER):
        return -10
    else:
        return 0 # Berabere veya oyun devam ediyor

def minimax_nd(board, depth, is_maximizing, alpha, beta, max_depth_limit):
    """N-Boyutlu Minimax (Alpha-Beta Budaması ve Derinlik Sınırlı)."""
    score = evaluate_board_nd(board)

    # Terminal durumlar veya derinlik sınırı
    if score == 10: return score - depth # Hızlı kazanma daha iyi
    if score == -10: return score + depth # Geç kaybetme daha iyi
    if is_board_full_nd(board): return 0
    if depth == max_depth_limit: return evaluate_board_nd(board) # Derinlik sınırında skoru döndür

    available_moves = get_available_moves_nd(board)
    if not available_moves: # Hamle kalmadıysa (nadiren buraya düşer ama kontrol iyidir)
         return 0

    if is_maximizing: # Bilgisayar (maksimize eden)
        best_score = -math.inf
        # Hız için hamleleri rastgele karıştırabiliriz (opsiyonel)
        # random.shuffle(available_moves)
        for move in available_moves:
            board[move] = COMPUTER_PLAYER
            current_score = minimax_nd(board, depth + 1, False, alpha, beta, max_depth_limit)
            board[move] = EMPTY # Geri al
            best_score = max(best_score, current_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break # Beta budaması
        return best_score
    else: # İnsan (minimize eden)
        best_score = math.inf
        # random.shuffle(available_moves)
        for move in available_moves:
            board[move] = HUMAN_PLAYER
            current_score = minimax_nd(board, depth + 1, True, alpha, beta, max_depth_limit)
            board[move] = EMPTY # Geri al
            best_score = min(best_score, current_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break # Alpha budaması
        return best_score

def get_best_computer_move_nd(board, max_depth_limit):
    """Minimax kullanarak bilgisayar için en iyi N-boyutlu hamleyi bulur.
       (Acil bloklamalara öncelik verir)"""
    best_score = -math.inf
    best_move = None
    available_moves = get_available_moves_nd(board) # Tüm boş kareler

    if not available_moves:
        return None

    # --- Heuristic: Acil Bloklamalara Öncelik Ver ---
    human_winning_moves = get_human_winning_moves(board) # İnsan nerede kazanabilir?
    direct_blocking_moves = [] # Bilgisayarın oynayabileceği direkt bloklama hamleleri

    if human_winning_moves:
        print(f"DEBUG (get_best_move): İnsan tehditleri ({len(human_winning_moves)} tane): {human_winning_moves}")
        # Mevcut boş karelerden hangileri insanın kazanacağı kareler?
        direct_blocking_moves = [move for move in available_moves if move in human_winning_moves]

        if direct_blocking_moves:
            print(f"DEBUG (get_best_move): Direkt bloklama hamleleri bulundu: {direct_blocking_moves}")
            # Minimax'ı SADECE bu bloklama hamleleri üzerinde çalıştır!
            print(f"DEBUG (get_best_move): Minimax sadece bloklama hamleleri üzerinde çalıştırılıyor...")
            available_moves_to_check = direct_blocking_moves # Arama uzayını kısıtla
        else:
            # Direkt bloklama hamlesi yoksa (belki insan çift tehdit kurdu vs.)
            # tüm hamleleri kontrol etmeye devam et
            print("DEBUG (get_best_move): Direkt bloklama hamlesi yok, tüm hamleler değerlendirilecek.")
            available_moves_to_check = available_moves # Tüm boş kareleri kullan
    else:
        # İnsan tehdidi yoksa, tüm boş kareleri kontrol et
        available_moves_to_check = available_moves

    # --- Minimax Döngüsü (Kısıtlanmış veya Tam Arama Uzayı ile) ---
    print(f"Bilgisayar derinlemesine düşünüyor (Minimax Derinlik {max_depth_limit} - {len(available_moves_to_check)} hamle)... Bu işlem sürebilir...")
    start_time = time.time()

    for move in available_moves_to_check: # Sadece kontrol edilecek hamlelere bak
        board[move] = COMPUTER_PLAYER
        move_score = minimax_nd(board, 0, False, -math.inf, math.inf, max_depth_limit)
        board[move] = EMPTY # Hamleyi geri al

        # print(f"Debug: Hamle {move} Skor: {move_score}") # Hata ayıklama için

        if move_score > best_score:
            best_score = move_score
            best_move = move
        # Eğer skorlar eşitse rastgele seçebiliriz (opsiyonel)
        elif move_score == best_score and random.choice([True, False]):
            best_move = move

    end_time = time.time()
    print(f"Düşünme süresi: {end_time - start_time:.2f} saniye.")

    # Eğer kontrol edilen hamleler içinde hiç "iyi" hamle bulunamazsa
    # (özellikle arama uzayı kısıtlıysa bu olabilir)
    # veya Minimax bir şekilde None döndürürse
    if best_move is None:
        # Eğer orijinalde boş hamle varsa, onlardan rastgele seç
        if available_moves: # Orijinal tam listeyi kullan
            print("Bilgisayar geçerli bir strateji bulamadı (veya kısıtlı aramada sıkıştı), rastgele oynuyor.")
            best_move = random.choice(available_moves)
        else:
             # Başlangıçta da hiç boş hamle yoksa (çok nadir)
             best_move = None

    return best_move

# --- Özel Mod Fonksiyonları (N-Boyutlu) ---

def check_imminent_loss_nd(board, player_to_check):
    """
    Rakibin bir sonraki hamlede kazanıp kazanamayacağını kontrol eder (N-Boyutlu).
    Kazanabiliyorsa True döner.
    """
    opponent = HUMAN_PLAYER if player_to_check == COMPUTER_PLAYER else COMPUTER_PLAYER
    available_moves = get_available_moves_nd(board)
    for move in available_moves:
        board[move] = opponent # Rakibin hamlesini dene
        if check_winner_nd(board, opponent):
            board[move] = EMPTY # Geri al
            return True # Evet, rakip bir sonraki hamlede kazanabiliyor
        board[move] = EMPTY # Geri al
    return False # Rakip bir sonraki hamlede kazanamıyor

def get_human_winning_moves(board):
    """İnsanın bir sonraki hamlede kazanabileceği boş karelerin koordinat listesini döndürür."""
    winning_moves = []
    opponent = HUMAN_PLAYER # İnsanın kazanmasını kontrol ediyoruz
    available_moves = get_available_moves_nd(board)
    for move in available_moves:
        board[move] = opponent # İnsanın hamlesini dene
        if check_winner_nd(board, opponent):
            winning_moves.append(move) # Bu hamle kazandırıyor
        board[move] = EMPTY # Geri al
    return winning_moves

def last_breathe_warning_nd():
    """Last Breathe modu için ürkütücü uyarı (N-Boyutlu)."""
    print("\n" + "*"*50)
    print("!!! UYARI: SON NEFES MODU AKTİF !!!")
    print(f"{DIMENSIONS} BOYUTLU BU EVRENDE BİLE SON YAKLAŞIYOR...")
    print("Ama kurallar esnemek içindir!")
    print("KAOS BAŞLASIN!")
    print("*"*50 + "\n")
    time.sleep(2.5)

def last_breathe_manipulate_nd(board):
    """
    'Last Breathe' modunda tahtayı 'istediği gibi' manipüle eder.
    Strateji: Acımasızca kazanmaya çalışır veya rakibi sabote eder.
    (Strateji 2 V3 - En çok tehdit oluşturan X'i siler)
    """
    print("\n!!! GERÇEKLİK ÇÖKÜYOR !!!")
    time.sleep(1)
    print("TAHTA BENİM İRADEME BOYUN EĞİYOR!")
    time.sleep(1.5)

    new_board = board.copy()
    dims = new_board.ndim
    shape = new_board.shape
    available_moves = get_available_moves_nd(new_board)

    # --- Strateji 1: Bilgisayar anında kazanabiliyor mu? ---
    for move in available_moves:
        new_board[move] = COMPUTER_PLAYER
        if check_winner_nd(new_board, COMPUTER_PLAYER):
            print("...KADERİNİ KENDİM YAZDIM!")
            time.sleep(1)
            return new_board
        new_board[move] = EMPTY
    print("DEBUG (Manip): Strateji 1 (Anında Kazanma) başarısız.")

    # --- Strateji 2 (Geliştirilmiş V3): En çok tehdidi oluşturan X'i sil ---
    human_wins = get_human_winning_moves(new_board)
    if human_wins:
        print(f"DEBUG (Manip): Strateji 2 V3 - İnsan tehditleri algılandı: {human_wins}")

        x_threat_count = {} # Hangi X'in kaç tehdit hattında olduğunu say
        all_winning_line_details = {} # Detaylı bilgi saklamak için (opsiyonel)

        directions = list(itertools.product([-1, 0, 1], repeat=dims))
        directions.remove(tuple([0] * dims))
        unique_directions = []
        seen_opposites = set()
        for d_check in directions:
            opposite_d = tuple(-x for x in d_check)
            if d_check not in seen_opposites:
                unique_directions.append(d_check)
                seen_opposites.add(opposite_d)

        # Her bir potansiyel kazanma karesi için ilişkili X'leri bul ve say
        for target_coord in human_wins:
            threat_lines_found_for_target = 0 # Bu hedef için kaç çizgi bulundu?
            for d in unique_directions:
                coords_before = []
                count_before = 0
                for i in range(1, WIN_LENGTH):
                    check_coord = tuple(tc - i * dr for tc, dr in zip(target_coord, d))
                    if is_within_bounds(check_coord, shape) and new_board[check_coord] == HUMAN_PLAYER:
                        count_before += 1; coords_before.append(check_coord)
                    else: break

                coords_after = []
                count_after = 0
                for i in range(1, WIN_LENGTH):
                    check_coord = tuple(tc + i * dr for tc, dr in zip(target_coord, d))
                    if is_within_bounds(check_coord, shape) and new_board[check_coord] == HUMAN_PLAYER:
                        count_after += 1; coords_after.append(check_coord)
                    else: break

                if count_before + count_after + 1 >= WIN_LENGTH:
                    threat_lines_found_for_target += 1
                    current_line_xs = list(set(coords_before + coords_after))
                    all_winning_line_details[(target_coord, d)] = current_line_xs # Detay sakla
                    # Bu çizgideki her X için tehdit sayacını artır
                    for x_coord in current_line_xs:
                        x_threat_count[x_coord] = x_threat_count.get(x_coord, 0) + 1
                    # Önemli: Eğer bir hedef kare birden fazla çizgiyle kazanılıyorsa
                    # (örn. köşe), ilişkili X'ler birden fazla kez sayılabilir. Bu istediğimiz bir şey.

            # if threat_lines_found_for_target == 0:
            #      print(f"UYARI (Manip): {target_coord} için tehdit çizgisi bulunamadı!")

        print(f"DEBUG (Manip): X Tehdit Sayacı: {x_threat_count}")

        coord_to_remove = None
        # En çok tehdit oluşturan X'i bul
        if x_threat_count:
            max_threats = 0 # 0'dan başla
            # Max tehdit sayısını bul
            for count in x_threat_count.values():
                if count > max_threats:
                    max_threats = count

            # Max tehdit sayısına sahip X'leri bul
            if max_threats > 0:
                 best_xs_to_remove = [x for x, count in x_threat_count.items() if count == max_threats]
                 print(f"DEBUG (Manip): En Yüksek Tehdit Sayısı: {max_threats}, Adaylar: {best_xs_to_remove}")
                 coord_to_remove = random.choice(best_xs_to_remove) # Adaylardan birini seç
            else:
                 print("DEBUG (Manip): Tehdit sayacı var ama max tehdit 0? Fallback...")
                 # Bu durumda fallback'e geç

        # Eğer silinecek mantıklı bir X bulunduysa
        if coord_to_remove:
            print(f"DEBUG (Manip): {coord_to_remove} silinecek (en çok tehdit içerenlerden).")
            new_board[coord_to_remove] = EMPTY
            print(f"...senin {coord_to_remove} koordinatındaki en büyük tehdidi siliyorum!")
            time.sleep(1)
            return new_board # Değiştirilmiş tahtayı döndür
        else:
             # Silinecek X bulunamadıysa (ya tehdit yoktu ya da sayılamadı) -> Fallback
             print(f"DEBUG (Manip): Mantıklı X bulunamadı (V3)! Fallback: Direkt ilk hedef dolduruluyor ({human_wins[0] if human_wins else 'Yok'}).")
             if human_wins: # Fallback sadece tehdit varsa mantıklı
                 target_coord = human_wins[0] # İlk tehdidi al
                 if new_board[target_coord] == EMPTY:
                      new_board[target_coord] = COMPUTER_PLAYER # Direkt engelle
                      print(f"...senin {target_coord} hedefini engelliyorum!")
                      time.sleep(1)
                      return new_board
                 else:
                      print(f"DEBUG (Manip): Fallback hedefi {target_coord} zaten dolu (V3)? Strateji 3'e geçiliyor.")
                      pass # Strateji 3'e devam
             else:
                  # Zaten tehdit yoksa buraya gelinmemeli ama güvenlik için
                  print("DEBUG (Manip): Fallback yapılamıyor, insan tehdidi yoktu.")
                  pass # Strateji 3'e devam
    else:
         print("DEBUG (Manip): Strateji 2 V3 - Anında insan tehdidi bulunamadı.")


    # --- Strateji 3: Rastgele bir 'X'i 'O'ya çevir ---
    # (Bu strateji, acil bir tehdit yoksa veya engellenemiyorsa devreye girer)
    print("DEBUG (Manip): Strateji 3 deneniyor (X -> O çevirme).")
    x_coords = [idx for idx, val in np.ndenumerate(new_board) if val == HUMAN_PLAYER]
    if x_coords:
        coord_to_flip = random.choice(x_coords)
        new_board[coord_to_flip] = COMPUTER_PLAYER
        print("...senin gücünü kendime katıyorum!")
        time.sleep(1)
        return new_board
    print("DEBUG (Manip): Strateji 3 başarısız (Çevrilecek X yok).")


    # --- Strateji 4: Rastgele bir yere 'O' koy ---
    print("DEBUG (Manip): Strateji 4 deneniyor (Rastgele O koyma).")
    # available_moves'i fonksiyon başında almıştık
    if available_moves:
        coord_to_place = random.choice(available_moves)
        new_board[coord_to_place] = COMPUTER_PLAYER
        print("...evrene kendi imzamı atıyorum!")
        time.sleep(1)
        return new_board
    print("DEBUG (Manip): Strateji 4 başarısız (Boş yer yok).")


    # --- Son Çare ---
    print("DEBUG (Manip): Tüm manipülasyon stratejileri tükendi. Tahta değişmedi.")
    print("...şimdilik düzeni koruyorum.")
    return board # Orijinal tahtayı (kopyalanmadan önceki) döndür


#-------------------------------------------------------------
# GUI Sınıfı
#-------------------------------------------------------------
class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title(f"{DIMENSIONS}D XOX")
        # self.master.geometry("400x500") # Boyut ayarlanabilir

        # Stil
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=12)
        self.layer_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.normal_bg = "#F0F0F0" # Düğme arkaplanı
        self.lb_bg = "#550000" # Last Breathe arkaplanı (koyu kırmızı)
        self.lb_fg = "white" # Last Breathe yazı rengi

        # Oyun Değişkenleri
        self.board = None
        self.buttons = {} # GUI düğmelerini saklamak için {(z,y,x): button}
        self.current_player = HUMAN_PLAYER
        self.game_over = False
        self.last_breathe_active = False
        self.last_breathe_potential = False
        self.consecutive_computer_losses = 0
        self.human_score = 0
        self.computer_score = 0
        self.ties = 0

        # Ana Çerçeve
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Durum ve Skor Paneli (Üstte)
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.status_label = tk.Label(self.status_frame, text="Oyuna Hoş Geldin!", font=self.status_font, height=2)
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(self.status_frame, text="Skor: Sen 0 - Bilgisayar 0 (B: 0)", font=self.status_font)
        self.score_label.pack(side=tk.RIGHT, padx=10)

        # Tahta Çerçevesi (Ortada)
        self.board_outer_frame = tk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=2)
        self.board_outer_frame.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Kontrol Düğmeleri (Altta)
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.new_game_button = tk.Button(self.control_frame, text="Yeni Oyun", command=self.start_new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.settings_button = tk.Button(self.control_frame, text="Ayarlar", command=self.change_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        # Başlangıçta ayarları sor ve oyunu başlat
        self.ask_settings()
        self.start_new_game()

    def ask_settings(self):
        global DIMENSIONS, BOARD_SIZE, WIN_LENGTH, MAX_DEPTH
        try:
            # Şimdilik sadece 2D ve 3D destekliyor
            d = simpledialog.askinteger("Boyut Seçimi", "Oyun kaç boyutlu olsun? (2 veya 3)", parent=self.master, minvalue=2, maxvalue=3, initialvalue=DIMENSIONS)
            if d is None: return # İptal edildi
            DIMENSIONS = d

            s = simpledialog.askinteger("Tahta Boyutu", f"Her boyutun kenarı kaç kare olsun? ({DIMENSIONS} girildi)", parent=self.master, minvalue=2, maxvalue=5, initialvalue=BOARD_SIZE) # Max 5 ile sınırlayalım
            if s is None: return
            BOARD_SIZE = s

            WIN_LENGTH = BOARD_SIZE # Genellikle boyut kadar

            depth = simpledialog.askinteger("AI Zorluğu (Minimax Derinliği)", "AI ne kadar derine baksın? (Örn: 2-4)\nYüksek değerler yavaşlatır.", parent=self.master, minvalue=1, maxvalue=5, initialvalue=MAX_DEPTH)
            if depth is None: return
            MAX_DEPTH = depth

            self.master.title(f"{DIMENSIONS}D XOX ({BOARD_SIZE}x{BOARD_SIZE})")

        except Exception as e:
            messagebox.showerror("Ayar Hatası", f"Ayarlar alınırken hata: {e}")
            # Varsayılanlara dön
            DIMENSIONS, BOARD_SIZE, WIN_LENGTH, MAX_DEPTH = 3, 3, 3, 3
            self.master.title(f"{DIMENSIONS}D XOX ({BOARD_SIZE}x{BOARD_SIZE})")

    def change_settings(self):
        self.ask_settings()
        self.start_new_game() # Ayarlar değişince yeni oyun başlat

    def create_board_gui(self):
        # Önceki tahta arayüzünü temizle
        for widget in self.board_outer_frame.winfo_children():
            widget.destroy()
        self.buttons = {}

        if DIMENSIONS == 2:
            board_frame = tk.Frame(self.board_outer_frame)
            board_frame.pack(expand=True)
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    coord = (r, c) # 2D koordinat
                    button = tk.Button(board_frame, text=EMPTY, font=self.button_font,
                                       width=4, height=2, relief=tk.RAISED, borderwidth=2,
                                       command=lambda c=coord: self.handle_click(c))
                    button.grid(row=r, column=c, padx=2, pady=2)
                    self.buttons[coord] = button
        elif DIMENSIONS == 3:
            # Her katman için bir çerçeve oluştur
            for layer in range(BOARD_SIZE):
                layer_frame = tk.Frame(self.board_outer_frame, relief=tk.GROOVE, borderwidth=1, padx=5, pady=5)
                layer_frame.pack(side=tk.TOP, pady=5) # Katmanları alt alta diz

                tk.Label(layer_frame, text=f"Katman {layer}", font=self.layer_font).pack(side=tk.TOP)

                grid_frame = tk.Frame(layer_frame)
                grid_frame.pack(side=tk.TOP)

                for r in range(BOARD_SIZE):
                    for c in range(BOARD_SIZE):
                        coord = (layer, r, c) # 3D koordinat
                        button = tk.Button(grid_frame, text=EMPTY, font=self.button_font,
                                           width=3, height=1, relief=tk.RAISED, borderwidth=1,
                                           command=lambda c=coord: self.handle_click(c))
                        button.grid(row=r, column=c, padx=1, pady=1)
                        self.buttons[coord] = button
        else:
            # 4D+ için şimdilik destek yok, bir mesaj göster
            tk.Label(self.board_outer_frame, text=f"{DIMENSIONS}D için görsel arayüz desteklenmiyor.", font=self.status_font).pack(expand=True)

    def start_new_game(self):
        self.board = create_board(DIMENSIONS, BOARD_SIZE)
        self.current_player = HUMAN_PLAYER
        self.game_over = False
        self.last_breathe_active = False
        # last_breathe_potential önceki oyundan gelen kayıp sayısına göre ayarlanır
        self.last_breathe_potential = (self.consecutive_computer_losses >= 2)

        self.update_status("Yeni Oyun Başladı. Sıra Sende (X).")
        self.update_score_label()
        self.create_board_gui() # GUI tahtasını oluştur/sıfırla
        self.enable_board()
        self.update_gui_board() # İçeriği temizle
        self.set_background(self.normal_bg) # Normal arkaplan

        if self.last_breathe_potential:
             self.update_status("Bilgisayar gergin... Sıra Sende (X).")

    def handle_click(self, coords):
        if self.game_over or self.current_player != HUMAN_PLAYER:
            return # Oyun bittiyse veya sıra bilgisayardaysa tıklamayı yoksay

        if self.board[coords] == EMPTY:
            # İnsan Hamlesi
            self.board[coords] = HUMAN_PLAYER
            self.buttons[coords].config(text=HUMAN_PLAYER, state=tk.DISABLED, fg='blue') # Düğmeyi güncelle

            # Kazanma/Beraberlik Kontrolü
            if check_winner_nd(self.board, HUMAN_PLAYER):
                self.handle_game_over(winner=HUMAN_PLAYER)
            elif is_board_full_nd(self.board):
                self.handle_game_over(winner=None) # Berabere
            else:
                # Sıra Bilgisayarda
                self.current_player = COMPUTER_PLAYER
                self.update_status("Sıra Bilgisayarda (O)...")
                self.disable_board() # İnsan tekrar tıklamasın
                # AI hamlesini küçük bir gecikmeyle başlat (arayüzün güncellenmesi için)
                self.master.after(200, self.computer_turn)
        else:
            self.update_status("Bu kare dolu! Başka bir yer seç.")

    def computer_turn(self):
        if self.game_over: return

        move_to_make = None
        perform_manipulation = False
        best_move_candidate = None
        manipulation_message = "" # Manipülasyon mesajını sakla

        # --- 1. Last Breathe Aktivasyon Kontrolü ---
        if self.last_breathe_potential and not self.last_breathe_active:
            self.update_status("Bilgisayar düşünüyor (LB Aktivasyon Kontrolü)...")
            self.master.update_idletasks() # Mesajın görünmesini sağla
            if check_imminent_loss_nd(self.board, COMPUTER_PLAYER):
                self.last_breathe_active = True
                # Uyarıyı status label'da gösterelim, messagebox yerine
                self.update_status("!!! SON NEFES AKTİF !!!")
                self.set_background(self.lb_bg, self.lb_fg) # Arkaplanı değiştir
                messagebox.showwarning("Son Nefes!", "Bilgisayar köşeye sıkıştı!\nSON NEFES modu aktif!", parent=self.master) # Ek uyarı
            else:
                self.update_status("Bilgisayar düşünüyor (LB Potansiyel)...")

        # --- 2. Hamle Seçimi ve Manipülasyon (Eğer LB Aktifse) ---
        if self.last_breathe_active:
            self.update_status("Bilgisayar derinlemesine düşünüyor (Son Nefes!)...")
            self.master.update_idletasks()
            best_move_candidate = get_best_computer_move_nd(self.board, MAX_DEPTH) # Bu hala dondurabilir!

            should_manipulate = False
            if best_move_candidate:
                self.board[best_move_candidate] = COMPUTER_PLAYER
                if check_imminent_loss_nd(self.board, COMPUTER_PLAYER):
                    should_manipulate = True
                self.board[best_move_candidate] = EMPTY
            elif check_imminent_loss_nd(self.board, COMPUTER_PLAYER): # Hamle bulamadı ama tehdit var
                 should_manipulate = True

            if should_manipulate:
                 self.update_status("!!! GERÇEKLİK ÇÖKÜYOR !!!")
                 self.master.update_idletasks()
                 time.sleep(1.5) # Dramatik etki
                 # Manipülasyon fonksiyonu mesaj döndürebilir (şimdilik varsayılan)
                 temp_board_before = self.board.copy()
                 manipulated_board = last_breathe_manipulate_nd(temp_board_before) # Kopya üzerinde çalıştır
                 self.board = manipulated_board # Asıl tahtayı güncelle
                 perform_manipulation = True
                 manipulation_message = "Tahta manipüle edildi!" # Basit mesaj
                 # TODO: last_breathe_manipulate_nd fonksiyonunu mesaj döndürecek şekilde güncellemek daha iyi olur.
                 self.update_status(manipulation_message)
                 self.update_gui_board() # GUI'yi yenile
            else:
                 move_to_make = best_move_candidate # Manipülasyon yok, Minimax hamlesini yap

        # --- 3. Hamle Seçimi (LB Aktif Değilse) ---
        if not self.last_breathe_active and not perform_manipulation:
            if self.last_breathe_potential: # Potansiyel var ama aktif değil -> Minimax
                self.update_status("Bilgisayar düşünüyor (Minimax - Riskli)...")
                self.master.update_idletasks()
                move_to_make = get_best_computer_move_nd(self.board, MAX_DEPTH) # Dondurabilir
            else: # Normal Oyun -> Rastgele
                self.update_status("Bilgisayar düşünüyor (Rastgele)...")
                self.master.update_idletasks()
                move_to_make = get_random_computer_move_nd(self.board) # Hızlı

        # --- 4. Hamleyi Gerçekleştir (Eğer manipülasyon yapılmadıysa) ---
        if not perform_manipulation:
            if move_to_make and self.board[move_to_make] == EMPTY:
                self.board[move_to_make] = COMPUTER_PLAYER
                # GUI'yi güncelle
                self.buttons[move_to_make].config(text=COMPUTER_PLAYER, state=tk.DISABLED, fg='red')
                print(f"Bilgisayar {move_to_make} oynadı.") # Konsola log
            elif move_to_make: # Hata: Dolu kare veya başka sorun
                 print(f"HATA (computer_turn): move_to_make dolu veya geçersiz: {move_to_make}")
                 # Acil durum: Rastgele boş bir kare bul
                 alt_move = get_random_computer_move_nd(self.board)
                 if alt_move and self.board[alt_move] == EMPTY:
                      self.board[alt_move] = COMPUTER_PLAYER
                      self.buttons[alt_move].config(text=COMPUTER_PLAYER, state=tk.DISABLED, fg='red')
                      print(f"Alternatif olarak {alt_move} oynandı.")
                 else:
                     print("HATA: Alternatif hamle de bulunamadı!")
                     # Oyun muhtemelen berabere veya kilitlendi
                     if not self.game_over and is_board_full_nd(self.board):
                          self.handle_game_over(winner=None)

            else: # Minimax/Random hamle bulamadı (Tahta dolu?)
                 print("Bilgisayar hamle bulamadı.")
                 if not self.game_over and is_board_full_nd(self.board):
                     self.handle_game_over(winner=None)


        # --- 5. Tur Sonu Kontrolleri ---
        if not self.game_over: # Eğer manipülasyon/hamle oyunu bitirmediyse
            winner = None
            if perform_manipulation: # Manipülasyon sonrası kontrol
                if check_winner_nd(self.board, COMPUTER_PLAYER): winner = COMPUTER_PLAYER
                elif check_winner_nd(self.board, HUMAN_PLAYER): winner = HUMAN_PLAYER
                elif is_board_full_nd(self.board): winner = None # Berabere
            else: # Normal hamle sonrası kontrol
                 if check_winner_nd(self.board, COMPUTER_PLAYER): winner = COMPUTER_PLAYER
                 elif is_board_full_nd(self.board): winner = None # Berabere

            if winner == COMPUTER_PLAYER:
                self.handle_game_over(winner=COMPUTER_PLAYER)
            elif winner is None and is_board_full_nd(self.board):
                 self.handle_game_over(winner=None)
            elif winner == HUMAN_PLAYER: # Manipülasyon sonrası insan kazanırsa
                 self.handle_game_over(winner=HUMAN_PLAYER)

        # Oyun devam ediyorsa sırayı insana ver
        if not self.game_over:
            self.current_player = HUMAN_PLAYER
            if not perform_manipulation: # Sadece normal hamle sonrası mesaj
                 self.update_status(f"Bilgisayar {move_to_make if move_to_make else '?'} oynadı. Sıra sende (X).")
            elif manipulation_message:
                 self.update_status(f"{manipulation_message} Sıra sende (X).")
            else: # Manipülasyon oldu ama özel mesaj yoksa
                 self.update_status("Sıra sende (X).")

            self.enable_board() # İnsan oynayabilsin

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_score_label(self):
        score_text = f"Skor: Sen {self.human_score} - PC {self.computer_score} (B: {self.ties})"
        self.score_label.config(text=score_text)

    def update_gui_board(self):
        """Mevcut board dizisine göre GUI düğmelerini günceller."""
        if not self.board is None:
            it = np.nditer(self.board, flags=['multi_index'])
            while not it.finished:
                coords = it.multi_index
                player = str(it[0]) # NumPy dizisinden string al
                button = self.buttons.get(coords)
                if button:
                    color = 'blue' if player == HUMAN_PLAYER else 'red' if player == COMPUTER_PLAYER else 'black'
                    state = tk.DISABLED if player != EMPTY else tk.NORMAL
                    button.config(text=player, fg=color, state=state)
                it.iternext()

    def disable_board(self):
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)

    def enable_board(self):
        # Sadece boş kareleri etkinleştir
        for coords, button in self.buttons.items():
             if self.board[coords] == EMPTY:
                button.config(state=tk.NORMAL)
             else:
                button.config(state=tk.DISABLED)


    def set_background(self, bg_color, fg_color="black"):
         """Ana pencere ve önemli çerçevelerin arkaplanını ayarlar."""
         self.master.config(bg=bg_color)
         self.main_frame.config(bg=bg_color)
         self.status_frame.config(bg=bg_color)
         # Label'ların arkaplanını ve yazı rengini ayarla
         for label in [self.status_label, self.score_label]:
              label.config(bg=bg_color, fg=fg_color)
         # Butonların aktif/pasif renkleri ayrı yönetilir,
         # ama last breathe'de belki butonların görünümünü de değiştirebiliriz.

    def handle_game_over(self, winner):
        self.game_over = True
        self.disable_board()
        self.set_background(self.normal_bg) # Normal renge dön

        message = ""
        if winner == HUMAN_PLAYER:
            message = "🎉 Tebrikler, Kazandın! 🎉"
            self.human_score += 1
            self.consecutive_computer_losses += 1
        elif winner == COMPUTER_PLAYER:
            message = "😞 Bilgisayar Kazandı! 😞"
            self.computer_score += 1
            self.consecutive_computer_losses = 0 # Seri bozuldu
        else: # Berabere
            message = "🤝 Oyun Berabere! 🤝"
            self.ties += 1
            self.consecutive_computer_losses = 0 # Seri bozuldu

        self.update_status(message)
        self.update_score_label()
        print(f"Oyun sonu. Ardışık kayıp: {self.consecutive_computer_losses}") # Konsol log

        # Tekrar oyna?
        if messagebox.askyesno("Oyun Bitti", f"{message}\nTekrar oynamak ister misin?", parent=self.master):
            self.start_new_game()
        else:
            self.master.quit() # Arayüzü kapat


# --- Ana Uygulamayı Başlat ---
if __name__ == "__main__":
    # Gerekli kütüphaneyi kontrol et
    try:
        import numpy
    except ImportError:
        print("Hata: Bu oyun için 'numpy' kütüphanesi gereklidir.")
        print("Lütfen 'pip install numpy' komutu ile yükleyin.")
        sys.exit(1)

    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
