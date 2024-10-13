import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# location of CSV to uploada
file_location = r"C:\Users\jonse\Downloads\archive\adult_data.csv"
#upload file 
initial_import = pd.read_csv(file_location)
#test upload - only uncomment on first run
#print(initial_import.head()) #confirm data has loaded 
#filter columns needed for first analysis of impact of age and education on salary 
age_education_salary = initial_import[['age','education','salary']]

#filter the education into groups 
education_mapping = {'HS-grad':"HS","9th":'Not Complete',"11th":'Not Complete','Masters':'Masters',
                     'Bachelors':'Bachelors', 'Some-college': "HS",'Doctorate':'Doctorate',"5th-6th":'Not Complete',
                     '10th':'Not Complete','1st-4th':'Not Complete','Preschool':'Not Complete','12th':'Not Complete',
                     'Prof-school':'Other','Assoc-acdm':'Other','Assoc-voc':'Other','7th-8th':'Not Complete'}
age_education_salary.loc[:,'education'] = age_education_salary['education'].replace(education_mapping)

#confirm mapping has occured
#print(age_education_salary['education'].unique())

#create age bins 
bins = [20,30,40,50,60,100]
label = ['20-30','31-40','41-50','51-60','60+']

age_education_salary.loc[:,'age_group'] = pd.cut(age_education_salary['age'],bins=bins,labels=label,right=False)
#for this chart we want to see people with salary over 50k p/a - this is filtered here 
age_education_salary_over50 = age_education_salary[age_education_salary['salary'] == '>50K']
#check buckets created 
#print(age_education_salary[['age','age_group']])
#pivot the DF in prep for heatmap
age_education_salary_pivot = age_education_salary_over50.pivot_table(values='salary', index='age_group',columns='education',aggfunc='count', fill_value=0)
#confirm its creation
#print(age_education_salary_pivot.head())

##create bar chart from results

age_education_salary_pivot.plot(kind='bar',stacked=True,figsize=(10, 6))

plt.title('Impact of age and education on US Salary Ranges (salary count over 50k p/a)')
plt.ylabel("count of salary")
plt.xlabel("Age group")
plt.xticks(rotation=45)
plt.legend(title='Education')


plt.tight_layout()
plt.show()

#chart shows you are most likley to earn over 50k at the ages of 40-50 if you have finnished HS or have a batchelors
# this though is an absolute amount of people - looking at it as a % of total people with that level of education may give
# a different tale

age_different_perc = age_education_salary[['age_group','education','salary']]

age_different_perc.loc[:,'above_50k'] = age_different_perc['salary'].apply(lambda x:1 if x == '>50K' else 0)

age_grouping = age_different_perc.groupby(['age_group','education']).agg(
    total_adults = ('above_50k', 'count'),
    total_above_50k = ('above_50k', 'sum')
)

age_grouping['%_above50k'] = (age_grouping['total_above_50k']/age_grouping['total_adults']) *100 

print(age_grouping)
