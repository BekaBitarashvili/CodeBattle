"""
Run once to seed 30 tasks into the DB.
Usage: flask shell < seed_tasks.py  OR  python seed_tasks.py
"""
import json

TASKS = [
# ══════════════════════════════════════════
#  EASY  (10)
# ══════════════════════════════════════════
dict(
    title="თეატრალური მოედანი",
    difficulty="easy", xp=25, category="Math",
    description="""## თეატრალური მოედანი

ქალაქის მოედანი არის მართკუთხედის ფორმის, ზომებით **n × m** მეტრი.  
მერიამ გადაწყვიტა მოედანი მოაპირკეთოს კვადრატული ფილებით, რომელთა გვერდის სიგრძეა **a**.

მინიმუმ რამდენი ფილაა საჭირო მოედნის სრულად დასაფარად?  
ფილების გატეხვა და გადაკეთება **აკრძალულია**, თუმცა ფილებმა შეიძლება მოედნის საზღვრებს გარეთაც გაიწიონ.

**Input:** სამი მთელი რიცხვი n, m, a (1 ≤ n, m, a ≤ 10⁹)  
**Output:** ფილების მინიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "6 6 4",  "output": "4",   "explanation": "⌈6/4⌉×⌈6/4⌉ = 2×2 = 4"},
        {"input": "1 1 1",  "output": "1",   "explanation": "1×1 ფილა საკმარისია"},
        {"input": "3 3 2",  "output": "4",   "hidden": True},
        {"input": "1000000000 1000000000 1", "output": "1000000000000000000", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="გუნდის ამოცანა",
    difficulty="easy", xp=20, category="Logic",
    description="""## გუნდის ამოცანა

სამი მეგობარი — პეტრე, ვასო და ტატო — მონაწილეობს ოლიმპიადაში.  
გუნდი წერს ამოცანას მხოლოდ მაშინ, თუ **მინიმუმ ორმა** მათგანმა იცის ამოხსნა.

მოცემულია n ამოცანა. დათვალეთ, რამდენ ამოცანას დაწერს გუნდი.

**Input:** n, შემდეგ n ხაზზე 3 რიცხვი (0 ან 1)  
**Output:** დაწერილი ამოცანების რაოდენობა""",
    test_cases=json.dumps([
        {"input": "3\n1 1 0\n1 1 1\n0 0 1", "output": "2"},
        {"input": "1\n0 0 0", "output": "0"},
        {"input": "4\n1 0 1\n0 1 1\n1 1 1\n0 0 0", "output": "3", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="გრძელი სიტყვების შემოკლება",
    difficulty="easy", xp=20, category="Strings",
    description="""## გრძელი სიტყვების შემოკლება

თუ სიტყვა შეიცავს **10-ზე მეტ** ასოს, ის ითვლება "გრძელად".  
შემოკლების წესი: **პირველი ასო** + **შუა ასოების რაოდენობა** + **ბოლო ასო**.

მაგალითად: `localization` → `l10n`

**Input:** n — სიტყვების რაოდენობა, შემდეგ n სიტყვა  
**Output:** თითოეული სიტყვა (შემოკლებული ან უცვლელი)""",
    test_cases=json.dumps([
        {"input": "4\nlocalization\ninternationally\nword\napple", "output": "l10n\ni13y\nword\napple"},
        {"input": "1\nabcdefghijk", "output": "a9k"},
        {"input": "2\nhello\nrepresentation", "output": "hello\nr12n", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="ბიტლენდის ენა",
    difficulty="easy", xp=20, category="Implementation",
    description="""## ბიტლენდის ენა

ბიტლენდში არის მხოლოდ ერთი ცვლადი **x** (საწყისი მნიშვნელობა 0).  
4 ოპერაცია: `++X`, `X++` — x-ს 1-ით გაზრდა; `--X`, `X--` — 1-ით შემცირება.

**Input:** n ოპერაცია  
**Output:** x-ის საბოლოო მნიშვნელობა""",
    test_cases=json.dumps([
        {"input": "4\n++X\n++X\n--X\nX++", "output": "2"},
        {"input": "2\n--X\n--X", "output": "-2"},
        {"input": "3\nX++\nX--\n++X", "output": "1", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="დომინოების განლაგება",
    difficulty="easy", xp=25, category="Math",
    description="""## დომინოების განლაგება

გაქვთ **M × N** ზომის დაფა და **2×1** ზომის დომინოს ქვები.  
მაქსიმუმ რამდენი დომინო ეტევა დაფაზე ისე, რომ არ გადაფარონ ერთმანეთს?

**Input:** M და N (1 ≤ M, N ≤ 16)  
**Output:** დომინოების მაქსიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "2 4", "output": "4", "explanation": "(2×4)/2 = 4"},
        {"input": "3 3", "output": "4", "explanation": "9/2 = 4 (floor)"},
        {"input": "1 1", "output": "0", "hidden": True},
        {"input": "16 16", "output": "128", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="ლამაზი მატრიცა",
    difficulty="easy", xp=30, category="Arrays",
    description="""## ლამაზი მატრიცა

მოცემულია **5×5** მატრიცა — 24 ნული და ერთი ერთიანი.  
ერთ სვლაში შეგიძლიათ გაცვალოთ ორი მეზობელი სტრიქონი ან სვეტი.  
იპოვეთ სვლების **მინიმალური** რაოდენობა, რომ 1 აღმოჩნდეს ცენტრში (3,3).

**Input:** 5×5 მატრიცა  
**Output:** სვლების მინიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "0 0 0 0 0\n0 0 0 0 0\n0 0 1 0 0\n0 0 0 0 0\n0 0 0 0 0", "output": "0"},
        {"input": "1 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0", "output": "4"},
        {"input": "0 0 0 0 1\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0", "output": "4", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="კაპიტალური ასო",
    difficulty="easy", xp=15, category="Strings",
    description="""## კაპიტალური ასო

მოცემულია სიტყვა. თუ მისი **პირველი ასო** არ არის დიდი, გახადეთ ის დიდი.  
დანარჩენი ასოები **უცვლელად** დარჩება.

**Input:** ერთი სიტყვა (ლათინური ასოებით)  
**Output:** იგივე სიტყვა დიდი პირველი ასოთი""",
    test_cases=json.dumps([
        {"input": "hello", "output": "Hello"},
        {"input": "World", "output": "World"},
        {"input": "pYthon", "output": "PYthon", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="ჯარისკაცი და ბანანები",
    difficulty="easy", xp=25, category="Math",
    description="""## ჯარისკაცი და ბანანები

ჯარისკაცს უნდა **k** ბანანის ყიდვა.  
პირველი ბანანი ღირს **w** დოლარი, მეორე 2w, მესამე 3w...  
მას აქვს **n** დოლარი. რამდენი დოლარის სესხება დასჭირდება?

**Input:** w, n, k  
**Output:** სესხის ოდენობა (0 თუ ყოფნის)""",
    test_cases=json.dumps([
        {"input": "2 3 5", "output": "27", "explanation": "სჭირდება 2+4+6+8+10=30, აქვს 3, სჭირდება 27"},
        {"input": "1 10 5", "output": "5",  "explanation": "1+2+3+4+5=15, 15-10=5"},
        {"input": "1 100 5","output": "0",  "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="სპილოს ნაბიჯები",
    difficulty="easy", xp=15, category="Greedy",
    description="""## სპილოს ნაბიჯები

სპილო იმყოფება **0** წერტილში და უნდა მივიდეს **x** წერტილში.  
ერთ ნაბიჯში შეუძლია გადაადგილდეს **1, 2, 3, 4 ან 5** ერთეულით.  
რა არის ნაბიჯების **მინიმალური** რაოდენობა?

**Input:** x  
**Output:** მინიმალური ნაბიჯების რაოდენობა""",
    test_cases=json.dumps([
        {"input": "0",  "output": "0"},
        {"input": "5",  "output": "1"},
        {"input": "13", "output": "3", "explanation": "5+5+3"},
        {"input": "1000000000", "output": "200000000", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),
dict(
    title="ქვები მაგიდაზე",
    difficulty="easy", xp=30, category="Strings",
    description="""## ქვები მაგიდაზე

მაგიდაზე მწკრივად დევს **n** ფერადი ქვა (R-წითელი, G-მწვანე, B-ლურჯი).  
მინიმუმ რამდენი ქვა უნდა ავიღოთ, რომ **არცერთი ორი მეზობელი** ქვა არ იყოს ერთი ფერის?

**Input:** n, შემდეგ ქვების ფერები  
**Output:** ასაღები ქვების მინიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "3\nR G G", "output": "1"},
        {"input": "5\nR R R R R", "output": "2"},
        {"input": "4\nR G B R", "output": "0", "hidden": True},
        {"input": "6\nR R G G B B", "output": "2", "hidden": True},
    ]),
    time_limit=1.0, memory_limit=256
),

