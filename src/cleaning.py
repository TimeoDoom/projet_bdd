from pathlib import Path
import pandas

data_path = Path(__file__).resolve().parent.parent / "data" / "route_performance.csv"
data = pandas.read_csv(data_path, skipinitialspace=True)
data.columns = data.columns.str.strip()

# Clean the data
for column in data.select_dtypes(include="object").columns:
	data[column] = data[column].str.strip()

data["region"] = data["region"].replace({
	"Asia-Europe": "Europe-Asia",
	"MENA": "Middle East",
})

# Derived columns for analysis
data["nb_compagnies"] = data["main_airlines"].str.count(",") + 1
data["revenu_par_vol"] = data["annual_revenue_usd_m"] / (
	data["weekly_frequency_est"] * 52
)
data["periode"] = pandas.cut(
	data["year"],
	bins=[2014, 2019, 2021, 2026],
	labels=[
		"Pré-Covid (2015-2019)",
		"Crise Covid (2020-2021)",
		"Reprise / Projection (2022-2026)",
	],
)

# Export of the cleaned data
cleaned_data_path = data_path.parent / "route_performance_clean.csv"
data.to_csv(cleaned_data_path, index=False)
