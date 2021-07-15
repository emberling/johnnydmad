;--------------------------------------------------------
; mPlayerData (needed for all 3 implementations)        |
; by madsiur (themadsiur@gmail.com)                     |
; version 1.3.2                                         |
; Released on 03/17/2017                                |
;-------------------------------------------------------- 

org $F06000

;------------------------------------
; Song Names                        |
;------------------------------------
MUSIC_NAMES:
MUSICNAME_01h:  db "pre:                      ",$00
MUSICNAME_02h:  db "Omen I                    ",$00
MUSICNAME_03h:  db "Omen II                   ",$00
MUSICNAME_04h:  db "open:                     ",$00
MUSICNAME_05h:  db "awake:                    ",$00
MUSICNAME_06h:  db "wob:                      ",$00
MUSICNAME_07h:  db "shadow:                   ",$00
MUSICNAME_08h:  db "strago:                   ",$00
MUSICNAME_09h:  db "gau:                      ",$00
MUSICNAME_0Ah:  db "figaro:                   ",$00
MUSICNAME_0Bh:  db "coin:                     ",$00
MUSICNAME_0Ch:  db "cyan:                     ",$00
MUSICNAME_0Dh:  db "locke:                    ",$00
MUSICNAME_0Eh:  db "rachel:                   ",$00
MUSICNAME_0Fh:  db "relm:                     ",$00
MUSICNAME_10h:  db "setzer:                   ",$00
MUSICNAME_11h:  db "daryl:                    ",$00
MUSICNAME_12h:  db "celes:                    ",$00
MUSICNAME_13h:  db "choco:                    ",$00
MUSICNAME_14h:  db "boss:                     ",$00
MUSICNAME_15h:  db "bar:                      ",$00
MUSICNAME_16h:  db "kefka:                    ",$00
MUSICNAME_17h:  db "narshe:                   ",$00
MUSICNAME_18h:  db "cave:                     ",$00
MUSICNAME_19h:  db "veldt:                    ",$00
MUSICNAME_1Ah:  db "protec:                   ",$00
MUSICNAME_1Bh:  db "empire:                   ",$00
MUSICNAME_1Ch:  db "troops:                   ",$00
MUSICNAME_1Dh:  db "etown:                    ",$00
MUSICNAME_1Eh:  db "SFX: Waterfall            ",$00
MUSICNAME_1Fh:  db "hurry:                    ",$00
MUSICNAME_20h:  db "train:                    ",$00
MUSICNAME_21h:  db "esper:                    ",$00
MUSICNAME_22h:  db "ultros:                   ",$00
MUSICNAME_23h:  db "koltz:                    ",$00
MUSICNAME_24h:  db "battle:                   ",$00
MUSICNAME_25h:  db "Unused Fanfare            ",$00
MUSICNAME_26h:  db "The Wedding Waltz I       ",$00
MUSICNAME_27h:  db "Aria di Mezzo Carattere   ",$00
MUSICNAME_28h:  db "trench:                   ",$00
MUSICNAME_29h:  db "zozo:                     ",$00
MUSICNAME_2Ah:  db "town:                     ",$00
MUSICNAME_2Bh:  db "what:                     ",$00
MUSICNAME_2Ch:  db "SFX: Crowd Noise          ",$00
MUSICNAME_2Dh:  db "gogo:                     ",$00
MUSICNAME_2Eh:  db "banon:                    ",$00
MUSICNAME_2Fh:  db "vict:                     ",$00
MUSICNAME_30h:  db "umaro:                    ",$00
MUSICNAME_31h:  db "mog:                      ",$00
MUSICNAME_32h:  db "danger:                   ",$00
MUSICNAME_33h:  db "boss2:                    ",$00
MUSICNAME_34h:  db "rtown:                    ",$00
MUSICNAME_35h:  db "flight:                   ",$00
MUSICNAME_36h:  db "doom:                     ",$00
MUSICNAME_37h:  db "owzer:                    ",$00
MUSICNAME_38h:  db "sleep:                    ",$00
MUSICNAME_39h:  db "SFX: Wind                 ",$00
MUSICNAME_3Ah:  db "SFX: Waves                ",$00
MUSICNAME_3Bh:  db "dmad1:                    ",$00
MUSICNAME_3Ch:  db "SFX: Train Stopping       ",$00
MUSICNAME_3Dh:  db "rag:                      ",$00
MUSICNAME_3Eh:  db "rip:                      ",$00
MUSICNAME_3Fh:  db "SFX: Chocobos Running     ",$00
MUSICNAME_40h:  db "SFX: Waterfall 2          ",$00
MUSICNAME_41h:  db "Overture I                ",$00
MUSICNAME_42h:  db "Overture II               ",$00
MUSICNAME_43h:  db "Overture III              ",$00
MUSICNAME_44h:  db "The Wedding Waltz II      ",$00
MUSICNAME_45h:  db "The Wedding Waltz III     ",$00
MUSICNAME_46h:  db "The Wedding Waltz IV      ",$00
MUSICNAME_47h:  db "mtek:                     ",$00
MUSICNAME_48h:  db "SFX: New Continent        ",$00
MUSICNAME_49h:  db "SFX: Crane Activation     ",$00
MUSICNAME_4Ah:  db "SFX: Fire                 ",$00
MUSICNAME_4Bh:  db "fc:                       ",$00
MUSICNAME_4Ch:  db "falcon:                   ",$00
MUSICNAME_4Dh:  db "cult:                     ",$00
MUSICNAME_4Eh:  db "ktower:                   ",$00
MUSICNAME_4Fh:  db "wor:                      ",$00
MUSICNAME_50h:  db "final:                    ",$00
MUSICNAME_51h:  db "forest:                   ",$00
MUSICNAME_52h:  db "Dancing Mad II            ",$00
MUSICNAME_53h:  db "Balance Is Restored I     ",$00
MUSICNAME_54h:  db "Balance Is Restored II    ",$00
MUSICNAME_55h:  db "tomb:                     ",$00
MUSICNAME_56h:  db "dream:                    ",$00
MUSICNAME_57h:  db "odin:                     ",$00
MUSICNAME_58h:  db "fenix:                    ",$00
MUSICNAME_59h:  db "gate:                     ",$00
MUSICNAME_5Ah:  db "mtzozo:                   ",$00
MUSICNAME_5Bh:  db "engine:                   ",$00
MUSICNAME_5Ch:  db "town2:                    ",$00
MUSICNAME_5Dh:  db "intro:                    ",$00
MUSICNAME_5Eh:  db "bat2:                     ",$00
MUSICNAME_5Fh:  db "bat3:                     ",$00
MUSICNAME_60h:  db "bat4:                     ",$00
MUSICNAME_61h:  db "mboss:                    ",$00

