import requests
import json

'''
* Add 5 users - Swati, Himanshu, Amit, Wriddha, Haarish

* Add expenditure (Breakfast, 1000) from Swati add contributors (Haarish, 200), (Swati, 200), 
(Himanshu, 300) and (Wriddha, 300)

* Fetch Haarish contributions
'''

def get_user_body(name: str, email: str, gender: str):
    return {
        'name': name,
        'email': email,
        'password': "Test@123",
        'gender': gender,
        'confirm_password': "Test@123"
    }

def get_auth_details_for_user(email: str):
    return {
        'email': email,
        'password': "Test@123"
    }

def add_users(baseUrl: str):
    # Add Swati as user
    response = requests.post(baseUrl + '/users', json=get_user_body('Swati', 'swati@gmail.com', 'Female'))
    assert response.status_code == 201
    
    # Add Himanshu as user
    response = requests.post(baseUrl + '/users', json=get_user_body('Himanshu', 'himanshu@gmail.com', 'Male'))
    assert response.status_code == 201

    # Add Roshan as user
    response = requests.post(baseUrl + '/users', json=get_user_body('Roshan', 'roshan@gmail.com', 'Male'))
    assert response.status_code == 201

    # Add Rahul as user
    response = requests.post(baseUrl + '/users', json=get_user_body('Rahul', 'rahul@gmail.com', 'Male'))
    assert response.status_code == 201

    # Add Haarish as user
    response = requests.post(baseUrl + '/users', json=get_user_body('Haarish', 'haarishkhan@gmail.com', 'Male'))
    assert response.status_code == 201

def delete_users(baseUrl: str, swatiAuthData, himanshuAuthData, roshanAuthData, rahulAuthData, haarishAuthData):
    # Delete Swati as user
    response = requests.delete(baseUrl + '/users/' + swatiAuthData['Id'], 
                               headers={'Authorization': 'Bearer ' + swatiAuthData['Token'] })
    assert response.status_code == 204

    # Delete Himanshu as user
    response = requests.delete(baseUrl + '/users/' + himanshuAuthData['Id'], 
                               headers={'Authorization': 'Bearer ' + himanshuAuthData['Token'] })
    assert response.status_code == 204

    # Delete Roshan as user
    response = requests.delete(baseUrl + '/users/' + roshanAuthData['Id'], 
                               headers={'Authorization': 'Bearer ' + roshanAuthData['Token'] })
    assert response.status_code == 204

    # Delete Rahul as user
    response = requests.delete(baseUrl + '/users/' + rahulAuthData['Id'], 
                               headers={'Authorization': 'Bearer ' + rahulAuthData['Token'] })
    assert response.status_code == 204

    # Delete Haarish as user
    response = requests.delete(baseUrl + '/users/' + haarishAuthData['Id'], 
                               headers={'Authorization': 'Bearer ' + haarishAuthData['Token'] })
    assert response.status_code == 204

def login_user(baseUrl: str, authData):
    response = requests.post(baseUrl + '/users/auth', json = authData)
    assert response.status_code == 200
    return json.loads(response.text)

def add_expenditure_of_user(baseUrl: str, expenditureName: str, expenditureAmount: int, userAuthData):
    response = requests.post(baseUrl + '/expenditures', 
                  headers={'Authorization': 'Bearer ' + userAuthData['Token'] },
                  json={
                        "name": expenditureName,
                        "userid": userAuthData['Id'],
                        "amount": expenditureAmount
                  })
    assert response.status_code == 201
    return json.loads(response.text)['New expenditure']['id']

def get_all_expenditures_for_user(baseUrl: str, userAuthData):
    response = requests.get(baseUrl + '/expenditures/' + userAuthData['Id'], 
                headers={'Authorization': 'Bearer ' + userAuthData['Token'] })
    assert response.status_code == 200
    return json.loads(response.text)['Expenditures']

def update_expenditure_of_user(baseUrl: str, expenditureId: str, userAuthData, newName: str, newAmount: int):
    response = requests.put(baseUrl + '/expenditures/' + expenditureId, 
                headers={'Authorization': 'Bearer ' + userAuthData['Token'] },
                json={
                    'userid': userAuthData['Id'],
                    'name': newName,
                    'amount': newAmount
                })
    assert response.status_code == 200
    return

def delete_expenditure_of_user(baseUrl: str, expenditureId: str, userAuthData):
    response = requests.delete(baseUrl + '/expenditures/' + expenditureId, 
                    headers={'Authorization': 'Bearer ' + userAuthData['Token'] })
    assert response.status_code == 204
    return

