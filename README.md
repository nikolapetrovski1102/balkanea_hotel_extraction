# Hotel Data Extractor

This project extracts hotel data from a `.zst` archive and saves desired hotels information into a JSON file. The script also supports an API request to fetch updated hotel data from a secured endpoint.

---

## 📌 Prerequisites
### 1️⃣ Install Dependencies
Ensure you have Python installed. Then, install required dependencies using:
```bash
pip install zstandard
```

### 2️⃣ File Structure
```
project-folder/
│-- extracting_hotels.php
│-- extract_hotels.py
│-- config.php
│-- output/ (Generated JSON files are saved here)
```

---

## 🔹 API Request for Extracting Hotels
This project supports an **authenticated API request** to:
```
https://staging.balkanea.com/wp-plugin/extracting_hotels.php
```
To access this endpoint, you need **Basic Authentication** credentials. These credentials are sent via email upon setup.

### 📡 How to Make the API Call
Use `curl` to manually test the endpoint:
```bash
curl -u username:password -X GET "https://staging.balkanea.com/wp-plugin/extracting_hotels.php"
```
Or make a request in Postman:
```Postman
POST: https://staging.balkanea.com/wp-plugin/extracting_hotels.php
```

Replace `username:password` with the correct credentials provided in the email.

In the response from the API request contains URL that includes this .zst file, proceed the link to download it

---

## 🔄 Extracting Hotel Data from `.zst` File
The `extract_hotels.py` script processes a `.zst` file containing hotel data.

### 📝 **Usage**
```bash
python extract_hotels.py
```

### ⚙ **Script Details**
- **Input:** `feed_en_v3.json.zst`
- **Output:** JSON file in `output/` directory with the name format `dd-mm-yyyy.json`.

### 🔧 **Steps Performed by the Script:**
1. Decompresses the `.zst` file.
2. Reads data line by line to avoid memory overflow.
3. Filters hotels where `region.name == "Berovo"`.
4. Saves extracted hotels into a `JSON` file.

---

## ❗ Troubleshooting
- **"FileNotFoundError"** → Ensure the `.zst` file exists in the same directory.
- **"Permission Denied"** → Run `chmod +x extract_hotels.py` or use `sudo` if needed.
- **API request fails** → Check if the credentials are correct and the endpoint is accessible.

---

## 👨‍💻 Author
**Nikola Petrovski**

