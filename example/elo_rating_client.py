from elorating.rpc.client import Client

if __name__ == '__main__':
    client = Client('127.0.0.1')
    for i in range(12):
        for _ in range(120):
            client.set_result('p1', f'p{i+2}', 1)

    print(client.leadboard(10))

    client.set_rating('p1', 2400)
    client.set_rating('p2', 1000)
    client.set_result('p1', 'p2', 0, 'game1')
    print(client['p1'], client['p2'])
    client.set_result('p2', 'p1', 1, 'game1')
    print(client['p1'], client['p2'])
