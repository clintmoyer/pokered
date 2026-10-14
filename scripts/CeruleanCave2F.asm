CeruleanCave2F_Script:
	call EnableAutoTextBoxDrawing
	ld hl, CeruleanCave2FTrainerHeaders
	ld de, CeruleanCave2F_ScriptPointers
	ld a, [wCeruleanCave2FCurScript]
	call ExecuteCurMapScriptInTable
	ld [wCeruleanCave2FCurScript], a
	ret

CeruleanCave2F_ScriptPointers:
	def_script_pointers
	dw_const CheckFightingMapTrainers,              SCRIPT_CERULEANCAVE2F_DEFAULT
	dw_const DisplayEnemyTrainerTextAndStartBattle, SCRIPT_CERULEANCAVE2F_START_BATTLE
	dw_const EndTrainerBattle,                      SCRIPT_CERULEANCAVE2F_END_BATTLE

CeruleanCave2F_TextPointers:
	def_text_pointers
	dw_const PickUpItemText,             TEXT_CERULEANCAVE2F_PP_UP
	dw_const PickUpItemText,             TEXT_CERULEANCAVE2F_ULTRA_BALL
	dw_const PickUpItemText,             TEXT_CERULEANCAVE2F_FULL_RESTORE
	dw_const CeruleanCave2FMudimythText, TEXT_CERULEANCAVE2F_MUDIMYTH

CeruleanCave2FTrainerHeaders:
	def_trainers 4
MudimythTrainerHeader:
	trainer EVENT_BEAT_MUDIMYTH, 0, MudimythBattleText, MudimythBattleText, MudimythBattleText
	db -1 ; end

CeruleanCave2FMudimythText:
	text_asm
	ld hl, MudimythTrainerHeader
	call TalkToTrainer
	jp TextScriptEnd

MudimythBattleText:
	text "Yip! Yip!@"
	text_asm
	ld a, MUDIMYTH
	call PlayCry
	call WaitForSoundToFinish
	jp TextScriptEnd
