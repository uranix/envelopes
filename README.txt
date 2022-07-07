1. ./process.sh > spam.sql. Преобразует spam.raw в виде
	Учреждение [индекс, адрес] - 5 экз.
в SQL базу
	recepient, address, zip, copies, phony
Если phony != 0, то pdf для этой записи не создается
2. sqlite3 spam.db < spam.sql
3. При необходимости подправить данные в базе руками командой 
    sqlitebrowser spam.db
4. ./makeenvelopes.py создает Envelopes.pdf и spam.txt
