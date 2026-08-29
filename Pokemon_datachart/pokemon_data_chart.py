import matplotlib.pyplot as plt
import pandas as pd
def file_path():
      try:
          df = pd.read_csv(r"Pokemon_datachart\all_pokemon.csv")
          return df
      except FileNotFoundError:
          print("Error: The file 'all_pokemon.csv' was not found. Please ensure the file exists in the specified path.")
          return None

df = file_path()
type1_count=df['Type1'].value_counts()
only_type1=df['Type2'].isna().sum()
both_types=df['Type2'].notna().sum()
total_pokemons=len(df)
one_type=(only_type1/total_pokemons)*100
both=(both_types/total_pokemons)*100
types=[one_type,both]
type_labels=['Single type','Dual types',]
h_avg=df.groupby('Type1')[['Height']].mean()
w_avg=df.groupby('Type1')[['Weight']].mean()
leg=df.groupby('Type1')['Legendary'].sum()
#leg_aligned=leg[type1_count.index] you could also use this

#putting the classifications in th3 charts
figure , axes = plt.subplots(3,2,figsize=(16,14))
def no_pokemon():
    axes[0,0].barh(type1_count.index,type1_count,)
    axes[0,0].set_title("# of Pokémon in Each Type",fontsize=18)
    axes[0,0].set_xlabel("# Pokémon",fontsize=12)
    axes[0,0].set_ylabel("Types",fontsize=12)
    axes[0,0].tick_params(axis='y', rotation=25, labelsize=10)

def types_pokemon():
    axes[0,1].pie(types,labels=type_labels,autopct='%1.1f%%',shadow=True)
    axes[0,1].set_title("% Pure and Dual Type Pokémons",fontsize=18)
    height_by_type = [
    group["Height"].dropna().values
    for _, group in df.groupby("Type1")
     ]
    height_labels = df.groupby("Type1").groups.keys()

    axes[1, 0].boxplot(height_by_type, tick_labels=height_labels)
    axes[1, 0].set_title("Height Distribution of Pokémon in Each Type",fontsize=18) 
    axes[1,0].grid()
    axes[1,0].set_xlabel("Height in Meter",fontsize=12)
    axes[1,0].set_ylabel("Types",fontsize=12)
    axes[0,1].tick_params(axis="x", labelrotation=45)
    axes[1,0].tick_params(axis="x", labelrotation=45)
   

def weight_pokemon():
    weight_by_type = [
        group["Weight"].dropna().values
        for _, group in df.groupby("Type1")
        ]
    weight_labels = df.groupby("Type1").groups.keys()
    
    axes[1, 1].boxplot(weight_by_type, tick_labels=weight_labels)
    axes[1, 1].set_title("Weight Distribution of Pokémon in Each Type",fontsize=18)
    axes[1,1].grid()
    
    axes[1,1].tick_params(axis="x", labelrotation=45)

def popularity_pokemon():
    YandR={"04-05":3.5,
"06-07":4.0,
"08-09":4.0,
"10-11":3.75,
"12-13":3.25,
"14-15":4.25,
"16-17":4.25,
"18-19":4.0,
"20-21":4.0,
"22-23":4.25,
"24-25":4.0
}
    axes[2,0].plot(YandR.keys(),YandR.values())
    axes[2, 0].tick_params(axis='x', rotation=45, labelsize=8)
    axes[2,0].grid()
    axes[2,0].set_title("Popularity of Pokémon Franchise",fontsize=18)
    axes[2,0].set_xlabel("Years",fontsize=12)
    axes[2,0].set_ylabel("Rating",fontsize=12)
    axes[2,0].tick_params(axis='x', rotation=45, labelsize=8)

def legendary_pokemon():
   axes[2,1].bar(leg.index,leg)
   axes[2,1].tick_params(axis='x',rotation=65)
   axes[2,1].set_title("Legendary in Each Type",fontsize=18)
   axes[2,1].set_xlabel("Types",fontsize=12)
   axes[2,1].set_ylabel("# of Legendary",fontsize=12)
   axes[2,1].tick_params(axis='x', rotation=65, labelsize=8)

def main():
    no_pokemon()
    types_pokemon()
    weight_pokemon()
    popularity_pokemon()
    legendary_pokemon() 
    plt.tight_layout(h_pad=4.0, w_pad=3.0)
    plt.subplots_adjust(top=0.95, bottom=0.10, left=0.05, right=0.99, hspace=0.5, wspace=0.4)
    plt.savefig(r"Pokemon_datachart\images\pokemon_data_chart.png",dpi=300)
    plt.show()

if __name__ == "__main__":
    main()