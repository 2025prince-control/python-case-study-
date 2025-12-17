import time
import matplotlib.pyplot as plt



def announce(func):
    """Prints a 'Generating pattern...' message before execution."""
    def wrapper(*args, **kwargs):
        print("\n Generating pattern...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f" Operation finished in {(end_time - start_time):.} seconds.")
        return result
    return wrapper


PATTERN_TYPES = {
    1: "Left-aligned Triangle",
    2: "Right-aligned Triangle",
    3: "Pyramid (Centered)",
    4: "Inverted Pyramid (Centered)",
    5: "Diamond",
}


class NumberPattern:
    
    def __init__(self, rows, pattern_type, spacing=" "):
        self.rows = rows
        self.pattern_type = pattern_type
        self.spacing = spacing
        self.generated_pattern = None

    def _generate_triangle_numbers(self, row_index):
        """Generates numbers for a single row: 1 2 3 4 ..."""
        nums = [str(i) for i in range(1, row_index + 1)]
        return self.spacing.join(nums)

    def _generate_pyramid_numbers(self, row_index):
        """Generates numbers for a single pyramid row: 1 2 3 2 1"""
        s = "".join(str(i) for i in range(1, row_index + 1))
        if row_index > 1:
            s += s[len(s)-2::-1]
        return self.spacing.join(list(s))

  
    def generate(self):
        pattern_list = []
        max_row_str = self._generate_pyramid_numbers(self.rows)
        max_width = len(max_row_str)
        type_id = self.pattern_type

        if type_id in [1, 2]:
            for i in range(1, self.rows + 1):
                row_str = self._generate_triangle_numbers(i)
                if type_id == 1:
                    formatted_row = row_str.ljust(max_width)
                elif type_id == 2:
                    formatted_row = row_str.rjust(max_width)
                pattern_list.append(formatted_row)
        
        elif type_id in [3, 4, 5]:
            temp_rows = [self._generate_pyramid_numbers(i) for i in range(1, self.rows + 1)]
            rows_to_use = []
            
            if type_id == 3:
                rows_to_use = temp_rows
            elif type_id == 4:
                rows_to_use = temp_rows[::-1]
            elif type_id == 5:
                rows_to_use = temp_rows + temp_rows[:-1][::-1]

            for row_str in rows_to_use:
                pattern_list.append(row_str.center(max_width))

        self.generated_pattern = pattern_list
        return self.generated_pattern

    def as_text(self):
        if not self.generated_pattern: self.generate()
        header = f"Pattern: {PATTERN_TYPES.get(self.pattern_type)}, Rows: {self.rows}, Spacing: '{self.spacing}'\n"
        return header + "\n".join(self.generated_pattern)

    def as_html(self):
        if not self.generated_pattern: self.generate()
        pattern_body = "<br>".join(
            f'<span style="white-space: pre;">{row.replace(" ", "&nbsp;")}</span>' 
            for row in self.generated_pattern
        )
        return f"""
        <!DOCTYPE html><html><head><title>Pattern</title></head>
        <body style="font-family: monospace; line-height: 1.2; padding: 20px;">
            <h2>{PATTERN_TYPES.get(self.pattern_type)}</h2><hr>{pattern_body}
        </body></html>
        """

    def save(self, file_path, mode='w'):
        if not self.generated_pattern: self.generate()
        content = ""
        if file_path.endswith(".txt"): content = self.as_text()
        elif file_path.endswith(".html"): content = self.as_html()
        else: return print(" Error: Unsupported file type. Use .txt or .html")

        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content + "\n")
            print(f" Pattern saved successfully to -> **{file_path}** (Mode: '{mode}')")
        except Exception as e:
            print(f" Error saving file: {e}")

    
    def save_image(self, file_path="pattern.png"):
        if not self.generated_pattern: self.generate()
        
        plt.figure(figsize=(10, self.rows / 2 + 1)) 
        plt.text(0.5, 0.5, "\n".join(self.generated_pattern), 
                 ha='center', va='center', fontsize=8, family='monospace')
        
        plt.title(f"{PATTERN_TYPES.get(self.pattern_type)} (Rows: {self.rows})", fontsize=10)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close() 
        print(f" Pattern image saved successfully to -> **{file_path}**")

    def show(self):
        print("\n" + "="*40)
        print(" PREVIEW:")
        print("="*40)
        print(self.as_text())
        print("="*40)


class PatternVisualizer:
    
    def __init__(self):
        self.pattern_obj = None

    def display_menu(self):
        print("\n"  + " NUMBER PATTERN VISUALIZER " )
        print("Options:")
        for key, value in PATTERN_TYPES.items():
            print(f"  {key}. Select pattern: {value}")
        print("-" * 40)
        print("  7. Save as text/HTML/Image")
        print("  8. Exit Program")
        print("-" * 40)

    def get_validated_input(self, prompt, type_func=int, validation_func=lambda x: True):
        while True:
            try:
                user_input = type_func(input(prompt))
                if validation_func(user_input):
                    return user_input
                else:
                    print(" Input validation failed. Please try again.")
            except ValueError:
                print(" Invalid input type. Please enter the correct format.")

    def configure_pattern(self):
        
        type_id = self.get_validated_input(
            "1. Enter Pattern Type ID (1-5): ", 
            validation_func=lambda x: x in PATTERN_TYPES
        )
        
        rows = self.get_validated_input(
            "2. Enter number of rows (> 0): ", 
            validation_func=lambda x: x > 0
        )
        
        spacing = input("3. Enter Spacing Character (leave blank for space): ") or " "
        
        self.pattern_obj = NumberPattern(
            rows=rows, 
            pattern_type=type_id, 
            spacing=spacing
        )
        self.pattern_obj.generate()
        print(f" Pattern generated: {PATTERN_TYPES[type_id]} with {rows} rows.")

    def handle_save_options(self):
        if not self.pattern_obj or not self.pattern_obj.generated_pattern:
            print(" Please generate a pattern first (Option 1-5).")
            return

        print("\n--- Save Options ---")
        print("1. Save as Text (.txt)")
        print("2. Save as HTML (.html)")
        print("3. Save as Image (.png)")
        save_choice = self.get_validated_input(
            "Enter Save Option (1-3): ",
            validation_func=lambda x: x in [1, 2, 3]
        )

        if save_choice == 1:
            file_path = input("Enter filename (default: pattern.txt): ") or "pattern.txt"
            mode = input("Use 'w' (overwrite) or 'a' (append)? (default: w): ") or 'w'
            self.pattern_obj.save(file_path, mode.lower())
        elif save_choice == 2:
            file_path = input("Enter filename (default: pattern.html): ") or "pattern.html"
            self.pattern_obj.save(file_path, 'w')
        elif save_choice == 3:
            file_path = input("Enter filename (default: pattern.png): ") or "pattern.png"
            self.pattern_obj.save_image(file_path)

    def run(self):
        while True:
            self.display_menu()
            
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print(" Invalid input. Please enter a number.")
                continue

            if choice in PATTERN_TYPES:
                self.configure_pattern()
                self.pattern_obj.show()
            
            elif choice == 7:
                self.handle_save_options()

            elif choice == 8:
                print("\n Exiting Number Pattern Visualizer. Goodbye!")
                break
                
            else:
                print(" Invalid choice. Please select an option from the menu (1-8).")


if __name__ == "__main__":
    visualizer = PatternVisualizer()
    visualizer.run()