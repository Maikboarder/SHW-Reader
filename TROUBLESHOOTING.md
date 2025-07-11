# 🔧 Guía de Solución de Problemas - SHW Reader

## ❌ "Error instalando Python. Instale Python manualmente"

### ¿Por qué ocurre este error?

Este error aparece cuando SHW Reader no puede instalar automáticamente las dependencias de Python (Flask) necesarias para el funcionamiento completo. Esto puede ocurrir por varias razones:

1. **Python no está instalado** en su sistema
2. **Python está instalado pero no está en el PATH** del sistema
3. **pip no está disponible** o configurado correctamente
4. **Permisos insuficientes** para instalar paquetes Python
5. **Firewall o antivirus** bloqueando la instalación

### ✅ Soluciones

#### Opción 1: Instalación Completa de Python (Recomendada)

1. **Descargue Python desde el sitio oficial:**
   - Vaya a [python.org/downloads](https://python.org/downloads/)
   - Descargue la versión más reciente de Python 3.9 o superior

2. **Durante la instalación:**
   - ✅ **IMPORTANTE**: Marque la casilla "Add Python to PATH"
   - ✅ Marque "Install pip" (viene marcado por defecto)
   - ✅ Marque "Install for all users" (recomendado)

3. **Después de la instalación:**
   - Abra una nueva terminal/comando (CMD)
   - Ejecute: `python --version` (debería mostrar la versión instalada)
   - Ejecute: `pip --version` (debería mostrar la versión de pip)

4. **Instale las dependencias manualmente:**
   ```bash
   pip install flask openpyxl python-docx reportlab
   ```

5. **Reinicie SHW Reader** - ahora debería funcionar completamente

#### Opción 2: Usar Modo Básico (Funcionalidad Limitada)

Si no puede instalar Python ahora mismo:

1. **Inicie SHW Reader**
2. **Cuando aparezca el error**, seleccione "Usar Modo Básico"
3. **Funciones disponibles en modo básico:**
   - ✅ Visualización básica de archivos SHW
   - ✅ Interfaz de usuario completa
   - ❌ Procesamiento completo de archivos SHW
   - ❌ Exportación a Excel, Word, PDF
   - ❌ Funciones avanzadas de edición

### 🔍 Diagnóstico de Problemas

#### Verificar si Python está instalado:

**Windows:**
```cmd
python --version
python3 --version
pip --version
```

**Si no funciona:**
- Python no está instalado o no está en el PATH
- Reinstale Python marcando "Add to PATH"

#### Verificar pip:
```cmd
python -m pip --version
```

**Si no funciona:**
- pip no está disponible
- Reinstale Python con pip incluido

#### Instalar Flask manualmente:
```cmd
python -m pip install --user flask openpyxl python-docx reportlab
```

**Si da error de permisos:**
```cmd
python -m pip install --user flask openpyxl python-docx reportlab
```

### 🛠️ Casos Especiales

#### Python instalado con Anaconda/Miniconda:
```cmd
conda install flask openpyxl python-docx reportlab
```

#### Python instalado desde Microsoft Store:
- A veces no incluye pip correctamente
- Desinstale la versión de Microsoft Store
- Instale desde python.org

#### Empresas con restricciones de red:
```cmd
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask openpyxl python-docx reportlab
```

### 📞 ¿Necesita más ayuda?

1. **Documentación completa:** [README.md](https://github.com/Maikboarder/SHW-Reader#installation)
2. **Reportar problemas:** [GitHub Issues](https://github.com/Maikboarder/SHW-Reader/issues)
3. **Tutorial en video:** [Próximamente]

### 🎯 Resumen Rápido

**Para usuarios que quieren la solución más rápida:**

1. Descargue Python de [python.org](https://python.org/downloads/)
2. Durante instalación: ✅ "Add Python to PATH"
3. Abra CMD y ejecute: `pip install flask openpyxl python-docx reportlab`
4. Reinicie SHW Reader

**¡Listo! SHW Reader funcionará con todas sus características.**
