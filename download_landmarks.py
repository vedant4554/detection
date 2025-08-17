import os
import urllib.request
import bz2
import shutil

def download_landmarks_file():
    """Download and extract the shape predictor file"""
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    filename = "shape_predictor_68_face_landmarks.dat.bz2"
    extracted_filename = "shape_predictor_68_face_landmarks.dat"
    
    print("Downloading shape_predictor_68_face_landmarks.dat.bz2...")
    print("This may take a few minutes...")
    
    try:
        # Download the file
        urllib.request.urlretrieve(url, filename)
        print("Download completed!")
        
        # Extract the bz2 file
        print("Extracting file...")
        with bz2.BZ2File(filename, 'rb') as f_in:
            with open(extracted_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print("Extraction completed!")
        
        # Remove the compressed file
        os.remove(filename)
        print("Cleaned up compressed file.")
        
        print(f"Successfully downloaded and extracted {extracted_filename}")
        return True
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

if __name__ == "__main__":
    if os.path.exists("shape_predictor_68_face_landmarks.dat"):
        print("shape_predictor_68_face_landmarks.dat already exists!")
    else:
        download_landmarks_file() 