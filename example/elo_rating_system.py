from elorating.rating_system import EloRatingSystem

rs = EloRatingSystem()
for i in range(12):
    for _ in range(120):
        rs.set_result('p1', f'p{i+2}', 1)

print(rs.leadboard(10))

rs.set_rating('p1', 2400)
rs.set_rating('p2', 1000)
rs.set_result('p1', 'p2', 0, 'game1')
print(rs['p1'], rs['p2'])
rs.set_result('p2', 'p1', 1, 'game1')
print(rs['p1'], rs['p2'])
