import tkinter as tk
from tkinter import messagebox
from login.loginScript import login
from login.signUp import create_user
from db.main import *

# Dictionary for service mapping
services = {
    "a": "Amazon Prime",
    "n": "Netflix",
    "d": "Disney+",
    "h": "Hulu",
    "hb": "HBO Max",
    "p": "Peacock",
    "y": "YouTube",
    "f": "Free Services",
    "c": "Cable TV",
}

# Dark mode colors
dark_mode_colors = {
    "bg": "#2e2e2e",  # Background
    "fg": "#ffffff",  # Foreground
    "button_bg": "#444444",
    "button_fg": "#ffffff",
    "entry_bg": "#3c3c3c",
    "entry_fg": "#ffffff",
    "scrollbar_bg": "#444444",
}

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x250")
        self.root.configure(bg=dark_mode_colors["bg"])  # Set background to dark mode

        tk.Label(self.root, text="Username:", bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.username_entry.pack()

        tk.Label(self.root, text="Password:", bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(pady=10)
        tk.Button(self.root, text="Sign Up", command=self.open_signup, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(pady=5)

        # Label to display login status
        self.login_status = tk.Label(self.root, text="", fg="red", bg=dark_mode_colors["bg"])
        self.login_status.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)  # Handle close button

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.login_status.config(text="Username or password cannot be empty")
            return

        login_successful = login(username, password)

        if login_successful:
            self.root.withdraw()  # Hide login window
            ContentAppWindow(self.root, username)
        else:
            self.login_status.config(text="Invalid username or password")

    def open_signup(self):
        SignUpWindow(self.root)

    def close_application(self):
        self.root.destroy()


class SignUpWindow:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel()
        self.root.title("Sign Up")
        self.root.geometry("400x300")
        self.root.configure(bg=dark_mode_colors["bg"])  # Dark mode for signup window

        # Username entry
        tk.Label(self.root, text="Username:", bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.username_entry.pack()

        # Password entry
        tk.Label(self.root, text="Password:", bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.password_entry.pack()

        # Confirm password entry
        tk.Label(self.root, text="Confirm Password:", bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.root, show="*", width=30, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.confirm_password_entry.pack()

        # Sign Up button
        tk.Button(self.root, text="Sign Up", command=self.sign_up, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(pady=10)

        # Status label for error messages
        self.status_label = tk.Label(self.root, text="", fg="red", bg=dark_mode_colors["bg"])
        self.status_label.pack(pady=5)

    def sign_up(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            self.status_label.config(text="All fields are required")
            return

        if password != confirm_password:
            self.status_label.config(text="Passwords do not match")
            return

        try:
            if usernameExists(username):
                self.status_label.config(text="Username already exists")
                return

            create_user(username, password)
            messagebox.showinfo("Success", "User created successfully. You can now login.")
            self.root.destroy()
        except Exception as e:
            self.status_label.config(text="An error occurred during sign up")
            print(f"Error during sign up: {e}")

    def close_window(self):
        self.root.destroy()


class ContentAppWindow:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username
        self.user_id = getUserID(username)
        self.root = tk.Toplevel()
        self.root.title(f"Content Application - Welcome, {username}")
        self.root.geometry("1280x800")
        self.set_dark_theme()

        # Search bar
        search_frame = tk.Frame(self.root, bg=dark_mode_colors["bg"])
        search_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(search_frame, text="Search:", font=("Arial", 12), bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=40, bg=dark_mode_colors["entry_bg"], fg=dark_mode_colors["entry_fg"])
        self.search_entry.pack(side="left", padx=5)

        tk.Button(search_frame, text="Search", command=self.perform_search, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="left", padx=5)
        tk.Button(search_frame, text="Watchlist", command=self.open_watchlist, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="right", padx=5)

        # Scrollable results area
        results_frame = tk.Frame(self.root, bg=dark_mode_colors["bg"])
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(results_frame, bg=dark_mode_colors["bg"])
        self.scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview, bg=dark_mode_colors["scrollbar_bg"])
        self.scrollable_frame = tk.Frame(self.canvas, bg=dark_mode_colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Log Out", command=self.logout, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="top", anchor="w", padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def set_dark_theme(self):
        self.root.configure(bg=dark_mode_colors["bg"])

    def perform_search(self):
        query = self.search_entry.get().strip()
        if query:
            results = search(query)
            self.populate_results(results)
        else:
            messagebox.showerror("Error", "Please enter a search query.")

    def populate_results(self, results):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if len(results) == 0:
            tk.Label(self.scrollable_frame, text="No results found", font=("Arial", 12), bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=10)
            return

        for result in results:
            showid, title, type, genre, from_service, description = result
            parsedResult = f"{title} ({type}) - Genre: {genre} - Available on {services[from_service]} - {description}"

            result_frame = tk.Frame(self.scrollable_frame, bg=dark_mode_colors["bg"])
            result_frame.pack(fill="x", pady=5, padx=10)

            result_label = tk.Label(result_frame, text=parsedResult, font=("Arial", 12), anchor="w", justify="center", wraplength=750, bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"])
            result_label.pack(fill="x", padx=5)

            tk.Button(result_frame, text="Add to Watchlist", command=lambda r=showid: self.addShow(r), bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="right", padx=5)

    def addShow(self, show_id):
        addToWatchlist(self.user_id, show_id)
        messagebox.showinfo("Success", "Show added to watchlist")

    def open_watchlist(self):
        WatchlistWindow(self.root, self.user_id)

    def logout(self):
        self.root.destroy()
        self.parent.deiconify()

    def close_application(self):
        self.root.destroy()
        self.parent.destroy()


class WatchlistWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        self.root = tk.Toplevel()
        self.root.title("Watchlist")
        self.root.geometry("800x600")
        self.root.configure(bg=dark_mode_colors["bg"])

        watchlist_frame = tk.Frame(self.root, bg=dark_mode_colors["bg"])
        watchlist_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(watchlist_frame, bg=dark_mode_colors["bg"])
        self.scrollbar = tk.Scrollbar(watchlist_frame, orient="vertical", command=self.canvas.yview, bg=dark_mode_colors["scrollbar_bg"])
        self.scrollable_frame = tk.Frame(self.canvas, bg=dark_mode_colors["bg"])

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Button(self.root, text="Close", command=self.close_window, bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="bottom", pady=10)

        self.fill_watchlist()

    def fill_watchlist(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        watchlist = getWatchlist(self.user_id)
        if not watchlist:
            tk.Label(self.scrollable_frame, text="Your watchlist is empty", font=("Arial", 12), bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"]).pack(pady=10)
            return

        for show_id in watchlist:
            show = getMovieInfo(show_id)
            if show:
                showid, title, type, genre, from_service, description = show
                parsedResult = f"{title} ({type}) - Genre: {genre} - Available on {services[from_service]} - {description}"

                result_frame = tk.Frame(self.scrollable_frame, bg=dark_mode_colors["bg"])
                result_frame.pack(fill="x", pady=5, padx=10)

                result_label = tk.Label(result_frame, text=parsedResult, font=("Arial", 12), anchor="w", justify="center", wraplength=750, bg=dark_mode_colors["bg"], fg=dark_mode_colors["fg"])
                result_label.pack(fill="x", padx=5)

                tk.Button(result_frame, text="Remove from Watchlist", command=lambda r=showid: self.removeFromWatchlist(r), bg=dark_mode_colors["button_bg"], fg=dark_mode_colors["button_fg"]).pack(side="right", padx=5)

    def removeFromWatchlist(self, show_id):
        removeFromWatchlist(self.user_id, show_id)
        messagebox.showinfo("Success", "Show removed from watchlist")
        self.fill_watchlist()

    def close_window(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
