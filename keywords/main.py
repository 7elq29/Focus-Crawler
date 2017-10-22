from pathlib import Path
from collections import deque
from keywords.ccnetwork import CCNetwork
from keywords.preference import Preference
from recommand.score import Score

if __name__ == "__main__":
    p = Path('../dataset')
    p = [x for x in p.iterdir() if x.is_dir()]

    queue = deque()

    for d in p:
        for file in d.iterdir():
            file.resolve()
            queue.append(open(str(file), "r", errors='ignore').read())

    ccnetwork = CCNetwork()
    ccnetwork.build(queue)
    print("{} words in network".format(len(ccnetwork.network)))
    maxCoocur, word1, word2 = 0, "", ""
    for w1, v1 in ccnetwork.network.items():
        for w2, v2 in v1.items():
            if v2 > maxCoocur and w2 != "_":
                maxCoocur, word1, word2 = v2, w1, w2
    print("the word [{}] and [{}] has the highest relation, score: {}".format(word1, word2, maxCoocur))
    maxCoocur, word = 0, ""
    l = [(x, ccnetwork.network[x]["_"]) for x in ccnetwork.network]
    l.sort(key=lambda x: x[1], reverse=True)
    print("top 20 words {}".format(l[:20]))
    print("bottom 10 words {}".format(l[len(l)-10:]))

    preference = Preference(ccnetwork)
    preference.prefer("software")
    print("words related to [software], {}".format(preference.top()))

    recommand = {}

    for d in p:
        for file in d.iterdir():
            file.resolve()
            recommand[file] = Score.get_score(preference, open(str(file), 'r', errors='ignore').read())

    l = [(x, recommand[x]) for x in recommand]
    l.sort(key=lambda x: x[1], reverse=True)
    print("top 20 recommandation, {}".format(l[:20]))

