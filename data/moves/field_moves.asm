FieldMoveDisplayData:
	; move id, FieldMoveNames index, leftmost tile
	; (leftmost tile = -1 + tile column in which the first
	;  letter of the move's name should be displayed)
	db CUT,        1, $06
	db FLY,        2, $0A
	db ANIM_B4,    3, $0C ; unused
	db SURF,       4, $08
	db STRENGTH,   5, $0C
	db FLASH,      6, $07
	db DIG,        7, $07
	db TELEPORT,   8, $09
	db SOFTBOILED, 9, $07
	db -1 ; end
