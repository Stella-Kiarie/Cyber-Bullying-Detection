from huggingface_hub import login, upload_folder
import os

# login using environment variable
login(token=os.getenv("HF_TOKEN"))

# upload the models folder
upload_folder(
    folder_path="Models",
    repo_id="ste-pp/kenyan-cyberbullying-models",
    repo_type="model",
    commit_message="Upload Kenyan cyberbullying models"
)

print("Upload completed successfully")