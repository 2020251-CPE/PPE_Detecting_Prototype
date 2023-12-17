from app import app
import os

# Run this when in prod
if __name__ == '__main__':
    try:
        app.run() # Remove this line when gunicorn is used as we won't use app.run directly
    except KeyboardInterrupt:
        folder_name = "screenshots"
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_list = os.listdir(folder_path)
        print("Removing screenshots")  
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
        print("Exiting gracefully.")        