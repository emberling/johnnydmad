;--------------------------------------------------------
; mPlayerCore (needed for all 3 implementations)        |
; by madsiur (themadsiur@gmail.com)                     |
; version 1.3.2                                         |
; Released on 03/17/2017                                |
;--------------------------------------------------------  

;----------------------------------------
; Map Song Saving                       |
;----------------------------------------
SaveSong:           ; Save field song ID when entering main menu
LDA #$04            ; Main menu init ID
STA $26             ; Save as current menu
LDA $1F80	        ; Load current song
STA $D2             ; Save in temporary RAM (unused)
LDA $1302           ; Load current volume
STA $D3             ; Save in temporary RAM (unused)
RTS

;----------------------------------------
; Map Song Resume                       |
;----------------------------------------
RestoreSong:        ; Restore last field song when exiting main menu
LDA $D2             ; Map song ID
STA $1301           ; Set Song
LDA #$10            ; SPC Command
STA $1300
LDA $D3             ; Map song Volume
STA $1302           ; Set Volume
JSL $C50004         ; Play Song
LDA #$FF
STA $27             ; Exit Menu
RTS

;----------------------------------------
; Music Player Init (menu action $7B)   |
;----------------------------------------
InitMusic:
JSR $352F                       ; Reset/Stop stuff
JSR $6904                       ; Reset BGs' X/Y
LDA #$01                        ; 64x32 at $0000
STA $2107                       ; Set BG1 map loc
LDA #$02                        ; Main cursor: On
STA $46                         ; Bar/Blinker: Off
STZ $4A                         ; List scroll: 0
STZ $49                         ; Top BG1 WR row: 0
LDA #$FF        
STA $5F                         ; Set return row ???
JSR MUSIC_SET_CURSOR_SETTINGS   ; Set cursor navigation data
JSR MUSIC_SET_CURSOR_POSITIONS  ; Relocate cursor
JSR $07B0                       ; Queue cursor OAM
JSR MUSIC_DISPLAY_MENU          ; Draw text and menu
JSR MUSIC_SET_SCROLLBAR         ; Set scrollbar height
NOP
NOP
NOP
JSR MUSIC_SET_HDMA
LDA #$7C                        ; Music Player Loop     
STA $27                         ; Queue action
LDA #$01                        ; C3/1D7E
STA $26                         ; Next: Fade-in
JMP $3541                       ; BRT:1 + NMI

;----------------------------------------
; Music Player Loop (menu action $7C)   |
;----------------------------------------
LoopMusic:
JSR $0EFD                       ; Queue list upload
JSR MUSIC_STATE_CONTROL         ; Check special songs like Phantom Train and Dancing Mad
JSR MUSIC_UPDATE_CURSOR         ; Update cursor
LDA $08                         ; No-autofire keys
BIT #$80                        ; Pushing A?
BEQ .check_b                    ; Branch if not

TDC                             ; Clear Accumulator
LDA $4B                         ; Load cursor slot 
TAX                             ; Index it
LDA $7E9D89,X                   ; Load song ID in slot?
JMP MUSIC_PLAY                  ; Play song

.check_b
LDA $09                         ; No-autofire keys
BIT #$80                        ; Pushing B?
BEQ .ret                        ; Branch if not

JSR ReturnToMenu                ; Return to Config / Main menu
.ret
RTS

MUSIC_SET_CURSOR_SETTINGS:      ; From function InitMusic
LDY #CURSOR_SETTINGS_MUSIC      ; Navigation data offset
JMP $05FE                       ; Load navig data     

MUSIC_UPDATE_CURSOR:            ; From function LoopMusic
JSR MUSIC_SELECT                ; Perform cursor logic

MUSIC_SET_CURSOR_POSITIONS:     ; From function InitMusic   
LDY #CURSOR_POSITIONS_MUSIC     ; Navigation data offset
JMP $0648                       ; Relocate cursor

CURSOR_SETTINGS_MUSIC:
db $01          
db $00          
db $00         
db $01                  
db MUSICPLAYER_NUM_ROWS

CURSOR_POSITIONS_MUSIC:
db $08,$34
db $08,$40
db $08,$4C
db $08,$58
db $08,$64
db $08,$70
db $08,$7C
db $08,$88
db $08,$94
db $08,$A0
db $08,$AC
db $08,$B8
db $08,$C4
db $00

CHAR_MUSIC_PLAYER:
dw $7915                      
db "BEYOND"
db $FE
db "CHAOS"
db $FE
db "JUKEBOX"    

