import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
# import os
data = pd.read_csv('Raw Database.csv')
data['Description'] = data['Description'].str.strip()

# Dropping all transactions which were done on credit
data = data[~data['InvoiceNo'].str.contains('C')]

# Transactions done in France
basket_France = (data[data['Country'] =="France"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

# Transactions done in the United Kingdom
basket_UK = (data[data['Country'] =="United Kingdom"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

# Transactions done in Portugal
basket_Por = (data[data['Country'] =="Portugal"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

basket_Sweden = (data[data['Country'] =="Sweden"]
        .groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('InvoiceNo'))

basket_France = pd.get_dummies(basket_France).astype(bool)
basket_UK = pd.get_dummies(basket_UK).astype(bool)
basket_Por = pd.get_dummies(basket_Por).astype(bool)
basket_Sweden = pd.get_dummies(basket_Sweden).astype(bool)
#%%
frq_items_France = apriori(basket_France, min_support = 0.05, use_colnames = True)
rules_France = association_rules(frq_items_France, metric ="lift", min_threshold = 1)
rules_France = rules_France.sort_values(['confidence', 'lift'], ascending =[False, False])

frq_items_UK = apriori(basket_UK, min_support = 0.05, use_colnames = True)
rules_UK = association_rules(frq_items_UK, metric ="lift", min_threshold = 1)
rules_UK = rules_UK.sort_values(['confidence', 'lift'], ascending =[False, False])
#%%
frq_items_Por = apriori(basket_Por, min_support = 0.05, use_colnames = True)
rules_Por = association_rules(frq_items_Por, metric ="lift", min_threshold = 1)
rules_Por = rules_Por.sort_values(['confidence', 'lift'], ascending =[False, False])
#%%
frq_items_Sweden = apriori(basket_Sweden, min_support = 0.05, use_colnames = True)
rules_Sweden = association_rules(frq_items_Sweden, metric ="lift", min_threshold = 1)
rules_Sweden = rules_Sweden.sort_values(['confidence', 'lift'], ascending =[False, False])

def predict(antecedent, rules, max_results=6):
    
    # get the rules for this antecedent
    preds = rules[rules['antecedents'] == antecedent]
    
    # a way to convert a frozen set with one element to string
    preds = preds['consequents'].apply(iter).apply(next)
    
    return preds.iloc[:max_results].unique()


print(predict({'SET OF 4 KNICK KNACK TINS LONDON'}, rules=rules_Por))

print(predict({'JAM MAKING SET PRINTED'}, rules=rules_Por))

print(predict({'ASS FLORAL PRINT MULTI SCREWDRIVER'}, rules=rules_Por))

print(predict({'PLASTERS IN TIN STRONGMAN'}, rules=rules_Por))
# basket_France.to_excel(os.getcwd()+'/df.xlsx')
