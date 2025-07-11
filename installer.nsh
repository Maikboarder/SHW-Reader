; Script personalizado para el instalador NSIS
; Instalar Python y pip si no están presentes

!macro customInstall
  ; Verificar si Python está instalado
  ExecWait '"python" --version' $0
  ${If} $0 != 0
    ; Python no está instalado, descargar e instalar
    MessageBox MB_YESNO "Python 3.x es requerido para SHW Reader. ¿Desea instalarlo automáticamente?" IDYES InstallPython IDNO SkipPython
    
    InstallPython:
      DetailPrint "Descargando Python..."
      NSISdl::download "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe" "$TEMP\python-installer.exe"
      Pop $R0
      ${If} $R0 == "success"
        DetailPrint "Instalando Python..."
        ExecWait '"$TEMP\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0'
        Delete "$TEMP\python-installer.exe"
      ${Else}
        MessageBox MB_OK "Error descargando Python. Por favor, instále Python manualmente desde python.org"
      ${EndIf}
    
    SkipPython:
  ${EndIf}
  
  ; Instalar dependencias de Python
  DetailPrint "Instalando dependencias Python..."
  ExecWait '"python" -m pip install flask openpyxl python-docx reportlab' $1
  ${If} $1 != 0
    MessageBox MB_OK "Error instalando dependencias Python. La aplicación podría no funcionar correctamente."
  ${EndIf}
!macroend
