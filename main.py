import os
from zstandard import ZstdDecompressor
import json
from datetime import date

def parse_dump(filename: str, output_file: str) -> None:
    """
    Parses a big zstd dump and saves Macedonian hotel data into a JSON file.
    :param filename: Path to a zstd archive
    :param output_file: Path to save the extracted JSON data
    """
    extracted_hotels = []  # To store hotel data
    count = 0  # Track number of hotels processed

    with open(filename, "rb") as fh:
        # Make decompressor
        dctx = ZstdDecompressor()
        with dctx.stream_reader(fh) as reader:
            previous_line = ""
            while True:
                # Read the file in 16MB chunks
                chunk = reader.read(2 ** 24)
                if not chunk:
                    break

                raw_data = chunk.decode("utf-8")
                lines = raw_data.split("\n")
                for i, line in enumerate(lines[:-1]):
                    if i == 0:
                        line = previous_line + line
                    try:
                        hotel_data = json.loads(line)
                        if hotel_data['region']['name'] == 'Berovo':
                            extracted_hotels.append(hotel_data)
                            count += 1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON line: {line}")
                previous_line = lines[-1]

    # Ensure directory exists before writing the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save the extracted data to a JSON file
    with open(output_file, "w") as f:
        json.dump(extracted_hotels, f, indent=4)


if __name__ == "__main__":
    zstd_filename = "feed_en_v3.json.zst"  # Your actual file

    # Define output directory and filename
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    output_file = os.path.join(output_dir, date.today().strftime('%d-%m-%Y') + ".json")

    parse_dump(zstd_filename, output_file)

    print(f"Extracted data saved to {output_file}")
