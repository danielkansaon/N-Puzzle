# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = "Filipe Ribeiro"
import json, os

education_status_grouped = {                                             
    'college':['UNDERGRAD','ALUM','SOME_COLLEGE','ASSOCIATE_DEGREE'],
    "high_school":['high_school','HIGH_SCHOOL_GRAD','SOME_HIGH_SCHOOL'],
    'grad_school':['IN_GRAD_SCHOOL','SOME_GRAD_SCHOOL','MASTER_DEGREE','PROFESSIONAL_DEGREE','DOCTORATE_DEGREE'],                  
}

racial_affinities = {
#         'all': [],                         
    'african_american': {"id":"6018745176183","name":"African American (US)"},
    'asian_american': {"id":"6021722613183","name":"Asian American (US)"},
    'hispanic_all': {"id":"6003133212372","name":"Hispanic (US - All)"},
    'other': 'dealt with specially' #excluded
#         'hispanic_bilingual': [{"id":"6009609054383","name":"Hispanic (US - Bilingual)"}],
#         'hispanic_english': [{"id":"6009609045383","name":"Hispanic (US - English dominant)"}],
#         'hispanic_spanish':     [{"id":"6009609033583","name":"Hispanic (US - Spanish dominant)"}],
    # this goes into behaviors in exclusions     
}

caucasian_spec = {
    "behaviors":[
        {"id":"6018745176183","name":"African American (US)"},
        {"id":"6021722613183","name":"Asian American (US)"},
        {"id":"6003133212372","name":"Hispanic (US - All)"}
    ]
} 
# people's political leaning. goes into politics in flexible_spec
political_alignment = {
#     "all": [],
    "conservative": [{"id":"6015760532183","name":"US politics (conservative)"}],
    "liberal": [{"id":"6015760027783","name":"US politics (liberal)"}],
    "moderate": [{"id":"6015760036783","name":"US politics (moderate)"}],
    "very_conservative": [{"id":"6015762142783","name":"US politics (very conservative)"}],
    "very_liberal": [{"id":"6015759997983","name":"US politics (very liberal)"}]  
            
}

# People whose activity on Facebook suggests that they're more likely to engage with/distribute liberal political content 
political_engagement ={
    "conservative": [{"id":"6029977111383","name":"US politics engagement (conservative)"}],
    "liberal": [{"id":"6031978535383","name":"US politics engagement (liberal)"}],
    "moderate": [{"id":"6031978554983","name":"US politics engagement (moderate)"}],
}

relationship_statuses = {
#         'all':[],
    'single' :[1], # ** audience insights does not include divorced, widowed, etc
    'in_relationship':[2],
    'engaged': [4],         
    'married':[3], 
    'civil_union': [7],
    'domestic_partnership':[8],
    'open_relationship': [9],
    'complicated': [10],
    'separated': [11],
    'divorced': [12],
    'widowed': [13],   
    'unspecified':[6]             
}
    

income_levels={
    '30k_to_40k':[{"id": "6018510070532","name": "$30,000 - $40,000"}],                 
    '40k_to_50k':[{"id": "6018510087532","name": "$40,000 - $50,000"}],
    '50k_to_75k':[{"id": "6018510122932","name": "$50,000 - $75,000"}],        
    '75k_to_100k':[{"id": "6018510100332","name": "$75,000 - $100,000"}],
    '100k_to_125k':[{"id": "6018510083132","name": "$100,000 - $125,000"}],
    '125k_to_150k':[{"id": "6017897162332","name": "$125,000 - $150,000"}],
    '150k_to_250k':[{"id": "6017897374132","name": "$150,000 - $250,000"}],
    '250k_to_350k':[{"id": "6017897397132","name": "$250,000 - $350,000"}], 
    '350k_to_500k':[{"id": "6017897416732","name": "$350,000 - $500,000"}],
    'over_500k':[{"id": "6017897439932","name": "Over $500,000"}]                                                            
}

brazilian_regions={
    'south':['parana','rio_grande_do_sul','santa_catarina'],
    "southeast":['espirito_santo','minas_gerais','rio_de_janeiro','sao_paulo'],
    'north':['acre','amapa','amazonas', 'para', 'rondonia','roraima','tocantins'],
    "northeast":['alagoas','bahia','ceara','maranhao','paraiba','pernambuco', 'piaui','rio_grande_do_norte','sergipe'],    
    'midwest':['distrito_federal','goias','mato_grosso','mato_grosso_do_sul'],                 
}

age_intervals = {     
    'adolescent' :{'age_min': 13, 'age_max': 17},
    'young_1' :{'age_min': 18, 'age_max': 24},
    'young_2' :{'age_min': 25, 'age_max': 34},
    'mid_aged_1' :{'age_min': 35, 'age_max': 44},
    'mid_aged_2' :{'age_min': 45, 'age_max': 54},        
    'old_1': {'age_min': 55, 'age_max': 64},
    'old_2': {'age_min': 65}                              
}