MUSIC_BG1_VERTICAL:
db $27,$00,$00
db $08,$00,$00
db $0C,$D4,$FF
db $0C,$D8,$FF
db $0C,$DC,$FF
db $0C,$E0,$FF
db $0C,$E4,$FF
db $0C,$E8,$FF
db $0C,$EC,$FF
db $0C,$F0,$FF
db $0C,$F4,$FF
db $0C,$F8,$FF
db $0C,$FC,$FF
db $0C,$00,$00
db $0C,$04,$00
db $00

MUSIC_BG1_HORIZONTAL:
db $2F,$00,$01
db $50,$00,$00
db $50,$00,$00
db $10,$00,$01
db $00

BOX_MUSIC_PLAYER:
dw $588B        ; dest
db $1C,$02      ; width, height

BOX_MUSIC_LIST:
dw $598B        ; dest
db $1C,$14      ; width, height

MUSIC_SET_HDMA:
LDA #$02                        ; 1Rx2B to PPU
STA $4350                       ; Set DMA mode
LDA #$0D                        ; $210D
STA $4351      
LDY #MUSIC_BG1_HORIZONTAL       ; HDMA scrolling data offset
STY $4352    
LDA #$C3
STA $4354   
LDA #$C3
STA $4357    
LDA #$20
TSB $43      
LDA #$02
STA $4360  
LDA #$0E       
STA $4361     
LDY #MUSIC_BG1_VERTICAL         ; HDMA data offset
STY $4362     
LDA #$C3
STA $4364 
LDA #$C3
STA $4367     
LDA #$40
TSB $43       
RTS

MUSIC_DISPLAY_MENU:                     ; From function InitMusic
LDY #BOX_MUSIC_PLAYER                   ; Menu data offset
JSR $0341                               ; Draw menu window
LDY #BOX_MUSIC_LIST                     ; Menu data offset
JSR $0341                               ; Draw menu window
JSR $0E52                               ; Upload BG2 A+B
JSR $6A15                               ; Clear BG1 map A
JSR $6A19                               ; Clear BG1 map B
JSR $6A3C                               ; Clear BG3 map A
LDA #$2C                                ; Palette 3
STA $29                                 ; Color: Blue
LDY #CHAR_MUSIC_PLAYER                  ; Window title
JSR $02F9                               ; Draw window title
LDA #$20                                ; Palette 0
STA $29                                 ; Color: User's         
LDX $00                                 ; Clear Index

.load_music_list
LDA FILEPOS_MUSIC_LIST,X                ; Load song ID from playlist
BEQ .break                              ; Branch if silence (End)

STA $7E9D89,X                           ; Store as song ID in slot
INX                                     ; increment index
BRA .load_music_list                    ; Branch until end (00)

.break
TXA                                     ; Load number of songs in A
SEC
SBC.b #MUSICPLAYER_NUM_ROWS             ; minus 14
BCS .allow_scroll                       ; Allow scroll if more than 14 songs in playlist

TDC                                     ; Clear Accumulator

.allow_scroll
STA $5C                                 ; Store song numbers as scroll limit
LDA.b #MUSICPLAYER_NUM_ROWS             ; Load number of rows on screen
STA $5A                                 ; Set as number of rows per page
LDA #$01
STA $5B                                 ; 1 col per page
JSR UPDATE_MUSIC_LIST                   ; Update list
JSR $0E28                               ; Upload BG1 A+B
JMP $0E6E                               ; Upload BG3 A+B

MUSIC_SET_SCROLLBAR:                    ; From function InitMusic
JSR $091F                               ; Create scrollbar
LDY #$9000
STY $4204                               ; Set dividend
LDA $5C         
STA $4206                               ; Set divisor
NOP
NOP
NOP
NOP
NOP
REP #$20
LDA $4214                               ; Load result in A                
STA $7E354A,X                           ; Set as V-Speed
LDA #$002E                              ; Y: 46
STA $7E34CA,X                           ; Set scrollbar's
SEP #$20                                ; 8-Bit Accumulator
RTS

UPDATE_MUSIC_LIST:
JSR $6A15                               ; Clear BG1 map A
JSR $83F7                               ; Define $E5, $E6
LDY #MUSICPLAYER_NUM_ROWS

.begin
PHY                                     ; Save number of row per page
TDC                                     ; Clear Accumulator
LDA $E5
TAX
LDA $7E9D89,X                           ; Load song ID in slot
PHA                                     ; Save song ID
LDX #$0003
LDA $E6                                 ; BG1 write row
JSR $809F                               ; Compute map ptr
TDC                                     ; Clear Accumulator
PLA                                     ; Restore song ID
JSR GET_MUSICNAME                       ; Get song name
INC $E5
LDA $E6
INC
INC
AND #$1F
STA $E6
PLY
DEY
BNE .begin
RTS

MUSIC_SELECT:
LDA $0B                         ; Semi-auto keys
BIT #$0A                        ; Pushing Up or Left
BEQ .check_down                 ; If not check push Down or Right

