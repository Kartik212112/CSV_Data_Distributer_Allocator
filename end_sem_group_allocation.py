import pandas as pd 
import os
import math

def group_allocation(filename, number_of_groups):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    student_df = pd.read_csv(os.path.join(os.getcwd(), filename))

    os.mkdir(os.path.join(os.getcwd(),'groups'))
    os.chdir(os.path.join(os.getcwd(),'groups'))
    
    student_df['BRANCH_CODE'] = student_df['Roll'].apply(lambda x: x[4:6])
   
    branch_strength_df =  student_df.groupby(['BRANCH_CODE']).size().reset_index(name='STRENGTH').sort_values(['STRENGTH','BRANCH_CODE'], ignore_index = True, ascending = [False,True] )
    with open('branch_strength.csv', 'w', newline= '') as f:
        branch_strength_df.to_csv(f, index = False)
 
    for branch_code in branch_strength_df['BRANCH_CODE']:
        temp_df= student_df[student_df['BRANCH_CODE'] == branch_code]
        branch_details_df = temp_df[['Roll', 'Name', 'Email']].sort_values('Roll', ignore_index = True)
        with open(branch_code +'.csv', 'w', newline= '') as f:
            branch_details_df.to_csv(f, index = False)
    
    for number in range(number_of_groups):
        group_name = 'Group_G' + str(number + 1).zfill(2)
        branch_strength_df[group_name] = branch_strength_df['STRENGTH'].apply(lambda x: math.floor(x/number_of_groups))
    
    branch_strength_df['left'] = branch_strength_df['STRENGTH'].apply(lambda x : x % number_of_groups)

    group_index = row = 0 

    for i in range(branch_strength_df['left'].sum()):
        if group_index == number_of_groups:
            group_index = 0

        branch_strength_df.iloc[row, group_index + 2] += 1
        branch_strength_df.loc[row, 'left'] -= 1
        
        if branch_strength_df.loc[row, 'left'] == 0:
            row += 1
        group_index += 1    
    
    branch_strength_row  = 0

    for branch in branch_strength_df['BRANCH_CODE']:
        branch_details_row = 0
        branch_details_df = pd.read_csv(os.path.join(os.getcwd(), branch + '.csv'))
  
        for group_index in range(number_of_groups):
           
            group_name = 'Group_G' + str(group_index + 1).zfill(2)
            group_strength = branch_strength_df.loc[branch_strength_row, group_name]
            
            group_name_df = branch_details_df.loc[branch_details_row : branch_details_row + group_strength - 1]
            
            if branch == branch_strength_df.iloc[0,0]:
                group_name_df.to_csv(group_name + '.csv', mode = 'a', index = False)
            else:
                 group_name_df.to_csv(group_name + '.csv', mode = 'a', index = False, header = False)
            
            branch_details_row += group_strength   
                   
        
        branch_strength_row += 1


   
    stats_df = pd.DataFrame(columns = ['group', 'total'])

    for group_index in range(number_of_groups):
        group_name = 'Group_G' + str(group_index + 1).zfill(2)
        stats_df.loc[group_index,'group'] = group_name + '.csv'
        stats_df.loc[group_index,'total'] = branch_strength_df[group_name].sum()
        
        row = 0
        for branch in branch_strength_df['BRANCH_CODE']:
            stats_df.loc[group_index, branch] = branch_strength_df.loc[row, group_name]
            row += 1
            stats_df[branch] = stats_df[branch].astype(int)          
           
    stats_df.to_csv('stats_grouping.csv', index = False)

        
filename = "Btech_2020_master_data.csv"
number_of_groups = 12
group_allocation(filename, number_of_groups)