; unique moves for gym leaders
; this is not automatic! you have to write the index you want to [wLoneAttackNo]
; first. e.g., erika's script writes 4 to [wLoneAttackNo] to get mega drain,
; the fourth entry in the list.
LoneMoves:
	; pokemon index, move to give nth pokemon
	db 1, BIDE
	db 1, BUBBLEBEAM
	db 2, THUNDERBOLT
	db 2, MEGA_DRAIN
	db 3, TOXIC
	db 3, PSYWAVE
	db 3, FIRE_BLAST
	db 4, FISSURE

; League aces: trainer class, fourth move for the fifth dog.
TeamMoves:
	db LORELEI, WHITEOUT_YIP
	db BRUNO, SKY_PAW
	db AGATHA, VENOM_MARK
	db LANCE, WYRM_BARK
	db -1 ; end