LDA $4E                         ; Cursor row
BNE .cursor_up

LDA $4A                         ; Scroll position
BEQ .ret

DEC $50                         ; List row -1
DEC $4A                         ; Scroll pos -1
BRA .redraw_list                ; Update list

.cursor_up
DEC $50                         ; Scroll pos -1
DEC $4E                         ; Move cursor up
RTS

.check_down
BIT #$05                        ; Pushing Right or Down
BEQ .check_lr                   ; If not, check L or R push

LDA $54                         ; Load bottom menu row
DEC                             ; Bottom menu row - 1
CMP $4E                         ; Compare to cursor row
BNE .cursor_down                ; Branch if we can move down

LDA $4A                         ; Load scroll position
CMP $5C                         ; Compare to scroll limit
BEQ .ret                        ; Branch if limit reached

INC $50                         ; List row +1
INC $4A                         ; Scroll position + 1
BRA .redraw_list                ; Update list

.cursor_down
INC $50                         ; List row +1
INC $4E                         ; Move cursor down

.ret
RTS

.check_lr
LDA $0A                         ; Semi-auto keys
BIT #$30                        ; Pushing L or R
BEQ .ret                        ; Exit if not

BIT #$20                        ; Pushing L
BEQ .input_r                    ; We are pushing R

.input_l
LDA $4A                         ; Load scroll position

CMP $5A                         ; Compare to number of rows per page
BCC .is_low

LDA $5A                         ; Load number of rows per page

.is_low
STA $E0                         ; Store in temp RAM
LDA $4A                         ; Load scroll position
SEC
SBC $E0                         ; One page up?
STA $4A                         ; Store as new scroll position
LDA $50                         ; List row
SEC
SBC $E0                         ; One page up?
STA $50                         ; Store as list row
BRA .redraw_list                ; Update list

.input_r
LDA $5C                         ; Load scroll limit
SEC
SBC $4A                         ; Subtract scroll position
BEQ .cursor_bottom
CMP $5A                         ; Compare to number of rows per page
BCC .not_max
LDA $5A                         ; Load number of rows per page
.not_max
STA $E0                         ; Store in temp RAM
LDA $4A                         ; Load scroll position
CLC
ADC $E0                         ; One page down?
STA $4A                         ; Store as new scroll position
LDA $50                         ; List row
CLC
ADC $E0                         ; One page down?
STA $50                         ; Store as list row
.redraw_list
JMP UPDATE_MUSIC_LIST           ; Update list

.cursor_bottom
LDA $54                         ; Load cursor limit
DEC                             ; Cursor limit - 1
STA $4E                         ; Set as cursor row
CLC
ADC $4A                         ; Add scroll position
STA $50                         ; Store as list row
RTS

MUSIC_STATE_CONTROL:            ; From function LoopMusic
LDA $1305                       ; Load current song ID
CMP #$20                        ; Check if Phantom Train
BNE .check_dancing_mad          ; Branch if not
LDA $5F                         ; Load former cursor row?      
BEQ MUSIC_NEXT                  
RTS

.check_dancing_mad
CMP #$3B                        ; Check if Dancing Mad 1
BNE .ret                        ; Exit if not
LDA $5F                         ; Load former cursor row? 
BEQ .dancing_mad_1st
DEC                             ; Decrement former cursor row?
BNE .ret
LDY #$41D0                      ; Load Dancing Mad 2 song length?   
BRA .check_elapse

.dancing_mad_1st
LDY #$1940                      ; Load Dancing Mad 1 song length?  
.check_elapse
CPY $CF                         ; Set timer
BCC MUSIC_NEXT                  ; Play song
.ret
RTS

MUSIC_NEXT:
LDA #$89       
STA $1300     
JSL $C50004                     ; Play song
INC $5F                         ; Increment return row?
RTS

MUSIC_PLAY:
STA $1301     
LDA #$10       
STA $1300     
LDA #$FF
STA $1302       
STZ $1305      
JSL $C50004    
LDY $00
STY $CF         
STZ $5F        
RTS

GET_MUSICNAME:
LDY #$9E8B      
STY $2181       
REP #$21
PHA
TXA
ADC #$0040     
STA $7E9E89     
PLA
DEC
ASL
TAX
LDA FILEPOS_MUSICNAME_ADDR,X
TAX
SEP #$20
DEX

.transfer_name
INX
LDA $F00000,X           ;load letter. Since pointers are bank relative
                        ;no need to use the MUSIC_NAMES label defined in mplayerdata.asm.
                        ;Do not forget to change the LDA bank if mplayerdata.asm is outside bank $C3.
STA $2180      
BNE .transfer_name

LDY #$9E89   
STY $E7
LDA #$7E        
STA $E9
JMP $02FF    