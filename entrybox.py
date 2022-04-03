import pygame
import sys,os
import time

pygame.init()

file_dir = os.path.dirname(__file__)
punc = ("\"","\'",'!',"#","$","%","&","(",")","*","+","-",".","/",":",";","<","=",">","?","@","[","\\","^","_","{","|","}","~")

white = (255,255,255)
black = (0,0,0)
nickel_grey = (186,182,170)
platinum = (229,225,230)

img_ext = "png"
load_img = lambda path,img,ext=img_ext: pygame.image.load(file_dir+os.path.join("\\%s\\%s.%s"%(path,img,ext))).convert_alpha()
trans_img = lambda img,width,height: pygame.transform.smoothscale(img,(int(width),int(height)))

def draw_text(surf,text,font,size,color,pos,anti_alias = True,blit=True):
    font = pygame.font.Font(font,size) if font != None else pygame.font.SysFont(font,size)
    text_surf = font.render(text,anti_alias,color)
    text_surf_rect = text_surf.get_rect()
    text_surf_rect.left,text_surf_rect.top = pos
    if blit: surf.blit(text_surf,text_surf_rect)
    return text_surf,text_surf_rect


class Entry:
    entries = []
    def __init__(self,screen,font=None,text='',width=100,height=20,left=0,top=0,activecl=(186,182,170),inactivecl=(229,225,230),depth=0,edge=(0,0,0,0),staticalpha=255,dynamicalpha=255,textcl=(0,0,0),cursorcl=(0,0,0),show=None,lock=False,type="alnum",limit=-1,msg="",mindigvalue=None,maxdigvalue=None,blink=False,lock_open_img=(None,None,None),lock_img=(None,None,None)):
        Entry.entries.append(self)
        self.__pos = len(Entry.entries)-1
        self.__screen = screen
        self.__font = font
        self.res = (width,height)
        self.left = left
        self.top = top
        self.activecl = activecl
        self.inactivecl = inactivecl
        self.__depth = depth
        self.__edge = edge
        self.staticalpha = staticalpha
        self.dynamicalpha = dynamicalpha
        self.__surface = pygame.Surface(self.res,pygame.SRCALPHA)
        self.__rect = self.__surface.get_rect()
        self.__rect.left,self.__rect.top = self.left,self.top
        self.bottom = self.__rect.bottom
        self.right = self.__rect.right
        self.center = self.__rect.center
        self.text = text
        self.__blink = blink
        self.__type = type
        if self.__type == "digit":
            self.mindigvalue = mindigvalue
            self.maxdigvalue = maxdigvalue
        self.textcl = textcl
        self.cursorcl = cursorcl
        self.__textsize = int(self.res[1]/1.5)
        self.__size = self.__textsize
        self.__limit = int(self.res[0]/(self.__size/2))
        if limit<self.__limit and limit>0:
            self.__limit=limit
        if self.__type == "digit":
            if len(str(self.maxdigvalue))>self.__limit:
                self.__limit = len(str(self.maxdigvalue))

        self.msg = msg
        if len(self.msg)>self.__limit:
            self.msg = self.msg[:self.__limit]

        self.__select = False
        self.__full_select = False
        self.__lock = lock
        self.showvalue = True
        if self.__lock:
            self.showvalue = False
            if show == None: show = "*"
            if lock_open_img == (None,None,None):
                try:
                    self.__lock_open_img = trans_img(load_img("","eye"),25,self.res[1]) 
                except Exception:
                    self.__lock_open_img = pygame.Surface((25,self.res[1]),pygame.SRCALPHA)
            else:
                try:
                    self.__lock_open_img = trans_img(load_img(*lock_open_img),25,self.res[1]) 
                except Exception:
                    self.__lock_open_img = pygame.Surface((25,self.res[1]),pygame.SRCALPHA)

            if lock_img == (None,None,None):
                try:
                    self.__lock_img = trans_img(load_img("","eye_lock"),25,self.res[1])
                except Exception:
                    self.__lock_img = pygame.Surface((25,self.res[1]),pygame.SRCALPHA)
            else:
                try:
                    self.__lock_img = trans_img(load_img(*lock_img),25,self.res[1])
                except Exception:
                    self.__lock_img = pygame.Surface((25,self.res[1]),pygame.SRCALPHA)

            self.__lock_surface = pygame.Surface(self.__lock_img.get_rect().size,pygame.SRCALPHA)
            self.__lock_rect = self.__lock_surface.get_rect()
            self.__lock_rect.left,self.__lock_rect.top = self.__rect.right+self.__lock_rect.width/3,self.__rect.top
        self.__showtext = show
        if not self.__lock:
            self.__entrytext = self.text if self.__showtext == None else self.__showtext*len(self.text)
        else:
            self.__entrytext = self.text if self.showvalue else self.__showtext*len(self.text)

        if len(self.text)==0 and self.__lock: 
            self.__entrytext=self.text
        self.__text_surf=draw_text(self.__screen,self.__entrytext,self.__font,self.__size,self.textcl,(self.__rect.left+2,self.__rect.top+2),blit=False)
        self.__text_surf[1].centery = self.__rect.centery
        self.__cursor = pygame.Rect(self.__text_surf[1].right,self.__rect.top+2,1,self.__rect.height-6)

    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.__select:
            if self.__lock:
                if self.showvalue:
                    pygame.draw.rect(self.__lock_surface,(*self.activecl,self.dynamicalpha),self.__lock_surface.get_rect(),self.__depth,*self.__edge)
                    self.__screen.blit(self.__lock_surface,self.__lock_rect)
                    self.__screen.blit(self.__lock_open_img,self.__lock_rect)
                else:
                    pygame.draw.rect(self.__lock_surface,(*self.inactivecl,self.staticalpha),self.__lock_surface.get_rect(),self.__depth,*self.__edge)
                    self.__screen.blit(self.__lock_surface,self.__lock_rect)
                    self.__screen.blit(self.__lock_img,self.__lock_rect)

            self.__text_surf=draw_text(self.__screen,self.__entrytext,self.__font,self.__size,self.textcl if not self.__full_select else self.inactivecl,(self.__rect.left+2,self.__rect.top+2),blit=False)
            self.__text_surf[1].centery = self.__rect.centery

            if self.__text_surf[1].right < self.__rect.right-2:
                self.__size = self.__textsize 

            while self.__text_surf[1].right>=self.__rect.right-2 and self.__size>0:
                self.__size -= 1
                self.__text_surf=draw_text(self.__screen,self.__entrytext,self.__font,self.__size,self.textcl if not self.__full_select else self.inactivecl,(self.__rect.left+2,self.__rect.top+2),blit=False)
                self.__text_surf[1].centery = self.__rect.centery

            pygame.draw.rect(self.__surface,(*self.inactivecl,self.dynamicalpha),self.__surface.get_rect(),self.__depth,*self.__edge)
            self.__screen.blit(self.__surface,self.__rect)
            self.__cursor.left = self.__text_surf[1].right

            if self.__blink:
                if time.time()%1>0.5:
                    pygame.draw.rect(self.__screen,(*self.cursorcl,self.dynamicalpha),self.__cursor,1)
            else:
                pygame.draw.rect(self.__screen,(*self.cursorcl,self.dynamicalpha),self.__cursor,1)

            if self.__full_select:
                pygame.draw.rect(self.__screen,(*self.activecl,self.dynamicalpha),self.__text_surf[1],0,*self.__edge)

            self.__screen.blit(*self.__text_surf)


        else:
            if self.__rect.collidepoint(mouse):
                pygame.draw.rect(self.__surface,(*self.activecl,self.dynamicalpha),self.__surface.get_rect(),self.__depth,*self.__edge)
            else:
                pygame.draw.rect(self.__surface,(*self.inactivecl,self.staticalpha),self.__surface.get_rect(),self.__depth,*self.__edge)
            self.__screen.blit(self.__surface,self.__rect)
            self.__text_surf = draw_text(self.__screen,self.__entrytext,self.__font,self.__size,self.textcl,(self.__rect.left+2,self.__rect.top+2),blit=False)
            self.__text_surf[1].centery = self.__rect.centery
            self.__screen.blit(*self.__text_surf)
            if self.text == "":
                draw_text(self.__screen,self.msg,self.__font,self.__size,self.activecl if not self.__rect.collidepoint(mouse) else self.inactivecl,(self.__text_surf[1].left,self.__text_surf[1].top))
        return
    
    def inputevents(self,event):
        keys = pygame.key.get_pressed()
        
        if self.__select and keys[pygame.K_LCTRL] and keys[pygame.K_a] and not self.__full_select:
            self.__full_select = True

        none_selected = True
        for entry in Entry.entries:
            if entry.isselect(): none_selected = False;break

        if none_selected:
            pygame.key.set_repeat(0)
        else:
            pygame.key.set_repeat(400,100)    

        if self.__select and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.__full_select: 
                    self.text=""
                    self.__full_select = False
            elif event.key == pygame.K_RETURN:
                self.__select = self.__full_select = False
                if self.__lock: self.showvalue=False
            elif event.key == pygame.K_SPACE:
                if self.__type != "digit" and self.__type != "phone":
                    self.text += " "
            else: 
                if self.__type == "alnum":
                    if event.unicode.isalnum() or event.unicode in punc:
                        self.text += event.unicode
                        if self.__full_select: 
                            self.text = event.unicode
                            self.__full_select = False
                    else:
                        if self.__full_select and (not (keys[pygame.K_LCTRL] and keys[pygame.K_a])) and not(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not(keys[pygame.K_CAPSLOCK]):
                            self.__full_select = False
                elif self.__type == "digit":
                    if event.unicode.isdigit() or event.unicode in (".","-"):
                        if event.unicode == "." and "." in self.text:
                            return
                        if event.unicode == "-" and self.text=="":
                            self.text += event.unicode
                        else:
                            if event.unicode != "-":
                                self.text += event.unicode

                        if self.text == ".":
                            self.text="0."
                        elif self.text == "-.":
                            self.text = "-0."
                        if self.__full_select: 
                            self.text = event.unicode
                            self.__full_select = False
                        if self.text != "-":
                            if self.maxdigvalue!=None and float(self.text) > self.maxdigvalue:
                                self.text = str(self.maxdigvalue)
                            elif self.mindigvalue!=None and float(self.text)<self.mindigvalue:
                                self.text = str(self.mindigvalue)
                    else:
                        if self.__full_select and (not (keys[pygame.K_LCTRL] and keys[pygame.K_a])):
                            self.__full_select = False

                elif self.__type == "phone":
                    if event.unicode.isdigit() or event.unicode in ("+","-"):
                        self.text += event.unicode
                        if self.__full_select: 
                            self.text = event.unicode
                            self.__full_select = False
                    else:
                        if self.__full_select and (not (keys[pygame.K_LCTRL] and keys[pygame.K_a])) and not(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                            self.__full_select = False
         
                elif self.__type == "alpha":
                    if event.unicode.isalpha() or event.unicode == " ":
                        self.text += event.unicode
                        if self.__full_select: 
                            self.text = event.unicode
                            self.__full_select = False
                    else:
                        if self.__full_select and (not (keys[pygame.K_LCTRL] and keys[pygame.K_a])) and not(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not(keys[pygame.K_CAPSLOCK]):
                            self.__full_select = False
 
                else:
                    if self.__full_select and (not (keys[pygame.K_LCTRL] and keys[pygame.K_a])) and not(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not(keys[pygame.K_CAPSLOCK]): 
                        self.__full_select = False


            if len(self.text)>self.__limit:
                self.text = self.text[:self.__limit]
            self.__entrytext = self.text if self.__showtext == None and not self.__lock else self.__showtext*len(self.text)

            if self.__lock:
                self.__entrytext = self.text if self.showvalue else self.__showtext*len(self.text)    

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.__select:
                    if self.__lock:
                        if self.__lock_rect.collidepoint(event.pos) and not self.showvalue:
                            self.showvalue = True
                            self.__entrytext = self.text    
                        elif self.__lock_rect.collidepoint(event.pos) and self.showvalue: 
                            self.showvalue = False
                            self.__entrytext = self.__showtext*len(self.text)

                        else:
                            if not self.__rect.collidepoint(event.pos) and not self.__lock_rect.collidepoint(event.pos):
                                self.__select = self.showvalue = self.__full_select = False
                                self.__entrytext = self.text if self.showvalue else self.__showtext*len(self.text)
                    else:
                        if not self.__rect.collidepoint(event.pos): 
                            self.__select = self.__full_select = False

                else:
                    if self.__rect.collidepoint(event.pos): 
                        self.__select = True


    def isselect(self): return self.__select    

    def pos(self): return self.__pos

    @classmethod
    def update_all(cls):
        for entry in cls.entries:
            entry.update()

    @classmethod
    def update_from_to(cls,start=1,end=-1):
        if end == -1: end = len(cls.entries)
        if not isinstance(start,int):
            raise TypeError("Expected position of Entry but got %s"%(start))
        if not isinstance(end,int):
            raise TypeError("Expected position of Entry but got %s"%(end))
        if start>end:
            raise ValueError("Start Value should be less than End Value")
        for pos in range(start-1,end):
            cls.entries[pos].update()



    @classmethod
    def inputevents_forall(cls,event):
        for entries in cls.entries:
            entries.inputevents(event)

