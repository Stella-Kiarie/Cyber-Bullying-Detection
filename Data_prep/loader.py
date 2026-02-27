import pandas as pd
import plotly.express as px


class DataLoader:
    """
    A class for loading and analyzing the labelled dataset.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None

    # 1️⃣ Load Dataset
    def load_data(self) -> pd.DataFrame:
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"✅ Dataset loaded successfully from {self.file_path}")
            return self.data
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None

    # 2️⃣ Standardize Column Names
    def standardize_column_names(self) -> pd.DataFrame:
        """
        Standardize column names:
        - Lowercase
        - Remove leading/trailing spaces
        - Replace spaces with underscore
        - Remove special characters
        """
        if self.data is None:
            print("Load data first.")
            return None

        self.data.columns = (
            self.data.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace(r"[^\w]", "", regex=True)
        )

        print("✅ Column names standardized.")
        print("New columns:", list(self.data.columns))
        return self.data

    # 3️⃣ Drop Irrelevant Columns
    def drop_irrelevant_columns(self, columns_to_drop: list) -> pd.DataFrame:
        if self.data is None:
            print("Load data first.")
            return None

        self.data.drop(columns=columns_to_drop, inplace=True, errors='ignore')
        print(f"✅ Dropped columns: {columns_to_drop}")
        print(f"New shape: {self.data.shape}")
        return self.data

    # 4️⃣ Clean Subcategory Column
    def clean_subcategory(self, column_name: str = "subcategory") -> pd.DataFrame:
        """
        Remove text inside brackets from subcategory column.
        Example:
        "[Offensive] Non-personal" → "Non-personal"
        """
        if self.data is None:
            print("Load data first.")
            return None

        if column_name not in self.data.columns:
            print(f"Column '{column_name}' not found.")
            return None

        self.data[column_name] = (
            self.data[column_name]
            .str.replace(r"\[.*?\]", "", regex=True)
            .str.strip()
        )

        print(f"✅ Cleaned '{column_name}' column.")
        return self.data
       # Clean Language Column
    def clean_language_column(self, column_name: str = "language") -> pd.DataFrame:
        """
        Standardize language column values.
        Converts:
        "Mixed (Code-switching)" → "Code Switching"
        """
        if self.data is None:
            print("Load data first.")
            return None

        if column_name not in self.data.columns:
            print(f"Column '{column_name}' not found.")
            return None

        # Replace specific pattern
        self.data[column_name] = (
            self.data[column_name]
            .str.replace(r"Mixed\s*\(Code-switching\)", "Code Switching", regex=True)
            .str.strip()
        )

        print(f"✅ Cleaned '{column_name}' column.")
        return self.data

    # 5️⃣ Check Data Info
    def check_info(self) -> None:
        if self.data is None:
            print("Load data first.")
            return

        print("\n📊 DATA INFO")
        print("=" * 50)
        print(self.data.info())
        print(f"\nShape: {self.data.shape}")

    # 6️⃣ Check Missing Values
    def check_missing_values(self) -> pd.Series:
        if self.data is None:
            print("Load data first.")
            return None

        missing = self.data.isnull().sum()
        print("\n🔎 MISSING VALUES")
        print("=" * 50)
        print(missing)
        return missing

    # 7️⃣ Drop Rows with Missing Values
    def drop_missing_values(self) -> pd.DataFrame:
        if self.data is None:
            print("Load data first.")
            return None

        original_rows = self.data.shape[0]
        self.data.dropna(inplace=True)
        removed_rows = original_rows - self.data.shape[0]

        print(f"✅ Dropped {removed_rows} rows with missing values.")
        print(f"New shape: {self.data.shape}")
        return self.data

    # 8️⃣ Check Shape
    def check_shape(self) -> tuple:
        if self.data is None:
            print("Load data first.")
            return None

        print(f"\n📐 Current Shape: {self.data.shape}")
        return self.data.shape

    # 9️⃣ Check Duplicates
    def check_duplicates(self) -> int:
        if self.data is None:
            print("Load data first.")
            return 0

        duplicates = self.data.duplicated().sum()
        print(f"\n🔁 Duplicate rows: {duplicates}")
        return duplicates

    # 🔟 Drop Duplicates
    def drop_duplicates(self, subset: list = None) -> pd.DataFrame:
        """
        Drop duplicate rows.

        Args:
            subset (list): Optional columns to check duplicates on.
                           If None, entire row is considered.
        """
        if self.data is None:
            print("Load data first.")
            return None

        duplicate_count = self.data.duplicated(subset=subset).sum()

        if duplicate_count == 0:
            print("✅ No duplicate rows found.")
            return self.data

        self.data.drop_duplicates(subset=subset, inplace=True)

        print(f"✅ Removed {duplicate_count} duplicate rows.")
        print(f"New shape: {self.data.shape}")
        return self.data