;------------------------------------
; Song Names Pointers               |
;------------------------------------
FILEPOS_MUSICNAME_ADDR:
    dw MUSICNAME_01h
    dw MUSICNAME_02h
    dw MUSICNAME_03h
    dw MUSICNAME_04h
    dw MUSICNAME_05h
    dw MUSICNAME_06h
    dw MUSICNAME_07h
    dw MUSICNAME_08h
    dw MUSICNAME_09h
    dw MUSICNAME_0Ah
    dw MUSICNAME_0Bh
    dw MUSICNAME_0Ch
    dw MUSICNAME_0Dh
    dw MUSICNAME_0Eh
    dw MUSICNAME_0Fh
    dw MUSICNAME_10h
    dw MUSICNAME_11h
    dw MUSICNAME_12h
    dw MUSICNAME_13h
    dw MUSICNAME_14h
    dw MUSICNAME_15h
    dw MUSICNAME_16h
    dw MUSICNAME_17h
    dw MUSICNAME_18h
    dw MUSICNAME_19h
    dw MUSICNAME_1Ah
    dw MUSICNAME_1Bh
    dw MUSICNAME_1Ch
    dw MUSICNAME_1Dh
    dw MUSICNAME_1Eh
    dw MUSICNAME_1Fh
    dw MUSICNAME_20h
    dw MUSICNAME_21h
    dw MUSICNAME_22h
    dw MUSICNAME_23h
    dw MUSICNAME_24h
    dw MUSICNAME_25h
    dw MUSICNAME_26h
    dw MUSICNAME_27h
    dw MUSICNAME_28h
    dw MUSICNAME_29h
    dw MUSICNAME_2Ah
    dw MUSICNAME_2Bh
    dw MUSICNAME_2Ch
    dw MUSICNAME_2Dh
    dw MUSICNAME_2Eh
    dw MUSICNAME_2Fh
    dw MUSICNAME_30h
    dw MUSICNAME_31h
    dw MUSICNAME_32h
    dw MUSICNAME_33h
    dw MUSICNAME_34h
    dw MUSICNAME_35h
    dw MUSICNAME_36h
    dw MUSICNAME_37h
    dw MUSICNAME_38h
    dw MUSICNAME_39h
    dw MUSICNAME_3Ah
    dw MUSICNAME_3Bh
    dw MUSICNAME_3Ch
    dw MUSICNAME_3Dh
    dw MUSICNAME_3Eh
    dw MUSICNAME_3Fh
    dw MUSICNAME_40h
    dw MUSICNAME_41h
    dw MUSICNAME_42h
    dw MUSICNAME_43h
    dw MUSICNAME_44h
    dw MUSICNAME_45h
    dw MUSICNAME_46h
    dw MUSICNAME_47h
    dw MUSICNAME_48h
    dw MUSICNAME_49h
    dw MUSICNAME_4Ah
    dw MUSICNAME_4Bh
    dw MUSICNAME_4Ch
    dw MUSICNAME_4Dh
    dw MUSICNAME_4Eh
    dw MUSICNAME_4Fh
    dw MUSICNAME_50h
    dw MUSICNAME_51h
    dw MUSICNAME_52h
    dw MUSICNAME_53h
    dw MUSICNAME_54h
    dw MUSICNAME_55h
    dw MUSICNAME_56h
    dw MUSICNAME_57h
    dw MUSICNAME_58h
    dw MUSICNAME_59h
    dw MUSICNAME_5Ah
    dw MUSICNAME_5Bh
    dw MUSICNAME_5Ch
    dw MUSICNAME_5Dh
    dw MUSICNAME_5Eh
    dw MUSICNAME_5Fh
    dw MUSICNAME_60h
    dw MUSICNAME_61h

