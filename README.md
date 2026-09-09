# Data-analysis

A collection of data analysis and visualization projects, each exploring a different dataset — from exploratory data analysis (EDA) to charts and insights built with Python's data science stack.

Each project lives in its own subfolder with its own notebook/script, data file, and (where relevant) its own README.

## Projects

| Project | Description | Stack |
|---|---|---|
| `sales/` | Exploratory analysis of a sales dataset — trends, revenue breakdowns, and key business metrics visualized. | Python, pandas, Sql, Power Bi |
| `Pokemon_datachart/` | Data visualization and charting on a Pokémon stats dataset — comparing types, stats distributions, and other patterns. | pandas, matplotlib |
| `IBM/` | Analysis of the IBM HR Employee Attrition dataset — exploring factors related to employee attrition and satisfaction. | Power Bi |

## Repo Structure
```
Data-Analysis/
├── sales/
|   ├── sales.py            
|   ├── sales.sql
|   ├── sales.pbix          
|   ├── requirements.txt    
|   ├── .env.example        
|   ├── .gitignore          
|   └── README.md
├── Pokemon_datachart/
|   ├── data_gen.py                
|   ├── pokemon_data_chart.py      
|   ├── all_pokemon.csv            
|   |── requirements.txt           
|   ├── images/
|   │   └── Fig_1.png              
|   └── README.md
├── IBM/
|   ├── IBM.pbix
|   └── README.md
└── README.md          # you are here
```

## How to Use
Each project is self-contained — clone the repo, `cd` into the project folder you want, and open its notebook.

```bash
git clone https://github.com/Pranav10261/Data-Analysis.git
cd Data-Analysis/<project-folder>
pip install -r requirements.txt   # if present
jupyter notebook
```

## Purpose
These projects are focused on practicing:
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Building clear, informative charts and visualizations
- Drawing insights from structured datasets

## Author
Pranav K — [Pranav10261](https://github.com/Pranav10261)
