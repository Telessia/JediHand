def get_number_images(labels):
  numbers = []
  models = db.tests
  for image_name in labels:
    numbers.append(models.count_documents({"groupname": image_name}))
    #print(numbers[-1])
  return numbers



def extract_head2(): #Function that get the header of our base signs
  letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
  extracted = []
  models = db.models
  for x in letters: #We will loop over all the base groupnames
    result = models.find_one({"groupname": x })
    #print(result['_id'])
    extracted.append(result)
  return extracted