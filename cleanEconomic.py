import os
import pandas as pd

economic_dir = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/economic_all_data'
output_file = os.path.join(economic_dir, 'ecom_data.csv')

def expand_quarter_to_months(quarter_str):
    year, q = quarter_str.split()
    month_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
    start_month = int(month_map[q])
    return [f"{year}-{str(m).zfill(2)}-01" for m in range(start_month, start_month + 3)]

def detect_frequency(dates):
    if all('Q' in d for d in dates):
        return 'quarterly'
    elif all('-' in d and len(d) == 10 for d in dates):
        return 'monthly'
    return 'multi_month'

all_data = []

for filename in os.listdir(economic_dir):
    if not filename.endswith('.csv'):
        continue

    filepath = os.path.join(economic_dir, filename)
    df = pd.read_csv(filepath)

    metric_name = filename.replace('.csv', '')
    df = df.rename(columns={df.columns[0]: 'State'})
    date_columns = df.columns[1:]
    frequency = detect_frequency(date_columns)

    if frequency == 'monthly':
        df_melted = df.melt(id_vars='State', var_name='Date', value_name='Value')
        df_melted['YearMonth'] = df_melted['Date'].str[:7]
        df_melted['Metric'] = metric_name
        all_data.append(df_melted)

    elif frequency == 'quarterly':
        for col in date_columns:
            month_dates = expand_quarter_to_months(col)
            temp_df = df[['State', col]].copy()
            temp_df[col] = temp_df[col] / 3  # dividir por 3
            for i, date_str in enumerate(month_dates):
                temp_month = temp_df.copy()
                temp_month['Date'] = date_str
                temp_month['YearMonth'] = date_str[:7]
                temp_month['Value'] = temp_month[col]
                temp_month['Metric'] = metric_name
                all_data.append(temp_month[['State', 'Date', 'YearMonth', 'Value', 'Metric']])

    else:  # multi-month (e.g., 3-month gaps)
        for i, col in enumerate(date_columns[:-1]):
            curr_date = pd.to_datetime(col)
            next_date = pd.to_datetime(date_columns[i + 1])
            delta = (next_date - curr_date).days // 30
            if delta == 0: delta = 1
            temp_df = df[['State', col]].copy()
            temp_df[col] = temp_df[col] / delta
            for m in range(delta):
                month_date = (curr_date + pd.DateOffset(months=m)).strftime('%Y-%m-01')
                temp_month = temp_df.copy()
                temp_month['Date'] = month_date
                temp_month['YearMonth'] = month_date[:7]
                temp_month['Value'] = temp_month[col]
                temp_month['Metric'] = metric_name
                all_data.append(temp_month[['State', 'Date', 'YearMonth', 'Value', 'Metric']])

# Concatenar tudo
final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df[['State', 'Date', 'YearMonth', 'Value', 'Metric']]
final_df.to_csv(output_file, index=False)
print(f"Ficheiro criado em: {output_file}")