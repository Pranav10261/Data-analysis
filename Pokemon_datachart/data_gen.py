import requests
import csv

# Currently, there are 1025 Pokémon in the National Pokédex
TOTAL_POKEMON = 1025

print(f"Starting download for {TOTAL_POKEMON} Pokémon.")
print("This will take a few minutes. Please keep the app open...\n")

# Create and open the CSV file
with open("all_pokemon.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write your exact column headers
    writer.writerow(["No", "Name", "Type1", "Type2", "Height", "Weight", "Legendary"])

    for i in range(1, TOTAL_POKEMON + 1):
        try:
            # 1. Fetch the main data (Name, Types, Height, Weight)
            url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{i}"
            poke_data = requests.get(url_pokemon).json()
            
            name = poke_data["name"].capitalize()
            # PokéAPI stores height in decimetres and weight in hectograms, so we divide by 10
            height = poke_data["height"] / 10  
            weight = poke_data["weight"] / 10  
            
            # Extract types (some only have 1 type, so we check the length)
            types = poke_data["types"]
            type1 = types[0]["type"]["name"].capitalize()
            type2 = types[1]["type"]["name"].capitalize() if len(types) > 1 else ""
            
            # 2. Fetch the species data (to check if it is Legendary or Mythical)
            url_species = f"https://pokeapi.co/api/v2/pokemon-species/{i}"
            species_data = requests.get(url_species).json()
            
            is_legendary = 1 if (species_data["is_legendary"] or species_data["is_mythical"]) else 0
            
            # Write the row to the CSV
            writer.writerow([i, name, type1, type2, height, weight, is_legendary])
            
            # Print a progress update so you know it's still working
            if i % 50 == 0:
                print(f"Successfully downloaded data for {i}/{TOTAL_POKEMON} Pokémon...")
                
        except Exception as e:
            print(f"Error fetching data for #{i}: {e}")

print("\nFinished! The file 'all_pokemon.csv' has been generated and saved.")