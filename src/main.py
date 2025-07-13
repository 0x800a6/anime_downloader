#!/usr/bin/env python3
"""
Anime Downloader GUI
A modern GUI application for downloading anime using anipy-api
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import os
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

from anipy_api.provider import get_provider, LanguageTypeEnum
from anipy_api.anime import Anime
from anipy_api.download import Downloader
from ttkthemes import ThemedTk


class AnimeDownloaderGUI:
    def __init__(self):
        # Create the main window with ttkbootstrap dark theme
        self.root = tb.Window(themename="darkly")
        self.root.title("Anime Downloader")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        # Variables
        self.search_results = []
        self.selected_anime = None
        self.episodes = []
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.provider = None
        self.download_queue = []
        
        # Initialize provider
        self.init_provider()
        
        # Create GUI elements
        self.create_widgets()
        
        # Configure grid weights for responsiveness
        self.configure_grid()
    
    def init_provider(self):
        """Initialize the anime provider"""
        try:
            self.provider = get_provider("allanime")  # Use a valid provider name! Do NOT call it, it returns an instance.
        except Exception as e:
            self.provider = None
            messagebox.showerror("Error", f"Failed to initialize provider: {str(e)}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = tb.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        # Title
        title_label = tb.Label(main_frame, text="Anime Downloader", font=("Segoe UI", 24, "bold"), bootstyle="info")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)
        # Search frame
        search_frame = tb.Labelframe(main_frame, text="Search Anime", padding=10)
        search_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0, 10))
        tb.Label(search_frame, text="Anime Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.search_entry = tb.Entry(search_frame, width=40, font=("Segoe UI", 12))
        self.search_entry.grid(row=0, column=1, sticky="we", padx=(0, 10))
        self.search_entry.bind('<Return>', lambda event: self.search_anime())
        search_btn = tb.Button(search_frame, text="Search", command=self.search_anime, bootstyle="primary")
        search_btn.grid(row=0, column=2, padx=(10, 0))
        # Results frame
        results_frame = tb.Labelframe(main_frame, text="Search Results", padding=10)
        results_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        results_scrollbar = tb.Scrollbar(results_frame, bootstyle="round")
        results_scrollbar.grid(row=0, column=1, sticky="ns")
        # Treeview for results
        self.results_treeview = tb.Treeview(results_frame, columns=("Anime"), show="headings", height=8, bootstyle="dark")
        self.results_treeview.heading("Anime", text="Anime (Languages)")
        self.results_treeview.column("Anime", anchor="w", width=600, stretch=True)
        self.results_treeview.grid(row=0, column=0, sticky="nsew")
        self.results_treeview.bind('<Double-1>', self.on_anime_select)
        results_scrollbar.config(command=self.results_treeview.yview)
        self.results_treeview.config(yscrollcommand=results_scrollbar.set)
        # Anime details frame
        details_frame = tb.Labelframe(main_frame, text="Anime Details", padding=10)
        details_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=(0, 10))
        self.anime_title_label = tb.Label(details_frame, text="Select an anime to see details")
        self.anime_title_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        episodes_frame = tb.Frame(details_frame)
        episodes_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0, 10))
        tb.Label(episodes_frame, text="Episode:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.episode_combobox = tb.Combobox(episodes_frame, state="readonly", width=15)
        self.episode_combobox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        tb.Label(episodes_frame, text="Language:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.language_combobox = tb.Combobox(episodes_frame, state="readonly", width=15, values=["SUB", "DUB"])
        self.language_combobox.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        self.language_combobox.set("SUB")
        tb.Label(episodes_frame, text="Quality:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.quality_combobox = tb.Combobox(episodes_frame, state="readonly", width=15, values=["1080", "720", "480", "360"])
        self.quality_combobox.grid(row=0, column=5, sticky=tk.W)
        self.quality_combobox.set("720")
        # Download settings frame
        download_frame = tb.Labelframe(main_frame, text="Download Settings", padding=10)
        download_frame.grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 10))
        tb.Label(download_frame, text="Download Path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.path_entry = tb.Entry(download_frame, textvariable=self.download_path, width=50)
        self.path_entry.grid(row=0, column=1, sticky="we", padx=(0, 10))
        browse_btn = tb.Button(download_frame, text="Browse", command=self.browse_download_path, bootstyle="secondary")
        browse_btn.grid(row=0, column=2)
        buttons_frame = tb.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0), sticky="we")
        self.download_episode_btn = tb.Button(buttons_frame, text="Download Episode", command=self.download_episode, state=tk.DISABLED, bootstyle="primary")
        self.download_episode_btn.grid(row=0, column=0, padx=(0, 10))
        self.download_all_btn = tb.Button(buttons_frame, text="Download All Episodes", command=self.download_all_episodes, state=tk.DISABLED, bootstyle="primary")
        self.download_all_btn.grid(row=0, column=1, padx=(0, 10))
        progress_frame = tb.Labelframe(main_frame, text="Download Progress", padding=10)
        progress_frame.grid(row=6, column=0, columnspan=3, sticky="we", pady=(10, 0))
        self.progress_label = tb.Label(progress_frame, text="Ready to download")
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.progress_bar = tb.Progressbar(progress_frame, mode='determinate', bootstyle="success-striped")
        self.progress_bar.grid(row=1, column=0, sticky="we")
        self.status_label = tb.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=7, column=0, columnspan=3, sticky="we", pady=(10, 0))
    
    def configure_grid(self):
        """Configure grid weights for responsive design"""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = self.root.winfo_children()[0]
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Results frame
        
        # Results frame
        for child in main_frame.winfo_children():
            if isinstance(child, tb.Labelframe) and child.cget('text') == 'Search Results':
                child.columnconfigure(0, weight=1)
                child.rowconfigure(0, weight=1)
                break
        
        # Search frame
        for child in main_frame.winfo_children():
            if isinstance(child, tb.Labelframe) and child.cget('text') == 'Search Anime':
                child.columnconfigure(1, weight=1)
                break
        
        # Download frame
        for child in main_frame.winfo_children():
            if isinstance(child, tb.Labelframe) and child.cget('text') == 'Download Settings':
                child.columnconfigure(1, weight=1)
                break
        
        # Progress frame
        for child in main_frame.winfo_children():
            if isinstance(child, tb.Labelframe) and child.cget('text') == 'Download Progress':
                child.columnconfigure(0, weight=1)
                break
        
        # Buttons frame
        for child in main_frame.winfo_children():
            if isinstance(child, tb.Frame) and len(child.winfo_children()) > 1:
                child.columnconfigure(0, weight=1)
                child.columnconfigure(1, weight=1)
                break
    
    def update_status(self, message):
        """Update the status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def search_anime(self):
        """Search for anime"""
        search_query = self.search_entry.get().strip()
        if not search_query:
            messagebox.showwarning("Warning", "Please enter an anime name to search")
            return
        if not self.provider:
            messagebox.showerror("Error", "Provider not initialized.")
            return
        self.update_status("Searching...")
        # Run search in background thread to avoid freezing GUI
        def search_thread():
            try:
                # linter: self.provider is not None here
                results = self.provider.get_search(search_query)  # type: ignore
                # Update GUI in main thread
                self.root.after(0, self.update_search_results, results)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Search failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Search failed"))
        threading.Thread(target=search_thread, daemon=True).start()
    
    def update_search_results(self, results):
        """Update the search results listbox"""
        self.search_results = results
        self.results_treeview.delete(*self.results_treeview.get_children())
        
        for result in results:
            # Display anime name and available languages
            languages = ", ".join(lang.name for lang in result.languages)
            display_text = f"{result.name} ({languages})"
            self.results_treeview.insert("", tk.END, values=(display_text,))
        
        self.update_status(f"Found {len(results)} results")
    
    def on_anime_select(self, event):
        """Handle anime selection from results"""
        selection = self.results_treeview.selection()
        if not selection:
            return
        index = self.results_treeview.index(selection[0])
        if index >= len(self.search_results):
            return
        result = self.search_results[index]
        if not self.provider:
            messagebox.showerror("Error", "Provider not initialized.")
            return

        # Defensive: ensure identifier, name, and languages exist
        identifier = getattr(result, 'identifier', None)
        if identifier is None:
            identifier = getattr(result, 'id', None)
        if identifier is None:
            messagebox.showerror("Error", "Anime identifier not found in search result.")
            return

        name = getattr(result, 'name', None)
        if name is None:
            messagebox.showerror("Error", "Anime name not found in search result.")
            return

        languages = getattr(result, 'languages', None)
        if not languages:
            languages = [LanguageTypeEnum.SUB]
        if not isinstance(languages, (set, list, tuple)):
            languages = [languages]
        languages = set(languages)

        try:
            self.selected_anime = Anime(self.provider, name, identifier, languages)  # type: ignore
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Anime object: {e}")
            return

        self.update_status("Loading anime details...")
        # Load anime details in background
        def load_details():
            try:
                lang = LanguageTypeEnum.SUB if LanguageTypeEnum.SUB in languages else next(iter(languages))
                episodes = self.selected_anime.get_episodes(lang=lang)  # type: ignore
                self.root.after(0, self.update_anime_details, result, episodes)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load anime details: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Failed to load details"))
        threading.Thread(target=load_details, daemon=True).start()
    
    def update_anime_details(self, result, episodes):
        """Update anime details display"""
        self.episodes = episodes
        
        # Update title
        self.anime_title_label.config(text=result.name)
        
        # Update episodes dropdown
        episode_values = [f"Episode {ep}" for ep in episodes]
        self.episode_combobox['values'] = episode_values
        if episode_values:
            self.episode_combobox.set(episode_values[0])
        
        # Update language dropdown based on available languages
        available_langs = [lang.name for lang in result.languages]
        self.language_combobox['values'] = available_langs
        if available_langs:
            self.language_combobox.set(available_langs[0])
        
        # Enable download buttons
        self.download_episode_btn.config(state=tk.NORMAL)
        self.download_all_btn.config(state=tk.NORMAL)
        
        self.update_status("Anime details loaded")
    
    def browse_download_path(self):
        """Browse for download directory"""
        folder_path = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder_path:
            self.download_path.set(folder_path)
    
    def get_current_settings(self):
        """Get current download settings"""
        episode_text = self.episode_combobox.get()
        if not episode_text:
            return None, None, None, None
        
        # Extract episode number
        episode_num = int(episode_text.split()[-1])
        
        # Get language
        lang_text = self.language_combobox.get()
        lang = LanguageTypeEnum.SUB if lang_text == "SUB" else LanguageTypeEnum.DUB
        
        # Get quality
        quality = int(self.quality_combobox.get())
        
        # Get download path
        download_dir = Path(self.download_path.get())
        
        return episode_num, lang, quality, download_dir
    
    def download_episode(self):
        """Download selected episode"""
        if not self.selected_anime:
            messagebox.showwarning("Warning", "Please select an anime first")
            return
        settings = self.get_current_settings()
        if not all(settings):
            messagebox.showwarning("Warning", "Please select all download settings")
            return
        episode_num, lang, quality, download_dir = settings
        if episode_num is None or lang is None or quality is None or download_dir is None:
            messagebox.showwarning("Warning", "Incomplete download settings.")
            return
        # Start download in background
        def download_thread():
            try:
                self.root.after(0, lambda: self.update_status(f"Downloading Episode {episode_num}..."))
                self.root.after(0, lambda: self.progress_label.config(text=f"Preparing Episode {episode_num}..."))
                # Get video stream
                print(f"Calling get_video with: episode_num={episode_num}, lang={lang}, quality={quality}")
                try:
                    stream = self.selected_anime.get_video(int(episode_num), lang, preferred_quality=int(quality))  # type: ignore
                    print("get_video returned:", stream)
                except IndexError:
                    print("get_video raised IndexError")
                    stream = None
                except Exception as e:
                    print("get_video raised Exception:", e)
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Error getting stream: {e}"))
                    self.root.after(0, lambda: self.update_status("Download failed"))
                    self.root.after(0, lambda: self.progress_bar.config(value=0))
                    return

                if not stream:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"No stream found for Episode {episode_num} ({lang.name}, {quality}p)"))
                    self.root.after(0, lambda: self.update_status("No stream found"))
                    self.root.after(0, lambda: self.progress_bar.config(value=0))
                    return

                # Create downloader with callbacks
                def progress_callback(percentage):
                    self.root.after(0, lambda: self.progress_bar.config(value=percentage))
                    self.root.after(0, lambda: self.progress_label.config(text=f"Downloading Episode {episode_num}: {percentage:.1f}%"))
                def info_callback(message, exc_info=None):
                    self.root.after(0, lambda: self.update_status(message))
                def error_callback(message, exc_info=None):
                    self.root.after(0, lambda: self.update_status(f"Warning: {message}"))
                downloader = Downloader(progress_callback, info_callback, error_callback)
                # Create download path
                selection = self.results_treeview.selection()
                if selection:
                    index = self.results_treeview.index(selection[0])
                else:
                    index = None
                if index is not None and index < len(self.search_results):
                    anime_name = getattr(self.search_results[index], 'name', 'Anime')
                elif self.selected_anime is not None:
                    anime_name = getattr(self.selected_anime, 'name', 'Anime')
                else:
                    anime_name = 'Anime'
                anime_name = anime_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                filename = f"{anime_name}_Episode_{episode_num}.mkv"
                # Download
                final_path = downloader.download(
                    stream=stream,
                    download_path=download_dir / filename,
                    container=".mkv",
                    max_retry=3
                )
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text=f"Episode {episode_num} downloaded successfully!"))
                self.root.after(0, lambda: self.update_status("Download completed"))
                self.root.after(0, lambda: messagebox.showinfo("Success", f"Episode {episode_num} downloaded to:\n{final_path}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Download failed"))
                self.root.after(0, lambda: self.progress_bar.config(value=0))
        threading.Thread(target=download_thread, daemon=True).start()
    
    def download_all_episodes(self):
        """Download all episodes"""
        if not self.selected_anime or not self.episodes:
            messagebox.showwarning("Warning", "Please select an anime first")
            return
        # Confirm download
        result = messagebox.askyesno("Confirm", f"Download all {len(self.episodes)} episodes?")
        if not result:
            return
        settings = self.get_current_settings()
        if not settings[1] or not settings[2] or not settings[3]:  # lang, quality, download_dir
            messagebox.showwarning("Warning", "Please select language, quality and download path")
            return
        _, lang, quality, download_dir = settings
        if lang is None or quality is None or download_dir is None:
            messagebox.showwarning("Warning", "Incomplete download settings.")
            return
        # Start download in background
        def download_all_thread():
            try:
                total_episodes = len(self.episodes)
                for i, episode_num in enumerate(self.episodes, 1):
                    self.root.after(0, lambda i=i, e=episode_num: self.progress_label.config(text=f"Downloading Episode {e} ({i}/{total_episodes})..."))
                    self.root.after(0, lambda i=i: self.progress_bar.config(value=(i-1)/total_episodes * 100))
                    try:
                        # Get video stream
                        # linter: self.selected_anime is not None here
                        stream = self.selected_anime.get_video(int(episode_num), lang, preferred_quality=int(quality))  # type: ignore
                        # Create downloader
                        def progress_callback(percentage):
                            overall_progress = ((i-1) + percentage/100) / total_episodes * 100
                            self.root.after(0, lambda: self.progress_bar.config(value=overall_progress))
                        def info_callback(message, exc_info=None):
                            pass  # Skip individual episode info messages
                        def error_callback(message, exc_info=None):
                            pass  # Skip individual episode error messages
                        downloader = Downloader(progress_callback, info_callback, error_callback)
                        # Create download path
                        selection = self.results_treeview.selection()
                        if selection:
                            index = self.results_treeview.index(selection[0])
                        else:
                            index = None
                        if index is not None and index < len(self.search_results):
                            anime_name = getattr(self.search_results[index], 'name', 'Anime')
                        elif self.selected_anime is not None:
                            anime_name = getattr(self.selected_anime, 'name', 'Anime')
                        else:
                            anime_name = 'Anime'
                        anime_name = anime_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                        filename = f"{anime_name}_Episode_{episode_num}.mkv"
                        # Download
                        downloader.download(
                            stream=stream,
                            download_path=download_dir / filename,
                            container=".mkv",
                            max_retry=3
                        )
                    except Exception as e:
                        self.root.after(0, lambda e=episode_num, err=str(e): messagebox.showerror("Error", f"Failed to download episode {e}: {err}"))
                self.root.after(0, lambda: self.progress_bar.config(value=100))
                self.root.after(0, lambda: self.progress_label.config(text="All episodes downloaded!"))
                self.root.after(0, lambda: self.update_status("All downloads completed"))
                self.root.after(0, lambda: messagebox.showinfo("Success", f"All episodes downloaded to:\n{download_dir}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {str(e)}"))
                self.root.after(0, lambda: self.update_status("Download failed"))
        threading.Thread(target=download_all_thread, daemon=True).start()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = AnimeDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()