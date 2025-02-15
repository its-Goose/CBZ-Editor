from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import zipfile
import tempfile
import shutil
import tkinter as tk
import re
import time
import threading
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk


class CBZEditor:

    def __init__(self, root):
        self.root = root
        self.root.title('CBZ Editor Pro+')
        self.root.geometry('1200x800')
        self.current_cbz = None
        self.temp_dir = None
        self.thumbnail_size = 300
        self.cbz_files = []
        self.current_index = 0
        self.image_cache = {}
        self.modified_files = set()
        self.deleted_files = set()
        self.needs_refresh = False
        self.resize_timer = None
        self.image_frames = {}
        self.base_temp_dir = os.path.join(tempfile.gettempdir(),
            'CBZ_Editor_Pro_Temp')
        self.monitor_active = False
        self.file_timestamps = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.set_dark_theme()
        self.create_widgets()
        self.create_batch_button()
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<Control-s>', lambda e: self.save_and_next())
        self.root.bind('<Control-S>', lambda e: self.save_and_next())
        self.root.bind('<Control-w>', lambda e: self.close_and_next())
        self.root.bind('<Left>', lambda e: self.load_previous_cbz())
        self.root.bind('<Right>', lambda e: self.load_next_cbz())
        self.canvas.bind_all('<MouseWheel>', self.on_mouse_wheel)

        # New variable to track sorting order: True = ascending, False = descending
        self.sort_order = True  # Default to ascending order

        # Bind the "s" key to toggle sorting order
        self.root.bind('s', lambda e: self.toggle_sort_order())

    def set_dark_theme(self):
        self.root.configure(bg='#2d2d2d')
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('.', background='#2d2d2d', foreground='white')
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('TButton', background='#404040', foreground='white')
        self.style.map('TButton', background=[('active', '#505050')])
        self.style.configure('Large.TButton', font=('Arial', 12, 'bold'), padding=10)
        self.style.configure('green.TButton', background='#006600')
        self.style.configure('red.TButton', background='#660000')

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        ttk.Button(header_frame, text='←', width=3, command=self.load_previous_cbz).pack(side=tk.LEFT, padx=5)
        ttk.Button(header_frame, text='→', width=3, command=self.load_next_cbz).pack(side=tk.RIGHT, padx=5)
        self.title_label = ttk.Label(header_frame, text='No CBZ Loaded', font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=5, expand=True, fill=tk.X)
        control_frame = ttk.Frame(header_frame)
        control_frame.pack(pady=10)
        ttk.Button(control_frame, text='📂 Open', command=self.open_cbz).pack(side=tk.LEFT, padx=5)
        self.save_btn = ttk.Button(control_frame, text='💾 Save', width=15, style='Large.TButton', command=self.save_and_next)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text='✖ Close', command=self.close_and_next).pack(side=tk.LEFT, padx=5)
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(toolbar, text='Thumbnail Size:').pack(side=tk.LEFT)
        self.size_slider = ttk.Scale(toolbar, from_=100, to=500, command=lambda e: self.update_thumbnail_size())
        self.size_slider.set(self.thumbnail_size)
        self.size_slider.pack(side=tk.LEFT, padx=5)

        # Added label to show sorting order
        self.sort_label = ttk.Label(toolbar, text="  Order: First", font=('Arial', 10))
        self.sort_label.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(main_frame, bg='#2d2d2d', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.image_frame = ttk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_batch_button(self):
        batch_btn = ttk.Button(self.root, text='Batch Create CBZs', command=self.batch_create_cbzs)
        batch_btn.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)

    def batch_create_cbzs(self):
        zip_files = filedialog.askopenfilenames(title='Select Zip Files with Folders', filetypes=[('Zip files', '*.zip')], multiple=True)
        if not zip_files:
            return
        output_dir = filedialog.askdirectory(title='Select Output Directory')
        if not output_dir:
            return
        progress_window = tk.Toplevel(self.root)
        progress_window.title('Batch Processing')
        progress_window.geometry('400x150')
        progress_label = ttk.Label(progress_window, text='Processing zip files...')
        progress_label.pack(pady=10)
        progress = ttk.Progressbar(progress_window, orient='horizontal', length=300, mode='determinate')
        progress.pack(pady=10)
        status_label = ttk.Label(progress_window, text='')
        status_label.pack(pady=5)
        threading.Thread(target=self.process_batch, args=(zip_files, output_dir, progress, status_label, progress_window), daemon=True).start()

    def create_cbz_from_folder(self, folder_path, cbz_path):
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=lambda x: [(int(c) if c.isdigit() else c) for c in re.split('(\\d+)', x)])
        with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
            for image_file in image_files:
                image_path = os.path.join(folder_path, image_file)
                cbz_file.write(image_path, arcname=image_file)

    def open_cbz(self):
        file_types = [('CBZ files', '*.cbz'), ('Zip files', '*.zip')]
        self.cbz_files = filedialog.askopenfilenames(filetypes=file_types)
        if not self.cbz_files:
            return
        loading_window = tk.Toplevel(self.root)
        loading_window.title('Loading')
        loading_window.geometry('300x100')
        loading_label = ttk.Label(loading_window, text='Loading CBZ files...')
        loading_label.pack(pady=10)
        progress = ttk.Progressbar(loading_window, orient='horizontal', length=200, mode='indeterminate')
        progress.pack(pady=10)
        progress.start()
        threading.Thread(target=self.load_cbz_files, args=(loading_window,), daemon=True).start()

    def load_current_cbz(self):
        if self.current_index < len(self.cbz_files):
            self.load_cbz(self.cbz_files[self.current_index])
        else:
            self.title_label.config(text='All CBZs Processed')
            self.cbz_files = []
            self.current_index = 0

    def load_cbz(self, file_path):
        try:
            if self.temp_dir:
                self.stop_file_monitor()
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            os.makedirs(self.base_temp_dir, exist_ok=True)
            cbz_filename = os.path.basename(file_path)
            temp_dir_name = f'{cbz_filename}_{int(time.time())}'
            self.temp_dir = os.path.join(self.base_temp_dir, temp_dir_name)
            os.makedirs(self.temp_dir, exist_ok=True)
            self.current_cbz = file_path
            self.title_label.config(text=f'Editing: {cbz_filename} ({self.current_index + 1}/{len(self.cbz_files)})')
            self.sort_order = True  # Reset to ascending order when a new CBZ is loaded
            self.image_cache.clear()
            self.modified_files.clear()
            self.deleted_files.clear()
            self.needs_refresh = True
            self.image_frames.clear()
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            self.initialize_file_monitor()
            self.display_images()
        except Exception as e:
            self.show_status(f'Error: {str(e)}', 'red')
            self.load_next_cbz()

    def initialize_file_monitor(self):
        self.monitor_active = True
        self.file_timestamps = {f: os.path.getmtime(os.path.join(self.temp_dir, f)) for f in os.listdir(self.temp_dir)}
        threading.Thread(target=self.monitor_file_changes, daemon=True).start()

    def stop_file_monitor(self):
        self.monitor_active = False

    def monitor_file_changes(self):
        while self.monitor_active and self.temp_dir:
            try:
                current_files = set(os.listdir(self.temp_dir))
                for filename in current_files:
                    file_path = os.path.join(self.temp_dir, filename)
                    if os.path.isfile(file_path):
                        current_mtime = os.path.getmtime(file_path)
                        if (filename not in self.file_timestamps or current_mtime > self.file_timestamps[filename]):
                            self.file_timestamps[filename] = current_mtime
                            self.root.after(0, self.update_single_image, file_path)
                for filename in list(self.file_timestamps.keys()):
                    if filename not in current_files:
                        del self.file_timestamps[filename]
                        self.root.after(0, self.handle_deleted_file, filename)
                time.sleep(1)
            except Exception as e:
                print(f'Monitoring error: {e}')
                break

    def toggle_sort_order(self):
        """Toggle the sorting order between ascending and descending."""
        self.sort_order = not self.sort_order
        self.needs_refresh = True
        self.display_images()

        # Update the sort label based on the current sorting order
        if self.sort_order:
            self.sort_label.config(text="  Order: First")
        else:
            self.sort_label.config(text="  Order: Last")

    def display_images(self):
        if not self.temp_dir or not self.needs_refresh:
            return
        try:
            # Sort the images based on the current sorting order (ascending or descending)
            image_files = sorted([f for f in os.listdir(self.temp_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], 
                                 key=lambda x: [(int(c) if c.isdigit() else c) for c in re.split('(\\d+)', x)], reverse=not self.sort_order)
        except:
            image_files = sorted(os.listdir(self.temp_dir), reverse=not self.sort_order)
        
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        canvas_width = self.canvas.winfo_width() - 20
        cols = max(1, int(canvas_width / (self.thumbnail_size + 20)))
        for i in range(cols):
            self.image_frame.columnconfigure(i, weight=1, uniform='cols')
        row = col = 0
        for idx, filename in enumerate(image_files):
            if filename in self.deleted_files:
                continue
            img_path = os.path.join(self.temp_dir, filename)
            try:
                frame = ttk.Frame(self.image_frame)
                frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
                self.image_frames[filename] = frame
                self.create_image_widgets(frame, img_path, filename)
                col += 1
                if col >= cols:
                    col = 0
                    row += 1
            except Exception as e:
                print(f'Error loading {filename}: {e}')
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        self.needs_refresh = False

    def create_image_widgets(self, frame, img_path, filename):
        img = Image.open(img_path)
        img.thumbnail((self.thumbnail_size, self.thumbnail_size))
        photo = ImageTk.PhotoImage(img)
        container = ttk.Frame(frame)
        container.pack(expand=True, fill=tk.BOTH)
        lbl = ttk.Label(container, image=photo)
        lbl.image = photo
        lbl.pack(expand=True)
        ttk.Label(frame, text=filename).pack()
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        ttk.Button(btn_frame, text='Edit', command=lambda p=img_path: self.edit_image(p)).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text='Delete', command=lambda f=filename: self.delete_image(f)).pack(side=tk.LEFT)

    def edit_image(self, img_path):
        try:
            os.startfile(img_path)
            self.modified_files.add(img_path)
        except Exception as e:
            self.show_status(f'Error opening image: {str(e)}', 'red')

    def delete_image(self, filename):
        try:
            img_path = os.path.join(self.temp_dir, filename)
            os.remove(img_path)
            self.deleted_files.add(filename)
            self.needs_refresh = True
            self.display_images()
        except Exception as e:
            self.show_status(f'Delete failed: {str(e)}', 'red')

    def update_thumbnail_size(self, event=None):
        self.thumbnail_size = int(self.size_slider.get())
        self.needs_refresh = True
        self.display_images()

    def on_window_resize(self, event):
        if self.resize_timer:
            self.root.after_cancel(self.resize_timer)
        self.resize_timer = self.root.after(500, self.display_images)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), 'units')

    def load_previous_cbz(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_cbz()

    def load_next_cbz(self):
        if self.temp_dir:
            self.stop_file_monitor()
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = None
        self.current_index += 1
        self.load_current_cbz()

    def save_cbz(self):
        if not self.current_cbz or not self.temp_dir:
            self.show_status('No CBZ loaded!', 'red')
            return False
        try:
            with zipfile.ZipFile(self.current_cbz, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in os.listdir(self.temp_dir):
                    zipf.write(os.path.join(self.temp_dir, file), arcname=file)
            self.show_status('Saved successfully!', 'green')
            return True
        except Exception as e:
            self.show_status(f'Save failed: {str(e)}', 'red')
            return False

    def show_status(self, message, color):
        self.save_btn.config(style=f'{color}.TButton')
        self.root.after(2000, lambda: self.save_btn.config(style='Large.TButton'))

    def save_and_next(self):
        if self.current_cbz and self.save_cbz():
            self.load_next_cbz()

    def close_and_next(self):
        self.load_next_cbz()

    def process_batch(self, zip_files, output_dir, progress, status_label, progress_window):
        total_files = len(zip_files)
        progress['maximum'] = total_files
        try:
            created_count = 0
            for i, zip_path in enumerate(zip_files):
                status_label.config(text=f'Processing {os.path.basename(zip_path)}...')
                progress['value'] = i + 1
                progress_window.update()
                try:
                    temp_dir = tempfile.mkdtemp()
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    for root, dirs, files in os.walk(temp_dir):
                        for dir_name in dirs:
                            folder_path = os.path.join(root, dir_name)
                            cbz_path = os.path.join(output_dir, f'{dir_name}.cbz')
                            self.create_cbz_from_folder(folder_path, cbz_path)
                            created_count += 1
                        break
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f'Error processing {zip_path}: {e}')
            progress_window.destroy()
            messagebox.showinfo('Batch Complete', f"""Successfully created {created_count} CBZ files in:\n{output_dir}""")
        except Exception as e:
            progress_window.destroy()
            messagebox.showerror('Error', f'Batch processing failed:\n{str(e)}')

    def load_cbz_files(self, loading_window):
        self.current_index = 0
        self.load_current_cbz()
        loading_window.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = CBZEditor(root)
    root.mainloop()
