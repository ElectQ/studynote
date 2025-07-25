# studynote
JUST FOR STUDY


#Windows WDK download link

https://github.com/appveyor/build-images/tree/master/scripts/Windows


# Windows Server Avaticve
DISM /online /Get-CurrentEdition

DISM /online /Set-Edition:ServerDatacenter /ProductKey:xxxxxx(version from https://github.com/netnr/kms) /AcceptEula

slmgr -skms skms.netnr.eu.org

slmgr -ipk （ProductKey)

slmgr -ato