# ══════════════════════════════════════════
#  MEDIUM  (10)
# ══════════════════════════════════════════
dict(
    title="დრაკონები",
    difficulty="medium", xp=70, category="Greedy",
    description="""## დრაკონები

კირილე თამაშობს RPG თამაშს. მას აქვს ძალა **s** და უნდა დაამარცხოს **n** დრაკონი.  
თითოეულ დრაკონს აქვს ძალა **xᵢ** და ბონუსი **yᵢ**.  
კირილე ამარცხებს დრაკონს მხოლოდ მაშინ, თუ **s > xᵢ** (მკაცრად მეტი).  
გამარჯვებისას **s += yᵢ**.

**Input:** s, n, შემდეგ n ხაზი xᵢ yᵢ-ით  
**Output:** YES ან NO""",
    test_cases=json.dumps([
        {"input": "2 3\n1 3\n4 5\n3 2", "output": "YES"},
        {"input": "1 2\n5 5\n6 6",     "output": "NO"},
        {"input": "10 4\n9 1\n10 1\n11 1\n12 1", "output": "YES", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="საინტერესო სასმელი",
    difficulty="medium", xp=75, category="Binary Search",
    description="""## საინტერესო სასმელი

ქალაქში n მაღაზია სხვადასხვა ფასით ყიდის კოკა-კოლას.  
ყოველი დღე ვასოს აქვს გარკვეული ბიუჯეტი **mⱼ**.  
დათვალეთ, **რამდენი მაღაზიიდან** შეუძლია ყიდვა ყოველ დღე.

**Input:** n, ფასების მასივი, q, q ბიუჯეტი  
**Output:** q რიცხვი — თითოეული დღისთვის""",
    test_cases=json.dumps([
        {"input": "4\n4 2 3 1\n3\n3 5 1", "output": "3\n4\n1"},
        {"input": "2\n10 20\n2\n5 15",    "output": "0\n1"},
        {"input": "3\n1 2 3\n3\n1 2 3",   "output": "1\n2\n3", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="რეგისტრაციის სისტემა",
    difficulty="medium", xp=65, category="Hashing",
    description="""## რეგისტრაციის სისტემა

სისტემა ამოწმებს username-ების ხელმისაწვდომობას.  
- თუ სახელი თავისუფალია → **OK**  
- თუ დაკავებულია → **name + ბოლო ციფრი** (first1, first2...)

**Input:** n მოთხოვნა, შემდეგ n სახელი  
**Output:** OK ან ახალი სახელი""",
    test_cases=json.dumps([
        {"input": "4\neka\neka\neka\nbekaa", "output": "OK\neka1\neka2\nOK"},
        {"input": "2\ntest\ntest",           "output": "OK\ntest1"},
        {"input": "3\na\na\na",              "output": "OK\na1\na2", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="ტაქსი",
    difficulty="medium", xp=65, category="Greedy",
    description="""## ტაქსი

**n** ჯგუფი ბავშვებისა, ყველა ჯგუფი **ერთად** უნდა ჩასხდეს.  
ტაქსში ეტევა **მაქსიმუმ 4** ადამიანი. ჯგუფები შეიძლება გაერთიანდნენ.  
რა არის ტაქსების **მინიმალური** რაოდენობა?

**Input:** n, შემდეგ ჯგუფების ზომები (1–4)  
**Output:** მინიმალური ტაქსების რაოდენობა""",
    test_cases=json.dumps([
        {"input": "5\n1 2 4 3 3", "output": "4"},
        {"input": "4\n1 1 1 1",   "output": "1"},
        {"input": "3\n4 4 4",     "output": "3", "hidden": True},
        {"input": "6\n3 3 3 1 1 1", "output": "4", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="ბერლიანდი და მონეტები",
    difficulty="medium", xp=80, category="Math",
    description="""## ბერლიანდი და მონეტები

გაქვთ **n** ღირებულების ჩეკი. გაქვთ მონეტები: **1, 2, 3, ..., k**.  
მინიმუმ რამდენი მონეტა სჭირდება ზუსტად **n** თანხისთვის?

**Input:** n, k (1 ≤ n, k ≤ 10⁹)  
**Output:** მონეტების მინიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "6 4",  "output": "2", "explanation": "4+2=6, 2 მონეტა"},
        {"input": "7 4",  "output": "2", "explanation": "4+3=7"},
        {"input": "100 1","output": "100", "hidden": True},
        {"input": "1000000000 1000000000", "output": "1", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="ორი გროვა კანფეტი",
    difficulty="medium", xp=85, category="Game Theory",
    description="""## ორი გროვა კანფეტი

მაგიდაზე ორი გროვა: **a** და **b** კანფეტი.  
სვლა: ერთი გროვიდან 1 კანფეტი, მეორიდან 2 (ან პირიქით).  
ვინც ვეღარ ასრულებს სვლას — **წაგებულია**.  
ორივე ოპტიმალურად თამაშობს. **ვინ მოიგებს?**

**Input:** a, b  
**Output:** First ან Second""",
    test_cases=json.dumps([
        {"input": "1 1", "output": "Second"},
        {"input": "1 2", "output": "First"},
        {"input": "5 4", "output": "First", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="T-Prime რიცხვები",
    difficulty="medium", xp=90, category="Number Theory",
    description="""## T-Prime რიცხვები

რიცხვს ეწოდება **T-Prime**, თუ მას აქვს ზუსტად **3** გამყოფი.  
(მაგ: 4 → გამყოფები: 1, 2, 4 — T-Prime ✓)

**Input:** n, შემდეგ n რიცხვი (xᵢ ≤ 10¹²)  
**Output:** YES ან NO თითოეულისთვის""",
    test_cases=json.dumps([
        {"input": "3\n4 5 9",    "output": "YES\nNO\nYES"},
        {"input": "2\n1 25",     "output": "NO\nYES"},
        {"input": "3\n49 50 121","output": "YES\nNO\nYES", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=256
),
dict(
    title="ლექსიკოგრაფიული მინიმუმი",
    difficulty="medium", xp=75, category="Strings",
    description="""## ლექსიკოგრაფიული მინიმუმი

n სტრიქონი. დალაგეთ ისე, რომ მათი გაერთიანება (concatenation) იყოს  
**ლექსიკოგრაფიულად ყველაზე პატარა**.

**Input:** n, შემდეგ n სტრიქონი  
**Output:** ერთიანი სტრიქონი""",
    test_cases=json.dumps([
        {"input": "3\nb\nba\nbab",   "output": "babbab"},
        {"input": "2\naa\naaa",      "output": "aaaaa"},
        {"input": "3\nc\ncb\ncba",   "output": "cbacbc", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="კვადრატები და კუბები",
    difficulty="medium", xp=80, category="Math",
    description="""## კვადრატები და კუბები

მოცემულია **n**. დათვალეთ 1-დან n-მდე (ჩათვლით) რამდენი რიცხვია,  
რომელიც არის **სრული კვადრატი** ან **სრული კუბი** (ან ორივე).

**Input:** n (1 ≤ n ≤ 10⁹)  
**Output:** ასეთი რიცხვების რაოდენობა""",
    test_cases=json.dumps([
        {"input": "10",  "output": "4",  "explanation": "1,4,8,9"},
        {"input": "1",   "output": "1"},
        {"input": "100", "output": "14", "hidden": True},
        {"input": "1000000000", "output": "32290", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),
dict(
    title="ყველაზე გრძელი ქვესტრიქონი",
    difficulty="medium", xp=85, category="Two Pointers",
    description="""## ყველაზე გრძელი ქვესტრიქონი

მოცემულია სტრიქონი **S**. იპოვეთ ყველაზე გრძელი ქვესტრიქონის სიგრძე,  
**რომელშიც არცერთი სიმბოლო არ მეორდება**.

**Input:** სტრიქონი S  
**Output:** მაქსიმალური სიგრძე""",
    test_cases=json.dumps([
        {"input": "abcabcbb", "output": "3"},
        {"input": "bbbbb",    "output": "1"},
        {"input": "pwwkew",   "output": "3"},
        {"input": "abcdefgh", "output": "8", "hidden": True},
    ]),
    time_limit=2.0, memory_limit=256
),

# ══════════════════════════════════════════
#  HARD  (10)
# ══════════════════════════════════════════
dict(
    title="ყველაზე გრძელი საერთო ქვემიმდევრობა",
    difficulty="hard", xp=150, category="DP",
    description="""## ყველაზე გრძელი საერთო ქვემიმდევრობა (LCS)

მოცემულია ორი სტრიქონი **A** და **B**.  
იპოვეთ მათი **ყველაზე გრძელი საერთო ქვემიმდევრობის** (LCS) სიგრძე.

ქვემიმდევრობა — სიმბოლოები, რომლებიც ორივე სტრიქონში ერთი თანმიმდევრობით გვხვდება, მაგრამ არ არის აუცილებელი მეზობლები იყვნენ.

**Input:** ორი სტრიქონი (სიგრძე ≤ 5000)  
**Output:** LCS-ის სიგრძე""",
    test_cases=json.dumps([
        {"input": "abcde\nace",   "output": "3", "explanation": "ace"},
        {"input": "abc\nabc",     "output": "3"},
        {"input": "abc\ndef",     "output": "0"},
        {"input": "abcbdab\nbdcaba", "output": "4", "hidden": True},
    ]),
    time_limit=5.0, memory_limit=512
),
dict(
    title="უმოკლესი გზა გრაფში",
    difficulty="hard", xp=160, category="Graph",
    description="""## უმოკლესი გზა გრაფში (Dijkstra)

მოცემულია **n** ქალაქი და **m** ორმხრივი გზა.  
თითოეულ გზას აქვს წონა. იპოვეთ უმოკლესი გზა **1-ლი → n-ური** ქალაქი.  
თუ გზა არ არსებობს, გამოიტანეთ **-1**.

**Input:** n, m; შემდეგ m ხაზი: u v w  
**Output:** მინიმალური მანძილი""",
    test_cases=json.dumps([
        {"input": "4 4\n1 2 1\n2 3 2\n3 4 3\n1 4 10", "output": "6"},
        {"input": "2 0", "output": "-1"},
        {"input": "3 3\n1 2 5\n2 3 3\n1 3 9", "output": "8", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=512
),
dict(
    title="ზურგჩანთის ამოცანა",
    difficulty="hard", xp=155, category="DP",
    description="""## ზურგჩანთის ამოცანა (0/1 Knapsack)

ზურგჩანთის ტევადობა **W**. გაქვთ **n** ნივთი (წონა wᵢ, ღირებულება vᵢ).  
შეარჩიეთ ნივთები ისე, რომ **წონა ≤ W** და **ღირებულება მაქსიმალური**.

**Input:** n, W; შემდეგ n ხაზი: wᵢ vᵢ  
**Output:** მაქსიმალური ღირებულება""",
    test_cases=json.dumps([
        {"input": "3 4\n1 1\n3 4\n4 5", "output": "5"},
        {"input": "4 5\n1 2\n2 3\n3 4\n4 5", "output": "7"},
        {"input": "1 0\n1 100", "output": "0", "hidden": True},
        {"input": "3 10\n5 10\n4 40\n3 30", "output": "70", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=512
),
dict(
    title="Range Sum Query",
    difficulty="hard", xp=165, category="Data Structures",
    description="""## Range Sum Query (Segment Tree / Fenwick Tree)

მოცემულია **n** რიცხვისგან შემდგარი მასივი. q ოპერაცია:
- `1 i x` — i-ური ელემენტი გახდეს x
- `2 l r` — [l, r] დიაპაზონის ელემენტების ჯამი

**Input:** n, მასივი, q, q ოპერაცია  
**Output:** "2" ტიპის ოპერაციების პასუხები""",
    test_cases=json.dumps([
        {"input": "5\n1 2 3 4 5\n3\n2 1 3\n1 2 10\n2 1 5", "output": "6\n22"},
        {"input": "3\n1 1 1\n2\n2 1 3\n2 2 2", "output": "3\n1"},
        {"input": "4\n4 3 2 1\n2\n1 1 10\n2 1 4", "output": "16", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=512
),
dict(
    title="მაქსიმალური ნაკადი",
    difficulty="hard", xp=180, category="Graph",
    description="""## მაქსიმალური ნაკადი (Max Flow)

მოცემულია მიმართული გრაფი — წყალსადენი სისტემა.  
თითოეულ წიბოს აქვს გამტარუნარიანობა **cᵢⱼ**.  
იპოვეთ მაქსიმალური ნაკადი **Source (1) → Sink (n)**.

**Input:** n (ქალაქები), m (მილები); შემდეგ m ხაზი: u v c  
**Output:** მაქსიმალური ნაკადი""",
    test_cases=json.dumps([
        {"input": "4 5\n1 2 3\n1 3 2\n2 4 2\n3 4 2\n2 3 1", "output": "4"},
        {"input": "2 1\n1 2 5", "output": "5"},
        {"input": "3 3\n1 2 10\n2 3 5\n1 3 7", "output": "12", "hidden": True},
    ]),
    time_limit=5.0, memory_limit=512
),
dict(
    title="მინიმალური დამფარავი ხე",
    difficulty="hard", xp=170, category="Graph",
    description="""## მინიმალური დამფარავი ხე (MST)

**n** კუნძული, ყველა კუნძული ერთმანეთთან დასაკავშირებელია ხიდებით.  
მოცემულია ყველა შესაძლო ხიდის ღირებულება.  
იპოვეთ **მინიმალური ჯამური ხარჯი** ყველა კუნძულის დასაკავშირებლად.

**Input:** n, m; შემდეგ m ხაზი: u v w  
**Output:** MST-ის ჯამური ღირებულება""",
    test_cases=json.dumps([
        {"input": "4 6\n1 2 1\n1 3 3\n1 4 4\n2 3 2\n2 4 3\n3 4 1", "output": "4"},
        {"input": "2 1\n1 2 5", "output": "5"},
        {"input": "3 3\n1 2 1\n2 3 2\n1 3 4", "output": "3", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=512
),
dict(
    title="პალინდრომული დანაწილება",
    difficulty="hard", xp=160, category="DP",
    description="""## პალინდრომული დანაწილება

მოცემულია სტრიქონი **S**.  
იპოვეთ **მინიმალური ჭრების** რაოდენობა, რომ ყველა ნაწილი იყოს პალინდრომი.

**Input:** სტრიქონი S (სიგრძე ≤ 2000)  
**Output:** მინიმალური ჭრების რაოდენობა""",
    test_cases=json.dumps([
        {"input": "aab",      "output": "1", "explanation": "aa|b"},
        {"input": "a",        "output": "0"},
        {"input": "ab",       "output": "1"},
        {"input": "ababbbabbababa", "output": "3", "hidden": True},
    ]),
    time_limit=5.0, memory_limit=512
),
dict(
    title="მოგზაური გამყიდველი (TSP)",
    difficulty="hard", xp=200, category="DP",
    description="""## მოგზაური გამყიდველი (TSP — Bitmask DP)

გამყიდველმა უნდა მოინახულოს **n** ქალაქი (ყველა ზუსტად ერთხელ)  
და დაბრუნდეს საწყის წერტილში (ქალაქი 0).  
იპოვეთ **მარშრუტის მინიმალური სიგრძე**.

**Input:** n (≤ 20), შემდეგ n×n მატრიცა (d[i][j] — მანძილი)  
**Output:** მინიმალური მანძილი""",
    test_cases=json.dumps([
        {"input": "4\n0 10 15 20\n10 0 35 25\n15 35 0 30\n20 25 30 0", "output": "80"},
        {"input": "2\n0 5\n5 0", "output": "10"},
        {"input": "3\n0 1 2\n1 0 3\n2 3 0", "output": "6", "hidden": True},
    ]),
    time_limit=10.0, memory_limit=512
),
dict(
    title="მაქსიმალური XOR ქვემასი",
    difficulty="hard", xp=175, category="Bit Manipulation",
    description="""## მაქსიმალური XOR ქვემასი

მოცემულია **n** რიცხვისგან შემდგარი მასივი.  
იპოვეთ უწყვეტი ქვემასი, რომლის ელემენტების **XOR ჯამი მაქსიმალურია**.

**Input:** n, შემდეგ n რიცხვი  
**Output:** მაქსიმალური XOR""",
    test_cases=json.dumps([
        {"input": "4\n1 2 3 4",    "output": "7"},
        {"input": "3\n8 1 2",       "output": "11"},
        {"input": "5\n3 8 2 6 5",  "output": "15", "hidden": True},
    ]),
    time_limit=3.0, memory_limit=512
),
dict(
    title="მატრიცების გამრავლების ჯაჭვი",
    difficulty="hard", xp=185, category="DP",
    description="""## მატრიცების გამრავლების ჯაჭვი

გაქვთ **n** მატრიცა. M₁ ზომა p₀×p₁, M₂ ზომა p₁×p₂, ...  
იპოვეთ ფრჩხილების ისეთი დასმა, რომ **სკალარული გამრავლებების**  
საერთო რაოდენობა **მინიმალური** იყოს.

**Input:** n+1 რიცხვი (pᵢ — განზომილებები)  
**Output:** ოპერაციების მინიმალური რაოდენობა""",
    test_cases=json.dumps([
        {"input": "4\n10 30 5 60",  "output": "4500"},
        {"input": "3\n2 3 4",       "output": "24"},
        {"input": "2\n10 20",       "output": "0"},
        {"input": "5\n5 10 3 12 5", "output": "405", "hidden": True},
    ]),
    time_limit=5.0, memory_limit=512
),
]


def seed():
    from app import create_app
    from extensions import db
    from models import Task

    app = create_app()
    with app.app_context():
        if Task.query.count() > 0:
            print("Tasks already exist. Delete DB first if you want to re-seed.")
            return

        for t in TASKS:
            task = Task(
                title        = t["title"],
                difficulty   = t["difficulty"],
                xp           = t["xp"],
                category     = t["category"],
                description  = t["description"],
                test_cases   = t["test_cases"],
                time_limit   = t.get("time_limit", 2.0),
                memory_limit = t.get("memory_limit", 256),
            )
            db.session.add(task)
        db.session.commit()
        print(f"✅ {len(TASKS)} tasks seeded successfully.")


if __name__ == "__main__":
    seed()