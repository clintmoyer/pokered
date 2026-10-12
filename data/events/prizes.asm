PrizeDifferentMenuPtrs:
	dw PrizeMenuMon1Entries, PrizeMenuMon1Cost
	dw PrizeMenuMon2Entries, PrizeMenuMon2Cost
	dw PrizeMenuTMsEntries,  PrizeMenuTMsCost

NoThanksText:
	db "NO THANKS@"

PrizeMenuMon1Entries:
	db POODPUP
	db SAMOPUP
	db CATTLEDOG
	db "@"

PrizeMenuMon1Cost:
	bcd2 180
	bcd2 500
	bcd2 1200
	db "@"

PrizeMenuMon2Entries:
	db AKITAFIRE
	db TERVPUP
	db SHEPHGUARD
	db "@"

PrizeMenuMon2Cost:
	bcd2 2500
	bcd2 4000
	bcd2 6500
	db "@"

PrizeMenuTMsEntries:
	db TM_DRAGON_RAGE
	db TM_HYPER_BEAM
	db TM_SUBSTITUTE
	db "@"

PrizeMenuTMsCost:
	bcd2 3300
	bcd2 5500
	bcd2 7700
	db "@"
