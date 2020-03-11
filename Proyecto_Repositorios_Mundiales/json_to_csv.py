import os
import json
import csv
from random import randint

#Ya esta todo creado y acomodado para crear el .csv. Falta juntar las dos partes, y fusionar las cosas para que ande todo en conjunto.

#---------------------------PRIMERA PARTE---------------------------

class Analyzed:
    def __init__(self,parameters):
        self.parameters = parameters

    def parameters_quantity(self):
        return len(self.parameters) - 1
    
    def analyze_parameters(self):
        if self.parameters_quantity == 0 or self.parameters[1]=='help':
            return self.show_instruccions()

        if self.parameters_quantity == 1 and self.parameters[1]=='*':
            return self.work_directory(os.getcwd())

        return self.iteration(self.parameters)
    
    def show_instruccions(self):
        message = 'To use this script it is necessary to send 1 or more parameters. These can be files, directories, or the special character '*' that will work with the files in the current directory.'
        print(message)
    
    def work_parameter(self,parameter):
        p_type = ''
        if os.path.isfile(parameter) and os.path.splitext(parameter)[1] == '.json':
            p_type = 'file'
        elif os.path.isdir(parameter):
            p_type = 'directory'
        return p_type

    def work_directory(self,a_directory):
        list_of_files = os.listdir(a_directory)
        return self.iteration(list_of_files)

    def iteration(self,a_list):
        for element in a_list:
            parameter_type = self.work_parameter(element)
            if parameter_type == 'file':
                self.create_new_json(element)
                self.add_to_csv(element)
            if (parameter_type == 'directory'):
                self.work_directory(element)



#--------------------------- SEGUNDA PARTE ---------------------------
def load_features(repository,repositories_features_dictionary):
    ''' This function load each feature of each repository, and in each 
        iteration (with a new repository) update the heading, and the dictionaries
        of content type and languages '''
    try:
        repositories_features_dictionary['repository_name'] = repository['repository_metadata']['name'][0]['name']
    except KeyError:
        random_number = randint(0,1000)
        repositories_features_dictionary['repository_name'] = 'repository_NN(hash_{})'.format(random_number)
    try:
        repositories_features_dictionary['repository_organisation_name'] = repository['organisation']['name'][0]['name']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_latitude'] = repository['organisation']['location']['latitude']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_longitude'] = repository['organisation']['location']['longitude']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_country'] = repository['organisation']['country']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_type'] = repository['policies']['content_policy']['repository_type']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_access'] = repository['policies']['metadata_policy']['access']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['respository_status'] = repository['repository_metadata']['repository_status']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_software'] = repository['repository_metadata']['software']['version']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_software_version'] = repository['repository_metadata']['software']['name']
    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_languages'] = repository['repository_metadata']['content_languages']
        for language in repositories_features_dictionary['repository_languages']:
            if language not in languages_dictionary:
                languages_dictionary['language_{}'.format(language)] = len(heading)
                heading.append('language_{}'.format(language))

    except KeyError:
        pass
    try:
        repositories_features_dictionary['repository_content_types'] = repository['repository_metadata']['content_types']
        for content in repositories_features_dictionary['repository_content_types']:
            if content not in content_type_dictionary:
                content_type_dictionary['content_type_{}'.format(content)] = len(heading)
                heading.append('content_type_{}'.format(content))
    except KeyError:
        pass

    return repositories_features_dictionary


def update_languages_and_content_types():
    repos_names = list(repositories_dictionary.keys())
    dict_languages_length = len(languages_dictionary)
    dict_content_length = len(content_type_dictionary)
    for repos in repos_names:
        all_values = []
        if repositories_dictionary[repos]['repository_languages'] is not None:
            languages_aux = repositories_dictionary[repos]['repository_languages'].copy() #Aca guardo provisoriamente los lenguajes de repos
            aux = [] # Lista que voy a usar para poner todos sus elementos en false y extender su tamanio en relacion al diccionario de lenguajes para que coincidan con la longitud del heading
            for i in range(0,dict_languages_length): #Ac
                aux.append(False)
        if repositories_dictionary[repos]['repository_content_types'] is not None:#Mismo procedimiento que hicimos para lenguajes, ahora con content_types
            content_aux = repositories_dictionary[repos]['repository_content_types'].copy()
            aux2 = []
            for i in range(0,dict_content_length):
                aux2.append(False)
        repos_features_aux = repositories_features_dictionary.copy() # Creo una lista con todas las features de los repos, excepto language y content_type
        repos_features_aux.remove('repository_content_types')
        repos_features_aux.remove('repository_languages')
        aux.extend(aux2) # Uno ambas listas con todo en false, para poder hacer el extend con all_values
        for feature in repos_features_aux:
            all_values.append(repositories_dictionary[repos][feature]) # Agrego cada valor del diccionario de repos
        all_values.extend(aux) # Aca el length del heading es igual al length de all_values
        for l in languages_aux:
            all_values[languages_dictionary['language_{}'.format(l)]] = True
        for c in content_aux:
            all_values[content_type_dictionary['content_type_{}'.format(c)]] + True #Los dos ultimos ponen los valores en True, de los lenguajes y contenidos de cada repo
        total_rows.append(all_values) # Vacío las variables que ya no uso
        aux.clear()
        aux2.clear()
        languages_aux.clear()
        content_aux.clear()
        all_values.clear()


#--------------------------- PROGRAMA PRINCIPAL ---------------------------


with open('/home/german/Escritorio/repository-data/json_0.php') as a_file:
    data = json.load(a_file)

total_rows = []

repositories_dictionary = {} #Se carga dinamicamente durante la ejecucion del script

repositories_features_dictionary = {'repository_name':'?', 'repository_organisation_name':'?', 'repository_latitude':'?','repository_longitude':'?', 
                        'repository_country':'?','repository_type':'?', 'repository_access': '?','respository_status':'?', 'repository_software':'?',
                         'repository_software_version':'?','repository_languages':[], 'repository_content_types':'?' }


heading = ['-']
heading.extend(list(repositories_features_dictionary.keys())[0:10]) #Cargo las caractericas de los repos, excepto los lenguajes y los contenidos, que se agregaran dinamicamente despues.

languages_dictionary = {} 
content_type_dictionary = {}
results_list = []

for i in range(0,len(data['items'])):
    repositories_features_dictionary = load_features(data['items'][i],repositories_features_dictionary)
    repositories_dictionary[repositories_features_dictionary['repository_name']] = repositories_features_dictionary.copy() # Cargo las caracteristicas de los repo, al diccionario de repos.

update_languages_and_content_types()

#Aca seguiria con la carga del csv