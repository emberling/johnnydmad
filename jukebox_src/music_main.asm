;--------------------------------------------------------
; Main Menu Music Player                                |
; by madsiur (themadsiur@gmail.com)                     |
; version 1.3.2                                         |
; Released on 03/17/2017                                |
;--------------------------------------------------------    

hirom       ;Do not touch
;header     ;uncomment if you have a header

table menu.tbl,rtl              ;Menu Table file
MUSICPLAYER_NUM_ROWS equ $000D  ;Music player number of rows

;------------------------------------
; Current field song preservation   |
;------------------------------------
org $C3011A             ;In invoke main menu
JSR SaveSong            ;Save current song ID
JMP $01BA               ;Enter menu loop

org $C31DCB             ;When pressing B to exit main menu
JSR RestoreSong         ;Set last field song as current song
STZ $26                 ;Fade out
RTS

;------------------------------------   
; Music menu option code (Main)     |
;------------------------------------
org $C302D1
dw InitMusic        ;Menu action #$7B (init music player)
dw LoopMusic        ;Menu action #$7C (scrolling loop)

org $C33741         ;In text pointers for main menu
dw LvlString        ;"LV" text pointer

org $C3376F         ;In text pointers for main menu
dw MusicString      ;"Music" text pointer

org $C33804         ;In positioned text for main menu
dw $7D77            ;"Time" text position

org $C3380F         ;In positioned text for main menu    
dw $7DF7            ;"Steps" text position

org $C3380B         ;In positioned text for main menu  
dw $7DBF            ;":" text position

org $C337FD         ;In Positioned text for main menu   
SaveString:
dw $7CB9            ;"Save" text new position

org $C32F89         ;In navigation data for main menu
db $08              ;New number of menu options

org $C32F65         ;In Mode 0: Initialize data
LDY #CursorTable    ;Cursor positions table offset

org $C32F76         ;In Mode 1: Update position
LDY #CursorTable    ;Cursor positions table offset

org $C331BB         ;In Window layout for main menu
dd $0F0658B7        ;08x17 at $58B7 (Options)
dd $00000000        ;Time Window is not used anymore
dd $06075D35        ;09x08 at $5D35 (Steps)

org $C3329F         ;In Draw time
LDX #$7DBB          ;Hours number position

org $C332AB         ;In Draw time
LDX #$7DC1          ;Minutes number position

org $C33252         ;In Draw most text in small windows of main menu 
LDX #$7E37          ;Steps number position

org $C33175         ;In Draw elements shared by main menu
BRA noDraw          ;Skip time window drawing
org $C3317B
noDraw:

org $C3321A         ;In Draw list of submenus in main menu
JSR DrawMusic
JSR $02F9           ;Draw "Music"
RTS

org $C32E69             ;In Handle selection in main menu list
JMP (ChoicesTable,X)    ;Menu choices jump table

org $C336AD         ;In Set to condense BG3 text in main menu
LDY #ShiftTable     ;Text shifting table

org $C3FA00         ;Free $C3 bank space used for rest of code

;------------------------------------
; Relocated and expanded tables     |
;------------------------------------
CursorTable:
dw $12AF            ;Item
dw $21AF            ;Skills
dw $30AF            ;Equip
dw $3FAF            ;Relic
dw $4EAF            ;Status
dw $5DAF            ;Config
dw $6CAF            ;Music
dw $7BAF            ;Save

ChoicesTable:       ;Jump table for menu choices
dw $2E86            ;Item
dw $2E90            ;Skills
dw $2E90            ;Equip
dw $2E90            ;Relic  
dw $2E90            ;Status
dw $2E7A            ;Config
dw BgmOption        ;Music (new entry)
dw $2EAA            ;Save

ShiftTable:
dl $00000F          ;Nothing
dl $00030F          ;Item
dl $00040F          ;Skills
dl $00050F          ;Equip
dl $00060F          ;Relic
dl $00070F          ;Status
dl $00080F          ;Config
dl $00090F          ;Music
dl $000A0F          ;Save
dl $000807          ;Nothing
dl $000807          ;Nothing
dl $000018          ;The rest
db $00              ;End

;------------------------------------
; Relocated and new Strings         |
;------------------------------------
LvlString:
dw $399D            ;"LV" position
db $8B,$95,$00      ;"LV"

MusicString:
dw $7C39            ;"Music" position
db $8C,$AE,$AC      ;"Music"
db $A2,$9C,$00    

;------------------------------------
; Hook ups and functions            |
;------------------------------------
DrawMusic:
LDY #SaveString     ;Text pointer
JSR $02F9           ;draw "Save"
LDA #$20            ;Palette 0
STA $29             ;Color: User's
LDY #MusicString    ;Text pointer
RTS

BgmOption:          ;Music player option pressed
JSR $0EB2           ;Click sound
LDA #$7B            ;Queue init music player
STA $27             ;Queue music menu
STZ $26             ;Fade-out
RTS

ReturnToMenu:       ;When pressing B in music player (called from mplayercore.asm)
JSR $0EB2           ;Click sound
LDA #$04            ;Main Initialization ID
STA $27             ;Queue Main init
STZ $26             ;Fade out
RTS
;------------------------------------
; External code                     |
;------------------------------------
incsrc mplayercore.asm  ;Music player       (need to remain in bank $C3)
incsrc mplayerdata.asm  ;Music player data  (could be moved outside bank $C3)
incsrc soundresume.asm  ;SPC code changes   (bank $C5)






