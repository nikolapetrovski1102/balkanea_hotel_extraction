import os
from zstandard import ZstdDecompressor
import json
from datetime import date
from collections import defaultdict

def parse_dump(filename: str, output_file: str) -> None:
    """
    Parses a big zstd dump and saves Macedonian hotel data into a JSON file.
    :param filename: Path to a zstd archive
    :param output_file: Path to save the extracted JSON data
    """
    extracted_hotels = []  # To store hotel data
    count = 0  # Track number of hotels processed
    # regions = []
    grouped_hotels = defaultdict(list)

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
                        # if hotel_data['region']['country_code'] == 'GR':
                            # regions.append((hotel_data['region']['name'],hotel_data['region']['id']))
                        if hotel_data['region']['id'] == 3186 and hotel_data['region']['country_code'] == 'GR':
                            extracted_hotels.append({
                                "hotel_data": hotel_data,
                                'hotel_region_id': hotel_data['region']['id'],
                                'hotel_region_name': hotel_data['region']['name']
                            })
                            count += 1
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON line: {line}")
                previous_line = lines[-1]

    # Ensure directory exists before writing the file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    for hotel in extracted_hotels:
        region_id = hotel["hotel_region_id"]
        grouped_hotels[region_id].append(hotel["hotel_data"])

    # Convert defaultdict to regular dict for JSON serialization
    final_structure = {region_id: hotels for region_id, hotels in grouped_hotels.items()}

    # Save the extracted data to a JSON file
    with open(output_file, "w") as f:
        json.dump(final_structure, f, indent=4)

    # Convert to DataFrame
    # df = pd.DataFrame(regions, columns=["Region ID", "Region Name"])
    # Remove duplicates while keeping the first occurrence
    # df_unique = df.drop_duplicates().reset_index(drop=True)
    # df_unique.to_excel("Greece_regions.xlsx", index=False)


if __name__ == "__main__":
    zstd_filename = "feed_en_v3.json.zst"  # Your actual file

    # Define output directory and filename
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    output_file = os.path.join(output_dir, date.today().strftime('%d-%m-%Y') + ".json")

    parse_dump(zstd_filename, output_file)

    print(f"Extracted data saved to {output_file}")