def verify_expenditures(baseUrl: str, user1AuthData, user2AuthData):
    # Add an expenditure (Food, 500) and (Travel, 100) for the given user1
    user1FoodExpenditureId = add_expenditure_of_user(baseUrl=baseUrl,
                            expenditureName='Food',
                            expenditureAmount=500,
                            userAuthData=user1AuthData)
    user1TravelExpenditureId = add_expenditure_of_user(baseUrl=baseUrl,
                            expenditureName='Travel',
                            expenditureAmount=100,
                            userAuthData=user1AuthData)
    
    # Add an expenditure (Party, 800) and (Snacks, 100) for the given user2
    user2PartyExpenditureId = add_expenditure_of_user(baseUrl=baseUrl,
                            expenditureName='Party',
                            expenditureAmount=800,
                            userAuthData=user2AuthData)
    user2SnacksExpenditureId = add_expenditure_of_user(baseUrl=baseUrl,
                            expenditureName='Snacks',
                            expenditureAmount=100,
                            userAuthData=user2AuthData)

    # Verify the added expenditures of user1
    user1Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user1AuthData)
    for i in range(0, user1Expenditures.__len__()):
        name: str = 'Food'
        amount: int = 500
        if user1Expenditures[i]['name'] != 'Food':
            name = 'Travel'
            amount = 100
        assert user1Expenditures[i]['name'] == name
        assert user1Expenditures[i]['amount'] == amount
        assert user1Expenditures[i]['userid'] == user1AuthData['Id']

    # Verify the added expenditures of user2
    user2Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user2AuthData)
    for i in range(0, user1Expenditures.__len__()):
        name = 'Party'
        amount = 800
        if user2Expenditures[i]['name'] != 'Party':
            name = 'Snacks'
            amount = 100
        assert user2Expenditures[i]['name'] == name
        assert user2Expenditures[i]['amount'] == amount
        assert user2Expenditures[i]['userid'] == user2AuthData['Id']

    # Update expenditure 'Food' to 600 of user1
    update_expenditure_of_user(baseUrl=baseUrl, 
                               expenditureId=user1FoodExpenditureId,
                               userAuthData=user1AuthData,
                               newName='Food',
                               newAmount=600)
    # Update expenditure 'Travel' to 50 of user1
    update_expenditure_of_user(baseUrl=baseUrl, 
                               expenditureId=user1TravelExpenditureId,
                               userAuthData=user1AuthData,
                               newName='Travel',
                               newAmount=50)
    # Verify the update
    user1Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user1AuthData)
    for i in range(0, user1Expenditures.__len__()):
        name = 'Food'
        amount = 600
        if user1Expenditures[i]['name'] != 'Food':
            name = 'Travel'
            amount = 50
        assert user1Expenditures[i]['name'] == name
        assert user1Expenditures[i]['amount'] == amount
        assert user1Expenditures[i]['userid'] == user1AuthData['Id']

    # Update expenditure 'Party' to 'Parties' of user2
    update_expenditure_of_user(baseUrl=baseUrl, 
                               expenditureId=user2PartyExpenditureId,
                               userAuthData=user2AuthData,
                               newName='Parties',
                               newAmount=1000)
    update_expenditure_of_user(baseUrl=baseUrl, 
                               expenditureId=user2SnacksExpenditureId,
                               userAuthData=user2AuthData,
                               newName='Full day food',
                               newAmount=1200)
    # Verify the update
    user2Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user2AuthData)
    for i in range(0, user1Expenditures.__len__()):
        name = 'Parties'
        amount = 1000
        if user2Expenditures[i]['name'] != 'Parties':
            name = 'Full day food'
            amount = 1200
        assert user2Expenditures[i]['name'] == name
        assert user2Expenditures[i]['amount'] == amount
        assert user2Expenditures[i]['userid'] == user2AuthData['Id']

    # Delete expenditure (Food, 600) of user1
    delete_expenditure_of_user(baseUrl=baseUrl, expenditureId=user1FoodExpenditureId, userAuthData=user1AuthData)
    # Verify the delete
    user1Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user1AuthData)
    assert user1Expenditures.__len__() == 1
    for i in range(0, user1Expenditures.__len__()):
        name = 'Food'
        amount = 600
        if user1Expenditures[i]['name'] != 'Food':
            name = 'Travel'
            amount = 50
        assert user1Expenditures[i]['name'] == name
        assert user1Expenditures[i]['amount'] == amount
        assert user1Expenditures[i]['userid'] == user1AuthData['Id']

    # Delete all expenditures of user2
    delete_expenditure_of_user(baseUrl=baseUrl, expenditureId=user2PartyExpenditureId, userAuthData=user2AuthData)
    delete_expenditure_of_user(baseUrl=baseUrl, expenditureId=user2SnacksExpenditureId, userAuthData=user2AuthData)
    user2Expenditures = get_all_expenditures_for_user(baseUrl=baseUrl, userAuthData=user2AuthData)
    assert user2Expenditures.__len__() == 0
    pass

def test_expenditure_contributors():
    baseUrl: str = 'http://127.0.0.1:8000'

    add_users(baseUrl=baseUrl)

    # Authenticate Swati by getting JWT token
    swatiAuthData = login_user(baseUrl, get_auth_details_for_user('swati@gmail.com'))

    # Authenticate Himanshu by getting JWT token
    himanshuAuthData = login_user(baseUrl, get_auth_details_for_user('himanshu@gmail.com'))

    # Authenticate Roshan by getting JWT token
    roshanAuthData = login_user(baseUrl, get_auth_details_for_user('roshan@gmail.com'))

    # Authenticate Rahul by getting JWT token
    rahulAuthData = login_user(baseUrl, get_auth_details_for_user('rahul@gmail.com'))

    # Authenticate Haarish by getting JWT token
    haarishAuthData = login_user(baseUrl, get_auth_details_for_user('haarishkhan@gmail.com'))


    # Verify expenditures API
    verify_expenditures(baseUrl=baseUrl, user1AuthData=swatiAuthData, user2AuthData=himanshuAuthData)

    # Add expenditure (Breakfast, 1000) from Swati
    # Add contributor (Haarish, 200), (Swati, 200), (Roshan, 300) and (Rahul, 300)

    delete_users(baseUrl=baseUrl, 
                 swatiAuthData=swatiAuthData,
                 himanshuAuthData=himanshuAuthData,
                 roshanAuthData=roshanAuthData,
                 rahulAuthData=rahulAuthData,
                 haarishAuthData=haarishAuthData)

