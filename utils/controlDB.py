# DB에 data를 저장하는 API

def saveDataToDB(client, data):
  try:
    client.test.cars.insert_one(data)
    print('Data save success')
  except:
    print('Database connect error')