genders = {
#     "all": [],            
    'male': [1],
    'female': [2]
}

translation_dict={
        "political_alignment":"Political Alignment"
        ,"political_engagement":"Political Engagement"
        ,"education_status_grouped":"Education Level"
        ,"relationship_statuses":"Relationship Status"
        ,"gender":"Gender"
        ,"income_levels":"Income Level"
        ,"age_intervals":"Age"
        ,"racial_affinities":"Racial Affinties"
        ,"expat":"Expats"
        ,"language":"Language"   
        ,"high_school":"High School"
        ,"very_conservative": "Very Conservative"
        ,"very_liberal": "Very Liberal"
        ,"moderate": "Moderate"
        ,"liberal": "Liberal"
        ,"conservative": "Conservative"
        ,"grad_school": "Grad School"
        ,"high_school": "High School"
        ,"college": "College"
        ,"separated": "Separated"
        ,"widowed": "Widowed"
        ,"open_relationship": "Open Relationship"
        ,"domestic_partnership": "Domestic Partnership"
        ,"engaged": "Engaged"
        ,"single": "Single"
        ,"complicated": "Complicated"
        ,"civil_union": "Civil Union"
        ,"in_relationship": "In Relationship"
        ,"divorced": "Divorced"
        ,"married": "Married"
        ,"unspecified": "Unspecified"
        ,"male": "Male"
        ,"female": "Female"
        ,"40k_to_50k": "40k to 50k"
        ,"150k_to_250k": "150k to 250k"
        ,"30k_to_40k": "30k to 40k"
        ,"100k_to_125k": "100k to 125k"
        ,"250k_to_350k": "250k to 350k"
        ,"over_500k": "over 500k"
        ,"75k_to_100k": "75k to 100k"
        ,"350k_to_500k": "350k to 500k"
        ,"50k_to_75k": "50k to 75k"
        ,"125k_to_150k": "125k to 150k"   
        ,"young_2": "25-34"
        ,"mid_aged_1": "35-44"
        ,"mid_aged_2": "45-54"
        ,"adolescent": "Under 18"
        ,"old_1": "55-64"
        ,"old_2": "Above 65"
        ,"young_1": "18-24"
        ,"other": "Caucasian"
        ,"hispanic_all": "Hispanic"
        ,"asian_american": "Asian American"
        ,"african_american": "African American"}

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))    
    dicts_file = open('%s/audiencia_presidentes.json' % dir_path, 'r')     
#     dicts_file = open('/home/filipe/Desktop/audiencia_presidentes.json', 'r')  
    
    for line in dicts_file:
        print line
        json_line = json.loads(line.strip())
#         ad_id = json_line.keys()[0]
        raw_values_dict = json_line['raw_values_dict']
        percent_values_dict = json_line['percent_values_dict']
        name = json_line['name']
        num_likes = json_line['num_likes']
        print 'NAME: %s' % name
        print 'NUM_LIKES: %s' % num_likes
#         print 'URL: %s' % json_line[ad_id]['url']
        print '%s' % translation_dict['education_status_grouped']
        for scholarity_field in education_status_grouped:
            print '\t%s' % (translation_dict[scholarity_field])
            print '\t\tRaw value: %d' % raw_values_dict['education_status_grouped'][scholarity_field]
            print '\t\tPercent value: %.2f' % (percent_values_dict['education_status_grouped'][scholarity_field]*100)
        
                                       
        print '%s' % translation_dict['relationship_statuses']        
        for relationship_status in relationship_statuses:
            print '\t%s' % (translation_dict[relationship_status])
            print '\t\tRaw value: %d' % raw_values_dict['relationship_status'][relationship_status]
            print '\t\tPercent value: %.2f' % (percent_values_dict['relationship_status'][relationship_status]*100)

        print 'brazilian_regions'            
        for region in brazilian_regions:
            print '\t%s' % (region)
            print '\t\tRaw value: %d' % raw_values_dict['brazilian_regions'][region]
            print '\t\tPercent value: %.2f' % (percent_values_dict['brazilian_regions'][region]*100)    
        
        print '%s' % translation_dict['age_intervals']                 
        for age_group in age_intervals:
            print '\t%s' % (translation_dict[age_group])
            print '\t\tRaw value: %d' % raw_values_dict['age_intervals'][age_group]
            print '\t\tPercent value: %.2f' % (percent_values_dict['age_intervals'][age_group]*100)              
                   

        print '%s' % translation_dict['gender']   
        for gender in genders:  
            print '\t%s' % (translation_dict[gender])
            print '\t\tRaw value: %d' % raw_values_dict['gender'][gender]
            print '\t\tPercent value: %.2f' % (percent_values_dict['gender'][gender]*100)                     

if __name__ == "__main__":
    main()