labels_skeleton = ['A',"B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def extract_skeletons(labels, number_image): #Function that get the header of our base signs
  #letters = ['A',"B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  
  dictionary_skeletons = {}
  value_to_get = len(labels) * number_image
  print("Value : ", value_to_get)

  for image_name in labels: # create the dictionary
    dictionary_skeletons[image_name] = []

  models = db.models
  datas = models.find() #retrieve a cursor on all the DB
  for data in datas:
    
    if(value_to_get == 0): break

    #print(data['groupname'])
    if(len(dictionary_skeletons[data['groupname']]) < number_image):
      value_to_get -= 1
      tabTempo = np.multiply(data['skeleton'], 100)
      dictionary_skeletons[data['groupname']].append(tabTempo)


  return dictionary_skeletons