;------------------------------------
; Music Player song list            |
;------------------------------------
FILEPOS_MUSIC_LIST:
    db $01,$04,$5D,$21,$05,$17,$1B,$0D,$0A,$0B
    db $16,$18,$06,$2A,$07,$13,$5C,$23,$32,$2E
    db $2B,$1C,$0C,$51,$20,$09,$19,$28,$1D,$1A
    db $0E,$29,$3D,$10,$35,$15,$47,$59,$1F,$31
    db $12,$08,$0F,$4B,$36,$4F,$34,$5B,$55,$11
    db $4C,$5A,$37,$30,$2D,$56,$57,$58,$4D,$4E
    db $24,$5E,$5F,$60,$61,$14,$22,$33,$3B,$50
    db $2F,$38,$3E,$02,$03,$41,$42,$43,$27,$26
    db $44,$45,$46,$52,$53,$54,$25,$1E,$2C,$39
    db $3A,$3C,$3F,$40,$48,$49,$4A,$00
    
;    db $02,$03,$04,$17,$05,$0D,$24,$2F,$0A,$16
;    db $23,$2E,$07,$1C,$0C,$32,$18,$20,$3C,$19
;    db $09,$28,$2A,$1D,$12,$1A,$14,$1F,$06,$0B
;    db $13,$0E,$29,$3D,$41,$42,$43,$27,$26,$44
;    db $45,$46,$22,$10,$15,$1B,$47,$35,$2B,$31
;    db $08,$0F,$21,$4B,$36,$33,$3E,$4F,$34,$4C
;    db $2D,$11,$37,$30,$4D,$4E,$3B,$52,$50,$53
;    db $54,$01,$38,$25,$3A,$1E,$2C,$39,$3F
;    db $40,$48,$49,$4A,$00 