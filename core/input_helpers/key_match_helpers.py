from difflib import SequenceMatcher

staff_salary_keys = ('Designation', 'No. of Persons', 'Monthly Salary (in BDT)',
       'Annual Salary (BDT in lac)')

def staff_salary_matcher(df):
    for col in df.columns:
        if col not in staff_salary_keys:
            diff_list = [SequenceMatcher(None, col, i).ratio() for i in staff_salary_keys]
            diff_list.index(max(diff_list))
            df = df.rename(columns={col : staff_salary_keys[diff_list.index(max(diff_list))]})

    return df
