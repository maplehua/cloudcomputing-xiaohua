from app.search import PaperSearch
s = PaperSearch()
(t, m) = s.results('Approximate', 0)
print t
for i in m:
    print i
