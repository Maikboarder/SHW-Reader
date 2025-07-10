import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import xml.etree.ElementTree as ET
import os

# Silencia la advertencia de obsolescencia de Tk en macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def parse_shw_file(filepath):
        header_frame = tk.Frame(self.table_frame, bg='#34495e', relief=tk.RAISED, bd=3)
        header_frame.pack(fill="x", pady=(0, 3))
        
        headers = ["☑️ Dispositivo / Modelo", "📻 Nombre del Canal", "📡 Frecuencia", "🌐 RF Zone", "📊 Banda"]
        widths = [300, 250, 150, 100, 100]
        
        # Add "Select All" checkbox for first column
        first_header_container = tk.Frame(header_frame, bg='#34495e')
        first_header_container.pack(side=tk.LEFT, fill="both", expand=True)
        
        select_all_frame = tk.Frame(first_header_container, bg='#34495e')
        select_all_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        self.select_all_var = tk.BooleanVar()
        select_all_checkbox = tk.Checkbutton(select_all_frame, variable=self.select_all_var, 
                                           bg='#34495e', fg='white',
                                           command=self.toggle_select_all)
        select_all_checkbox.pack(pady=10)
        
        first_label = tk.Label(first_header_container, text=headers[0], font=("Arial", 11, "bold"),
                              bg='#34495e', fg='white', anchor="w", padx=15, pady=10,
                              width=(widths[0]-30)//8, relief=tk.FLAT, bd=1)
        first_label.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Add separator
        separator = tk.Frame(header_frame, bg='#2c3e50', width=2)
        separator.pack(side=tk.LEFT, fill="y", padx=1)
        
        # Regular headers for remaining columns
        for i, (header, width) in enumerate(zip(headers[1:], widths[1:]), 1):
            label = tk.Label(header_frame, text=header, font=("Arial", 11, "bold"),
                           bg='#34495e', fg='white', anchor="w", padx=15, pady=10,
                           width=width//8, relief=tk.FLAT, bd=1)
            label.pack(side=tk.LEFT, fill="both", expand=True)
            
            # Add separator line between columns (except last)
            if i < len(headers) - 1:
                separator = tk.Frame(header_frame, bg='#2c3e50', width=2)
                separator.pack(side=tk.LEFT, fill="y", padx=1)= '1'

def parse_shw_file(filepath):
    """Parses the .shw file and extracts device information."""
    devices = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Find all device elements
        all_devices = root.findall('.//device')
        
        for i, device in enumerate(all_devices):
            device_info = {}
            
            # Extract top-level device details
            series = device.find('series')
            if series is not None and series.text:
                device_info['series'] = series.text.strip()
            else:
                device_info['series'] = 'N/A'

            model = device.find('model')
            if model is not None and model.text:
                device_info['model'] = model.text.strip()
            else:
                device_info['model'] = 'N/A'

            device_name_elem = device.find('device_name')
            if device_name_elem is not None and device_name_elem.text:
                 device_info['device_name'] = device_name_elem.text.strip()
            else:
                 device_info['device_name'] = 'N/A'

            zone_elem = device.find('zone')
            if zone_elem is not None and zone_elem.text:
                device_info['zone'] = zone_elem.text.strip()
            else:
                device_info['zone'] = 'N/A'

            band_elem = device.find('band')
            if band_elem is not None and band_elem.text:
                device_info['band'] = band_elem.text.strip()
            else:
                device_info['band'] = 'N/A'

            device_info['channels'] = []

            # Find all channel elements within the device
            channels = device.findall('channel')
            
            for channel in channels:
                channel_info = {}
                
                channel_name_elem = channel.find('channel_name')
                if channel_name_elem is not None:
                    # Handle CDATA sections
                    if channel_name_elem.text:
                        channel_info['name'] = channel_name_elem.text.strip()
                    else:
                        channel_info['name'] = 'N/A'
                else:
                    channel_info['name'] = 'N/A'

                frequency_elem = channel.find('frequency')
                if frequency_elem is not None and frequency_elem.text:
                    try:
                        # Frequency is in kHz, convert to MHz for display
                        freq_mhz = int(frequency_elem.text) / 1000
                        channel_info['frequency'] = f"{freq_mhz:.3f} MHz"
                    except (ValueError, TypeError):
                        channel_info['frequency'] = 'N/A'
                else:
                    channel_info['frequency'] = 'N/A'
                
                # Always add channel, even if some info is missing
                device_info['channels'].append(channel_info)

            # Always add device if it has any meaningful data
            if (device_info.get('device_name') != 'N/A' or 
                device_info.get('model') != 'N/A' or 
                device_info.get('series') != 'N/A' or 
                device_info['channels']):
                devices.append(device_info)

        return devices

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
        
    return devices

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SHW File Reader")
        self.geometry("1200x700")
        self.configure(bg='#f0f0f0')

        # --- Control Frame ---
        control_frame = tk.Frame(self, bg='#f0f0f0', relief=tk.RAISED, bd=2)
        control_frame.pack(pady=15, padx=20, fill="x")
        
        # Title label
        title_label = tk.Label(control_frame, text="SHW File Reader - Lector de Archivos Wireless Workbench", 
                              font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=5)
        
        # Button frame
        button_frame = tk.Frame(control_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.open_button = tk.Button(button_frame, text="📁 Abrir archivo .shw", command=self.open_file,
                                   font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3,
                                   padx=25, pady=8, cursor="hand2")
        self.open_button.pack(side=tk.LEFT, padx=15)
        
        self.clear_button = tk.Button(button_frame, text="🗑️ Limpiar", command=self.clear_data,
                                    font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3,
                                    padx=25, pady=8, cursor="hand2")
        self.clear_button.pack(side=tk.LEFT, padx=15)
        
        self.export_button = tk.Button(button_frame, text="💾 Exportar CSV", command=self.export_csv,
                                     font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3,
                                     padx=25, pady=8, cursor="hand2")
        self.export_button.pack(side=tk.LEFT, padx=15)
        
        self.delete_button = tk.Button(button_frame, text="🗑️ Eliminar Seleccionados", command=self.delete_selected,
                                     font=("Arial", 12, "bold"), relief=tk.RAISED, bd=3,
                                     padx=25, pady=8, cursor="hand2", bg='#ff6b6b', fg='white')
        self.delete_button.pack(side=tk.LEFT, padx=15)
        
        # Info frame
        info_frame = tk.Frame(control_frame, bg='#e8f4f8', relief=tk.GROOVE, bd=2)
        info_frame.pack(fill="x", pady=5, padx=10)
        
        info_text = "📋 Esta aplicación lee archivos .shw de Wireless Workbench y muestra dispositivos y canales en una tabla. 💡 Haz doble clic en nombres de canales y frecuencias para editarlos."
        self.info_label = tk.Label(info_frame, text=info_text, font=("Arial", 10), 
                                 bg='#e8f4f8', fg='#2c3e50', wraplength=800, justify="left")
        self.info_label.pack(pady=8, padx=10)

        # --- Table Container ---
        container = tk.Frame(self, bg='#f0f0f0')
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        self.v_scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        
        self.table_frame = tk.Frame(self.canvas, bg='white')
        
        # Configure scrolling
        self.table_frame.bind("<Configure>", 
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, 
                            xscrollcommand=self.h_scrollbar.set)
        
        # Pack scrollbars and canvas
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mousewheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Create table headers
        self.create_headers()
        
        # Status Bar
        self.status_bar = tk.Label(self, text="Listo. Por favor, abre un archivo .shw", 
                                 bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Selected rows tracking
        self.selected_rows = set()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_headers(self):
        header_frame = tk.Frame(self.table_frame, bg='#34495e', relief=tk.RAISED, bd=3)
        header_frame.pack(fill="x", pady=(0, 3))
        
        headers = ["📱 Dispositivo / Modelo", "📻 Nombre del Canal", "📡 Frecuencia", "🌐 RF Zone", "📊 Banda"]
        widths = [300, 250, 150, 100, 100]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = tk.Label(header_frame, text=header, font=("Arial", 11, "bold"),
                           bg='#34495e', fg='white', anchor=tk.W, padx=15, pady=10,
                           width=width//8, relief=tk.FLAT, bd=1)
            label.pack(side=tk.LEFT, fill="both", expand=True)
            
            # Add separator line between columns (except last)
            if i < len(headers) - 1:
                separator = tk.Frame(header_frame, bg='#2c3e50', width=2)
                separator.pack(side=tk.LEFT, fill="y", padx=1)
            

        
    def make_editable_cell(self, row_frame, text, width, anchor, font_style, text_color, bg_color, column_index, row_data, is_first_column=False):
        """Creates an editable cell that can switch between label and entry"""
        cell_container = tk.Frame(row_frame, bg=bg_color)
        cell_container.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Add checkbox for first column (device/model)
        if is_first_column:
            checkbox_frame = tk.Frame(cell_container, bg=bg_color)
            checkbox_frame.pack(side=tk.LEFT, padx=(5, 0))
            
            checkbox_var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, variable=checkbox_var, bg=bg_color,
                                    command=lambda: self.toggle_row_selection(row_frame, checkbox_var.get()))
            checkbox.pack(pady=6)
            
            # Store checkbox reference in row frame
            row_frame.checkbox_var = checkbox_var
        
        cell_frame = tk.Frame(cell_container, bg=bg_color)
        cell_frame.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Create label
        label = tk.Label(cell_frame, text=text, font=font_style,
                        bg=bg_color, fg=text_color, anchor=anchor, padx=10, pady=6,
                        width=(width-30 if is_first_column else width)//8, relief=tk.FLAT, bd=1,
                        wraplength=width-20)
        label.pack(fill="both", expand=True)
        
        # Only make channel name (index 1) and frequency (index 2) editable
        if column_index in [1, 2]:
            def on_double_click(event):
                self.edit_cell(cell_frame, label, text, column_index, row_data)
            
            label.bind("<Double-Button-1>", on_double_click)
            label.configure(cursor="hand2")
        
        return label
    
    def edit_cell(self, cell_frame, label, current_text, column_index, row_data):
        """Replace label with entry for editing"""
        # Hide label
        label.pack_forget()
        
        # Create entry
        entry_var = tk.StringVar(value=current_text)
        entry = tk.Entry(cell_frame, textvariable=entry_var, font=("Arial", 10),
                        justify=tk.LEFT if column_index == 1 else tk.CENTER,
                        relief=tk.SOLID, bd=1)
        entry.pack(fill="both", expand=True, padx=2, pady=2)
        entry.focus_set()
        entry.select_range(0, tk.END)
        
        def save_edit():
            new_text = entry_var.get().strip()
            if new_text != current_text:
                # Update the display
                label.config(text=new_text)
                # Update row data
                if column_index == 1:  # Channel name
                    row_data['channel_name'] = new_text
                elif column_index == 2:  # Frequency
                    row_data['frequency'] = new_text
                self.update_status(f"Campo actualizado: {new_text}")
            
            # Replace entry with label
            entry.destroy()
            label.pack(fill="both", expand=True)
        
        def cancel_edit():
            entry.destroy()
            label.pack(fill="both", expand=True)
        
        # Bind events
        entry.bind("<Return>", lambda e: save_edit())
        entry.bind("<Escape>", lambda e: cancel_edit())
        entry.bind("<FocusOut>", lambda e: save_edit())

    def toggle_row_selection(self, row_frame, is_selected):
        """Toggle row selection state"""
        if is_selected:
            self.selected_rows.add(row_frame)
            # Visual feedback
            row_frame.configure(relief=tk.SOLID, bd=2, highlightbackground='#007acc')
        else:
            self.selected_rows.discard(row_frame)
            row_frame.configure(relief=tk.SOLID, bd=1)
        
        # Update status
        count = len(self.selected_rows)
        if count > 0:
            self.update_status(f"{count} fila(s) seleccionada(s)")
        else:
            self.update_status("Listo. Por favor, abre un archivo .shw")
    
    def delete_selected(self):
        """Delete selected rows"""
        if not self.selected_rows:
            messagebox.showwarning("Aviso", "No hay filas seleccionadas para eliminar.")
            return
        
        count = len(self.selected_rows)
        result = messagebox.askyesno("Confirmar eliminación", 
                                   f"¿Estás seguro de que quieres eliminar {count} fila(s) seleccionada(s)?")
        
        if result:
            # Remove selected rows
            for row_frame in list(self.selected_rows):
                row_frame.destroy()
            
            self.selected_rows.clear()
            self.update_status(f"{count} fila(s) eliminada(s)")
            
            # Force refresh
            self.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_table_row(self, device, channel, freq, zone, band):
        # Get current number of data rows (excluding header)
        row_count = len([w for w in self.table_frame.winfo_children() if isinstance(w, tk.Frame) and w != self.table_frame.winfo_children()[0]])
        
        # Alternate row colors
        bg_color = '#f8f9fa' if row_count % 2 == 0 else '#ffffff'
        border_color = '#dee2e6' if row_count % 2 == 0 else '#e9ecef'
        
        row_frame = tk.Frame(self.table_frame, bg=bg_color, relief=tk.SOLID, bd=1)
        row_frame.pack(fill="x", pady=1)
        
        # Store row data for editing
        row_data = {
            'device': device,
            'channel_name': channel,
            'frequency': freq,
            'zone': zone,
            'band': band
        }
        
        # Data cells
        data = [device, channel, freq, zone, band]
        widths = [300, 250, 150, 100, 100]
        anchors = [tk.W, tk.W, tk.CENTER, tk.CENTER, tk.CENTER]
        
        for i, (text, width, anchor) in enumerate(zip(data, widths, anchors)):
            # Highlight device names
            font_style = ("Arial", 10, "bold") if device and i == 0 else ("Arial", 10)
            text_color = '#2c3e50' if device and i == 0 else '#495057'
            
            # Use editable cell for appropriate columns
            label = self.make_editable_cell(row_frame, text, width, anchor, font_style, 
                                          text_color, bg_color, i, row_data, is_first_column=(i == 0))
            
            # Add separator line between columns (except last)
            if i < len(data) - 1:
                separator = tk.Frame(row_frame, bg=border_color, width=1)
                separator.pack(side=tk.LEFT, fill="y")
            
    def clear_data(self):
        # Remove all rows except header
        children = self.table_frame.winfo_children()
        for child in children[1:]:  # Keep header (first child)
            child.destroy()
        self.status_bar.config(text="Tabla limpiada")
        self.canvas.yview_moveto(0)


    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Selecciona un archivo .shw",
            filetypes=(("SHW files", "*.shw"), ("All files", "*.*"))
        )
        if not filepath:
            return

        # Clear previous data
        self.clear_data()
        
        # Update status safely
        self.update_status(f"Procesando: {os.path.basename(filepath)}...")

        try:
            devices = parse_shw_file(filepath)
            if not devices:
                messagebox.showwarning("Aviso", "No se encontraron dispositivos con datos válidos en el archivo.")
                return

            self.display_data(devices)
            self.update_status(f"Éxito. Se encontraron {len(devices)} dispositivos.")

        except Exception as e:
            print(f"Error procesando archivo: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n{e}")
            self.update_status("Error al procesar el archivo.")
    
    def update_status(self, message):
        """Safely update status bar"""
        try:
            if hasattr(self, 'status_bar') and self.status_bar.winfo_exists():
                self.status_bar.config(text=message)
                self.update_idletasks()
        except:
            print(f"Status: {message}")  # Fallback to console

    def display_data(self, devices):
        print(f"Mostrando {len(devices)} dispositivos")
        
        # Clear any existing data first
        self.clear_data()
        
        row_count = 0
        # Process each device
        for device in devices:
            device_display_name = f"{device.get('device_name', 'Dispositivo')} ({device.get('model', 'N/A')})"
            zone = device.get('zone', 'N/A')
            band = device.get('band', 'N/A')

            if device['channels']:
                for i, channel in enumerate(device['channels']):
                    name = channel.get('name', 'N/A')
                    freq = channel.get('frequency', 'N/A')
                    
                    # For the first channel, show device name. For others, leave it blank.
                    if i == 0:
                        self.add_table_row(device_display_name, name, freq, zone, band)
                    else:
                        self.add_table_row("", name, freq, zone, band)
                    row_count += 1
            else:
                # If a device has no channels, still show the device
                self.add_table_row(device_display_name, "N/A", "N/A", zone, band)
                row_count += 1
        
        # Force refresh
        self.update_idletasks()
        self.canvas.yview_moveto(0)  # Scroll to top
        
        # Final count
        print(f"Total de filas insertadas: {row_count}")
        
        # Update status safely
        self.update_status(f"Éxito. Se mostraron {row_count} filas de {len(devices)} dispositivos.")

    def export_csv(self):
        """Export current table data to CSV"""
        import csv
        from tkinter import filedialog
        
        # Get all table rows
        children = self.table_frame.winfo_children()
        if len(children) <= 1:  # Only header or empty
            messagebox.showwarning("Aviso", "No hay datos para exportar.")
            return
        
        # Ask for save location
        filepath = filedialog.asksaveasfilename(
            title="Guardar datos como CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                headers = ["Dispositivo/Modelo", "Nombre del Canal", "Frecuencia", "RF Zone", "Banda"]
                writer.writerow(headers)
                
                # Write data rows
                for row_frame in children[1:]:  # Skip header
                    row_data = []
                    for cell_frame in row_frame.winfo_children():
                        if isinstance(cell_frame, tk.Frame):
                            # Get text from label inside cell_frame
                            for widget in cell_frame.winfo_children():
                                if isinstance(widget, tk.Label):
                                    row_data.append(widget.cget("text"))
                                    break
                        elif hasattr(cell_frame, 'cget'):
                            row_data.append(cell_frame.cget("text"))
                    
                    if row_data:
                        writer.writerow(row_data)
            
            self.update_status(f"Datos exportados a: {os.path.basename(filepath)}")
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos:\n{e}")
            self.update_status("Error al exportar datos.")

