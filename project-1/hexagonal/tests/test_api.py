def create(client,title='Write presentation'):
    return client.post('/tasks',json={'title':title,'description':'AS experiment'})
def test_root(client):
    assert client.get('/').status_code == 200
def test_initial_list(client):
    assert client.get('/tasks').json() == []
def test_create_task(client):
    r=create(client);assert r.status_code == 201
    data=r.json();assert data['title']=='Write presentation'
    assert data['status']=='TODO' and data['id'] and data['created_at']
def test_invalid_title(client):
    assert client.post('/tasks',json={'title':''}).status_code == 422
def test_get_task(client):
    task=create(client).json();r=client.get('/tasks/'+task['id'])
    assert r.status_code==200 and r.json()['id']==task['id']
def test_get_missing(client):
    assert client.get('/tasks/unknown').status_code == 404
def test_list_tasks(client):
    create(client,'A');create(client,'B')
    assert len(client.get('/tasks').json()) == 2
def test_update_title(client):
    task=create(client).json();r=client.patch('/tasks/'+task['id'],json={'title':'Updated'})
    assert r.status_code==200 and r.json()['title']=='Updated'
def test_update_status(client):
    task=create(client).json();r=client.patch('/tasks/'+task['id']+'/status',json={'status':'DONE'})
    assert r.status_code==200 and r.json()['status']=='DONE'
def test_invalid_status(client):
    task=create(client).json()
    assert client.patch('/tasks/'+task['id']+'/status',json={'status':'INVALID'}).status_code==422
def test_summary(client):
    a=create(client,'A').json();create(client,'B')
    client.patch('/tasks/'+a['id']+'/status',json={'status':'DONE'})
    assert client.get('/tasks/summary').json()=={'total':2,'todo':1,'done':1}
def test_delete(client):
    task=create(client).json();r=client.delete('/tasks/'+task['id'])
    assert r.status_code==204 and client.get('/tasks/'+task['id']).status_code==404
