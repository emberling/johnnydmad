;--------------------------------------------------------
; soundResume (needed for all 3 implementations)        |
; by madsiur (themadsiur@gmail.com)                     |
; version 1.0                                           |
; Released on 03/10/2017                                |
;-------------------------------------------------------- 

org $C5061F
PHP
SEP #$20
LDA $00         
CMP #$14
BCS .resume_enable

LDA $05         
BEQ .resume_disable

LDX #$FFFF

.compare_list
INX
LDA $C506F9,X  
BMI .resume_disable

CMP $01         
BNE .compare_list

.resume_enable
LDA #$04        
TSB $00       

.resume_disable
PLP
RTS
