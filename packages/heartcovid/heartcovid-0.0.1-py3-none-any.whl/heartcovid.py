import pandas as pd
import subprocess as sp
import sys
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

sp.call('wget -nc https://github.com/i-inose/heartcovid/raw/main/Center_for_Medicare___Medicaid_Services__CMS____Medicare_Claims_data.csv', shell=True)

data = pd.read_csv("Center_for_Medicare___Medicaid_Services__CMS____Medicare_Claims_data.csv")
data = data[["YearStart", "Topic", "Data_Value"]]

def plot_cause(keyword):
	# 2016から2019までのraw data
	condition = (data["YearStart"].between(2016, 2019)) & (data["Topic"] == keyword)
	data_16_19 = data[condition]
	data_16_19.drop(columns=["Topic"], inplace=True)
	data_16_19.rename(columns={"Data_Value":keyword}, inplace=True)
	data_16_19_mean = data_16_19.groupby('YearStart')[keyword].mean().reset_index()

	# 2020から2021のraw data
	condition = (data["YearStart"].between(2020, 2021)) & (data["Topic"] == keyword)
	data_20_21 = data[condition]
	data_20_21.drop(columns=["Topic"], inplace=True)
	data_20_21.rename(columns={"Data_Value":keyword}, inplace=True)
	data_20_21_mean = data_20_21.groupby('YearStart')[keyword].mean().reset_index()

	X = data_16_19_mean['YearStart'].values.reshape(-1, 1)
	y = data_16_19_mean[keyword].values
	reg = LinearRegression().fit(X, y)
	X_pred = data_20_21_mean[['YearStart']]
	y_pred = reg.predict(X_pred)
	r_squared = r2_score(y, reg.predict(X))

	impact_df = pd.DataFrame({'Year': data_20_21_mean['YearStart'], 'Actual': data_20_21_mean[keyword], 'Predicted': y_pred[:3].astype(int)})
	impact_df['Impact'] = impact_df['Actual'] / impact_df['Predicted']
	impact_df['Impact'] = impact_df['Impact'].round(2)
	impact_df['Excessive Deaths'] = impact_df['Actual'] - impact_df['Predicted']
	impact_df['Excessive Deaths'] = impact_df['Excessive Deaths']

	data1 = pd.concat([data_16_19_mean, data_20_21_mean])
	ax = data1.plot(x='YearStart', y=keyword, kind='line', marker=None, color='black')
	plt.xlabel('Year')
	plt.ylabel(f"{keyword} (%)")
	plt.title(f"{keyword} (%)")
	plt.grid()
	for x, y in zip(data1['YearStart'], data1[keyword]):
			label = "{:.0f}".format(y)
	X_all = data1[['YearStart']]
	y_pred_all = reg.predict(X_all)
	plt.plot(X_all, y_pred_all, linestyle='--', color='black')
	plt.legend(['Data', f'Prediction (R-squared: {r_squared:.3f})'], loc='upper left')
	fig=plt.figure(1)
	plt.savefig(f'{keyword}.png',dpi=fig.dpi,bbox_inches='tight')
	plt.show()
	impact_df.to_csv(f'{keyword} impact.xlsx', index=False)



def main():
    causes_menu = ["Stroke", "Acute Myocardial Infarction (Heart Attack)", "Heart Failure", "Coronary Heart Disease", "Major Cardiovascular Disease", "Diseases of the Heart (Heart Disease)"]
    print("Choose a cause:")
    for idx, cause in enumerate(causes_menu, start=1):
        print(f"{idx}. {cause}")

    choice = int(input("Enter the number corresponding to the cause: ")) - 1
    selected_cause = causes_menu[choice]
    
    if selected_cause in causes_menu:
        plot_cause(selected_cause)
    else:
        print("Invalid cause selection.")

if __name__ == "__main__":
    main()