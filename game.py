import pygame
import os


WIDTH = 800
HEIGHT = 600
FPS = 60

screen_speed = 0.1 #單位
mapresize_speed = 5
size = 50 #單位長
player_pos_x = 0 #單位 #螢幕中間即為玩家座標
player_pos_y = 0 #單位

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("樹樹遊戲")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

grass_img = pygame.image.load(os.path.join("grass.gif")).convert()
sand_img = pygame.image.load(os.path.join("sand.gif")).convert()



#字
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

#獨立迴圈地圖縮放
def key_pressed():
    global size, player_pos_x, player_pos_y, mapresize_speed, screen_speed
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_UP]:
        size += mapresize_speed
    if key_pressed[pygame.K_DOWN]:
        size -= mapresize_speed
    #玩家移動
    if key_pressed[pygame.K_a]:
        player_pos_x -= screen_speed
    if key_pressed[pygame.K_d]:
        player_pos_x += screen_speed
    if key_pressed[pygame.K_w]:
        player_pos_y -= screen_speed
    if key_pressed[pygame.K_s]:
        player_pos_y += screen_speed
#def mouse_pressed

#需要 x, y, oringinal_image
def on_map_update(self, image, pos_x, pos_y):
    global size, player_pos_x, player_pos_y
    #從單位與size轉換過來的的(x, y)
    x = pos_x*size
    y = pos_y*size
    #int()的目的是不要出現隙縫
    #"-WIDTH/2","-HEIGHT/2"使物件座標比較的對象變為螢幕左上角，才可以知道螢幕的座標
    self.rect.x = x - (int(player_pos_x*size)-WIDTH/2)
    self.rect.y = y - (int(player_pos_y*size)-HEIGHT/2)
    #必須得用原來的圖片變更
    self.image = pygame.transform.scale(image, (size, size))

class blocks(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x #單位
        self.pos_y = pos_y #單位
        global size
        self.rect = pygame.Surface((size, size)).get_rect()
        if block_type == "grass":
            self.original_image = grass_img
        if block_type == "sand":
            self.original_image = sand_img
    def update(self):
        on_map_update(self, self.original_image, self.pos_x, self.pos_y)
        
class tree(pygame.sprite.Sprite):
    def __init__(self, health, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x #單位
        self.pos_y = pos_y #單位
        self.image = pygame.Surface((50, 80))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.health = health
    def tp(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
    def update(self):
        on_map_update(self, self.image, self.pos_x, self.pos_y)
        

#一般地圖
normal_map =[
    "ssggsggsgggg",
    " sggggssgggsg",
    "   ggggssssssggg",
    "gsssssgggggs"
]

#創建地圖
def create_map(selected_map):
    for column_pos, row_data in enumerate(selected_map): #直行
        for row_pos, block_type in enumerate(row_data): #橫列
            if block_type == "g":
                block = blocks("grass", row_pos, column_pos)
                map.add(block)
            if block_type == "s":
                block = blocks("sand", row_pos, column_pos)
                map.add(block)
map = pygame.sprite.Group()
create_map(normal_map)

#樹

trees = pygame.sprite.Group()
normal_tree = tree(50, 0, 0)
trees.add(normal_tree)

if __name__ == "__main__":
    running = True
    fullscreen = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            #全螢幕切換
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
            #滾輪
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    normal_tree.tp(int((pygame.mouse.get_pos()[0] - WIDTH/2 + player_pos_x*size)//size),int((pygame.mouse.get_pos()[1] - HEIGHT/2 + player_pos_y*size)//size))
                if event.button == 4:
                    size += mapresize_speed
                elif event.button == 5:
                    size -= mapresize_speed
        #偵測按鍵
        key_pressed()
        #Group更新(螢幕輸出之前)
        map.update()
        trees.update()
        #畫面顯示
        screen.fill((0,0,0))
        map.draw(screen)
        trees.draw(screen)
        draw_text(screen, str(size), 100,100,10)
        pygame.display.update()
pygame.quit()