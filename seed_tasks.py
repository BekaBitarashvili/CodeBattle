import json

TASKS = [
# ══════════ EASY ══════════
dict(
    title_ka="თეატრალური მოედანი", title_en="Town Square Tiles",
    difficulty="easy", xp=25, category_ka="მათემატიკა", category_en="Math",
    description_ka="""## თეატრალური მოედანი

ქალაქის მოედანი არის მართკუთხედის ფორმის, ზომებით **n × m** მეტრი.
მერიამ გადაწყვიტა მოაპირკეთოს კვადრატული ფილებით, გვერდის სიგრძით **a**.

მინიმუმ რამდენი ფილაა საჭირო სრულად დასაფარად?
ფილების გატეხვა **აკრძალულია**, ფილებმა შეიძლება საზღვრებს გარეთ გაიწიონ.

**შეყვანა:** სამი მთელი რიცხვი n, m, a (1 ≤ n, m, a ≤ 10⁹)
**გამოტანა:** ფილების მინიმალური რაოდენობა""",
    description_en="""## Town Square Tiles

The city square is a rectangle of size **n × m** meters.
Maria wants to tile it with square tiles of side length **a**.

What is the minimum number of tiles needed to fully cover the square?
Tiles cannot be cut, but may extend beyond the boundary.

**Input:** Three integers n, m, a (1 ≤ n, m, a ≤ 10⁹)
**Output:** Minimum number of tiles""",
    test_cases=json.dumps([
        {"input":"6 6 4","output":"4","explanation_ka":"⌈6/4⌉×⌈6/4⌉=2×2=4","explanation_en":"⌈6/4⌉×⌈6/4⌉=2×2=4"},
        {"input":"1 1 1","output":"1","explanation_ka":"1 ფილა საკმარისია","explanation_en":"1 tile is enough"},
        {"input":"3 3 2","output":"4","hidden":True},
        {"input":"1000000000 1000000000 1","output":"1000000000000000000","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="გუნდის ამოცანა", title_en="Team Problem",
    difficulty="easy", xp=20, category_ka="ლოგიკა", category_en="Logic",
    description_ka="""## გუნდის ამოცანა

სამი მეგობარი — პეტრე, ვასო და ტატო — მონაწილეობს ოლიმპიადაში.
გუნდი წერს ამოცანას მხოლოდ მაშინ, თუ **მინიმუმ ორმა** მათგანმა იცის ამოხსნა.

**შეყვანა:** n, შემდეგ n ხაზი 3 რიცხვით (0 ან 1)
**გამოტანა:** დაწერილი ამოცანების რაოდენობა""",
    description_en="""## Team Problem

Three friends — Petre, Vaso, and Tato — compete in an olympiad.
The team submits a problem only if **at least two** of them know the solution.

**Input:** n, then n lines with 3 numbers (0 or 1)
**Output:** Number of problems the team will solve""",
    test_cases=json.dumps([
        {"input":"3\n1 1 0\n1 1 1\n0 0 1","output":"2"},
        {"input":"1\n0 0 0","output":"0"},
        {"input":"4\n1 0 1\n0 1 1\n1 1 1\n0 0 0","output":"3","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="გრძელი სიტყვების შემოკლება", title_en="Long Word Abbreviation",
    difficulty="easy", xp=20, category_ka="სტრიქონები", category_en="Strings",
    description_ka="""## გრძელი სიტყვების შემოკლება

10-ზე მეტი ასოს შემცველი სიტყვა "გრძელია".
შემოკლება: **პირველი ასო** + **შუა ასოების რაოდენობა** + **ბოლო ასო**.

მაგალითი: `localization` → `l10n`

**შეყვანა:** n სიტყვა
**გამოტანა:** თითოეული სიტყვა (შემოკლებული ან უცვლელი)""",
    description_en="""## Long Word Abbreviation

A word is "long" if it contains more than 10 letters.
Abbreviate as: **first letter** + **count of middle letters** + **last letter**.

Example: `localization` → `l10n`

**Input:** n words
**Output:** Each word (abbreviated or unchanged)""",
    test_cases=json.dumps([
        {"input":"4\nlocalization\ninternationally\nword\napple","output":"l10n\ni13y\nword\napple"},
        {"input":"1\nabcdefghijk","output":"a9k"},
        {"input":"2\nhello\nrepresentation","output":"hello\nr12n","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="ბიტლენდის ენა", title_en="Bitland Language",
    difficulty="easy", xp=20, category_ka="იმპლემენტაცია", category_en="Implementation",
    description_ka="""## ბიტლენდის ენა

ბიტლენდში ერთი ცვლადი **x** (საწყისი: 0).
4 ოპერაცია: `++X`, `X++` — +1; `--X`, `X--` — -1.

**შეყვანა:** n ოპერაცია
**გამოტანა:** x-ის საბოლოო მნიშვნელობა""",
    description_en="""## Bitland Language

In Bitland there is one variable **x** (initial: 0).
4 operations: `++X`, `X++` — increment by 1; `--X`, `X--` — decrement by 1.

**Input:** n operations
**Output:** Final value of x""",
    test_cases=json.dumps([
        {"input":"4\n++X\n++X\n--X\nX++","output":"2"},
        {"input":"2\n--X\n--X","output":"-2"},
        {"input":"3\nX++\nX--\n++X","output":"1","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="დომინოების განლაგება", title_en="Domino Placement",
    difficulty="easy", xp=25, category_ka="მათემატიკა", category_en="Math",
    description_ka="""## დომინოების განლაგება

**M × N** ზომის დაფა და **2×1** ზომის დომინოები.
მაქსიმუმ რამდენი დომინო ეტევა ისე, რომ არ გადაფარონ ერთმანეთს?

**შეყვანა:** M, N (1 ≤ M, N ≤ 16)
**გამოტანა:** მაქსიმალური რაოდენობა""",
    description_en="""## Domino Placement

A board of size **M × N** and dominoes of size **2×1**.
What is the maximum number of dominoes that can be placed without overlap?

**Input:** M, N (1 ≤ M, N ≤ 16)
**Output:** Maximum number of dominoes""",
    test_cases=json.dumps([
        {"input":"2 4","output":"4","explanation_en":"(2×4)/2=4"},
        {"input":"3 3","output":"4","explanation_en":"floor(9/2)=4"},
        {"input":"1 1","output":"0","hidden":True},
        {"input":"16 16","output":"128","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="ლამაზი მატრიცა", title_en="Beautiful Matrix",
    difficulty="easy", xp=30, category_ka="მასივები", category_en="Arrays",
    description_ka="""## ლამაზი მატრიცა

**5×5** მატრიცა — 24 ნული და ერთი ერთიანი.
ერთ სვლაში შეგიძლია გაცვალო ორი მეზობელი სტრიქონი ან სვეტი.
იპოვე მინიმალური სვლების რაოდენობა, რომ 1 იყოს ცენტრში (3,3).

**შეყვანა:** 5×5 მატრიცა
**გამოტანა:** სვლების მინიმალური რაოდენობა""",
    description_en="""## Beautiful Matrix

A **5×5** matrix with 24 zeros and one 1.
In one move you can swap two adjacent rows or two adjacent columns.
Find the minimum moves to place the 1 at the center (row 3, col 3).

**Input:** 5×5 matrix
**Output:** Minimum number of moves""",
    test_cases=json.dumps([
        {"input":"0 0 0 0 0\n0 0 0 0 0\n0 0 1 0 0\n0 0 0 0 0\n0 0 0 0 0","output":"0"},
        {"input":"1 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0","output":"4"},
        {"input":"0 0 0 0 1\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0\n0 0 0 0 0","output":"4","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="კაპიტალური ასო", title_en="Capital Letter",
    difficulty="easy", xp=15, category_ka="სტრიქონები", category_en="Strings",
    description_ka="""## კაპიტალური ასო

მოცემულია სიტყვა. თუ **პირველი ასო** არ არის დიდი, გახადე დიდი.
დანარჩენი ასოები **უცვლელად** რჩება.

**შეყვანა:** ერთი სიტყვა
**გამოტანა:** სიტყვა დიდი პირველი ასოთი""",
    description_en="""## Capital Letter

Given a word. If the **first letter** is not uppercase, make it uppercase.
Leave all other letters unchanged.

**Input:** One word
**Output:** Word with uppercase first letter""",
    test_cases=json.dumps([
        {"input":"hello","output":"Hello"},
        {"input":"World","output":"World"},
        {"input":"pYthon","output":"PYthon","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="ჯარისკაცი და ბანანები", title_en="Soldier and Bananas",
    difficulty="easy", xp=25, category_ka="მათემატიკა", category_en="Math",
    description_ka="""## ჯარისკაცი და ბანანები

ჯარისკაცს უნდა **k** ბანანი. პირველი ღირს **w**, მეორე **2w**, მესამე **3w**...
მას აქვს **n** დოლარი. რამდენის სესხება სჭირდება?

**შეყვანა:** w, n, k
**გამოტანა:** სესხის ოდენობა (0 თუ ყოფნის)""",
    description_en="""## Soldier and Bananas

A soldier needs **k** bananas. First costs **w**, second **2w**, third **3w**...
He has **n** dollars. How much does he need to borrow?

**Input:** w, n, k
**Output:** Amount to borrow (0 if enough)""",
    test_cases=json.dumps([
        {"input":"2 3 5","output":"27","explanation_en":"Total=30, has 3, borrow 27"},
        {"input":"1 10 5","output":"5","explanation_en":"Total=15, has 10, borrow 5"},
        {"input":"1 100 5","output":"0","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="სპილოს ნაბიჯები", title_en="Elephant Steps",
    difficulty="easy", xp=15, category_ka="გამხარბი", category_en="Greedy",
    description_ka="""## სპილოს ნაბიჯები

სპილო **0** წერტილშია, უნდა მივიდეს **x**-მდე.
ერთ ნაბიჯში შეიძლება გადაადგილდეს **1, 2, 3, 4 ან 5** ერთეულით.
რა არის მინიმალური ნაბიჯების რაოდენობა?

**შეყვანა:** x
**გამოტანა:** მინიმალური ნაბიჯები""",
    description_en="""## Elephant Steps

An elephant is at position **0** and needs to reach **x**.
In one step it can move **1, 2, 3, 4, or 5** units forward.
What is the minimum number of steps?

**Input:** x
**Output:** Minimum number of steps""",
    test_cases=json.dumps([
        {"input":"0","output":"0"},
        {"input":"5","output":"1"},
        {"input":"13","output":"3","explanation_en":"5+5+3"},
        {"input":"1000000000","output":"200000000","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
dict(
    title_ka="ქვები მაგიდაზე", title_en="Stones on Table",
    difficulty="easy", xp=30, category_ka="სტრიქონები", category_en="Strings",
    description_ka="""## ქვები მაგიდაზე

მაგიდაზე **n** ფერადი ქვა (R-წითელი, G-მწვანე, B-ლურჯი).
მინიმუმ რამდენი ქვა უნდა ავიღოთ, რომ **არცერთი ორი მეზობელი** ქვა არ იყოს ერთი ფერის?

**შეყვანა:** n, შემდეგ ფერები
**გამოტანა:** ასაღები ქვების მინიმალური რაოდენობა""",
    description_en="""## Stones on Table

**n** colored stones on a table (R-red, G-green, B-blue).
What is the minimum number of stones to remove so no two adjacent stones share a color?

**Input:** n, then colors
**Output:** Minimum stones to remove""",
    test_cases=json.dumps([
        {"input":"3\nR G G","output":"1"},
        {"input":"5\nR R R R R","output":"2"},
        {"input":"4\nR G B R","output":"0","hidden":True},
        {"input":"6\nR R G G B B","output":"2","hidden":True},
    ]), time_limit=1.0, memory_limit=256
),
# ══════════ MEDIUM ══════════
dict(
    title_ka="დრაკონები", title_en="Dragons",
    difficulty="medium", xp=70, category_ka="გამხარბი", category_en="Greedy",
    description_ka="""## დრაკონები

კირილეს აქვს ძალა **s** და უნდა დაამარცხოს **n** დრაკონი.
დრაკონი ამარცხდება თუ **s > xᵢ**. გამარჯვებისას **s += yᵢ**.

შეუძლია თუ არა ყველა დრაკონის დამარცხება?

**შეყვანა:** s, n; შემდეგ n ხაზი xᵢ yᵢ
**გამოტანა:** YES ან NO""",
    description_en="""## Dragons

Kiril has strength **s** and must defeat **n** dragons.
He defeats dragon i if **s > xᵢ**, then gains **s += yᵢ**.

Can he defeat all dragons?

**Input:** s, n; then n lines with xᵢ yᵢ
**Output:** YES or NO""",
    test_cases=json.dumps([
        {"input":"2 3\n1 3\n4 5\n3 2","output":"YES"},
        {"input":"1 2\n5 5\n6 6","output":"NO"},
        {"input":"10 4\n9 1\n10 1\n11 1\n12 1","output":"YES","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="საინტერესო სასმელი", title_en="Interesting Drink",
    difficulty="medium", xp=75, category_ka="ორობითი ძებნა", category_en="Binary Search",
    description_ka="""## საინტერესო სასმელი

n მაღაზია სხვადასხვა ფასით. ყოველ დღე ვასოს აქვს ბიუჯეტი **mⱼ**.
დათვალეთ, **რამდენი მაღაზიიდან** შეუძლია ყიდვა ყოველ დღე.

**შეყვანა:** n, ფასები, q, q ბიუჯეტი
**გამოტანა:** q რიცხვი""",
    description_en="""## Interesting Drink

n shops with different prices. Each day Vaso has budget **mⱼ**.
Count how many shops he can buy from each day.

**Input:** n, prices, q, q budgets
**Output:** q numbers""",
    test_cases=json.dumps([
        {"input":"4\n4 2 3 1\n3\n3 5 1","output":"3\n4\n1"},
        {"input":"2\n10 20\n2\n5 15","output":"0\n1"},
        {"input":"3\n1 2 3\n3\n1 2 3","output":"1\n2\n3","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="რეგისტრაციის სისტემა", title_en="Registration System",
    difficulty="medium", xp=65, category_ka="ჰეშირება", category_en="Hashing",
    description_ka="""## რეგისტრაციის სისტემა

სისტემა ამოწმებს username-ებს:
- თავისუფალია → **OK**
- დაკავებულია → **name + ბოლო ციფრი** (eka1, eka2...)

**შეყვანა:** n მოთხოვნა
**გამოტანა:** OK ან ახალი სახელი""",
    description_en="""## Registration System

The system checks usernames:
- Available → **OK**
- Taken → **name + next number** (eka1, eka2...)

**Input:** n requests, then n usernames
**Output:** OK or new generated name""",
    test_cases=json.dumps([
        {"input":"4\neka\neka\neka\nbekaa","output":"OK\neka1\neka2\nOK"},
        {"input":"2\ntest\ntest","output":"OK\ntest1"},
        {"input":"3\na\na\na","output":"OK\na1\na2","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="ტაქსი", title_en="Taxi",
    difficulty="medium", xp=65, category_ka="გამხარბი", category_en="Greedy",
    description_ka="""## ტაქსი

**n** ჯგუფი ბავშვი. ტაქსში ეტევა **მაქსიმუმ 4**.
ჯგუფი **ერთად** უნდა ჩასხდეს. ჯგუფები შეიძლება გაერთიანდნენ.
რა არის ტაქსების **მინიმალური** რაოდენობა?

**შეყვანა:** n, შემდეგ ჯგუფების ზომები
**გამოტანა:** მინიმალური ტაქსი""",
    description_en="""## Taxi

**n** groups of children. A taxi fits **at most 4**.
Each group must ride together. Groups can share a taxi.
What is the minimum number of taxis?

**Input:** n, then group sizes
**Output:** Minimum taxis""",
    test_cases=json.dumps([
        {"input":"5\n1 2 4 3 3","output":"4"},
        {"input":"4\n1 1 1 1","output":"1"},
        {"input":"3\n4 4 4","output":"3","hidden":True},
        {"input":"6\n3 3 3 1 1 1","output":"4","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="ბერლიანდი და მონეტები", title_en="Berland and Coins",
    difficulty="medium", xp=80, category_ka="მათემატიკა", category_en="Math",
    description_ka="""## ბერლიანდი და მონეტები

გაქვთ **n** ღირებულების ჩეკი. გაქვთ მონეტები **1, 2, ..., k**.
მინიმუმ რამდენი მონეტა სჭირდება ზუსტად **n** თანხისთვის?

**შეყვანა:** n, k
**გამოტანა:** მინიმალური მონეტები""",
    description_en="""## Berland and Coins

You have a bill of **n**. You have coins of denominations **1, 2, ..., k**.
What is the minimum number of coins to make exactly **n**?

**Input:** n, k
**Output:** Minimum coins""",
    test_cases=json.dumps([
        {"input":"6 4","output":"2","explanation_en":"4+2=6"},
        {"input":"7 4","output":"2","explanation_en":"4+3=7"},
        {"input":"100 1","output":"100","hidden":True},
        {"input":"1000000000 1000000000","output":"1","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="ორი გროვა კანფეტი", title_en="Two Candy Piles",
    difficulty="medium", xp=85, category_ka="თამაშის თეორია", category_en="Game Theory",
    description_ka="""## ორი გროვა კანფეტი

ორი გროვა: **a** და **b** კანფეტი. სვლა: ერთი გროვიდან 1, მეორიდან 2.
ვინც ვეღარ ასრულებს სვლას — **წაგებულია**. ორივე ოპტიმალურად თამაშობს.

**შეყვანა:** a, b
**გამოტანა:** First ან Second""",
    description_en="""## Two Candy Piles

Two piles: **a** and **b** candies. A move: take 1 from one pile and 2 from the other.
The player who cannot move **loses**. Both play optimally.

**Input:** a, b
**Output:** First or Second""",
    test_cases=json.dumps([
        {"input":"1 1","output":"Second"},
        {"input":"1 2","output":"First"},
        {"input":"5 4","output":"First","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="T-Prime რიცხვები", title_en="T-Prime Numbers",
    difficulty="medium", xp=90, category_ka="რიცხვთა თეორია", category_en="Number Theory",
    description_ka="""## T-Prime რიცხვები

რიცხვს ეწოდება **T-Prime** თუ მას აქვს ზუსტად **3** გამყოფი.
(მაგ: 4 → 1, 2, 4 — T-Prime ✓)

**შეყვანა:** n, შემდეგ n რიცხვი (xᵢ ≤ 10¹²)
**გამოტანა:** YES ან NO""",
    description_en="""## T-Prime Numbers

A number is **T-Prime** if it has exactly **3** divisors.
(e.g.: 4 → 1, 2, 4 — T-Prime ✓)

**Input:** n, then n numbers (xᵢ ≤ 10¹²)
**Output:** YES or NO for each""",
    test_cases=json.dumps([
        {"input":"3\n4 5 9","output":"YES\nNO\nYES"},
        {"input":"2\n1 25","output":"NO\nYES"},
        {"input":"3\n49 50 121","output":"YES\nNO\nYES","hidden":True},
    ]), time_limit=3.0, memory_limit=256
),
dict(
    title_ka="ლექსიკოგრაფიული მინიმუმი", title_en="Lexicographic Minimum",
    difficulty="medium", xp=75, category_ka="სტრიქონები", category_en="Strings",
    description_ka="""## ლექსიკოგრაფიული მინიმუმი

n სტრიქონი. დაალაგე ისე, რომ გაერთიანება იყოს
**ლექსიკოგრაფიულად ყველაზე პატარა**.

**შეყვანა:** n სტრიქონი
**გამოტანა:** ერთიანი სტრიქონი""",
    description_en="""## Lexicographic Minimum

n strings. Sort them so their concatenation is
**lexicographically smallest**.

**Input:** n strings
**Output:** Concatenated result""",
    test_cases=json.dumps([
        {"input":"3\nb\nba\nbab","output":"babbab"},
        {"input":"2\naa\naaa","output":"aaaaa"},
        {"input":"3\nc\ncb\ncba","output":"cbacbc","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="კვადრატები და კუბები", title_en="Squares and Cubes",
    difficulty="medium", xp=80, category_ka="მათემატიკა", category_en="Math",
    description_ka="""## კვადრატები და კუბები

მოცემულია **n**. დათვალე 1-დან n-მდე რამდენი რიცხვია,
რომელიც არის **სრული კვადრატი** ან **სრული კუბი**.

**შეყვანა:** n (1 ≤ n ≤ 10⁹)
**გამოტანა:** ასეთი რიცხვების რაოდენობა""",
    description_en="""## Squares and Cubes

Given **n**. Count numbers from 1 to n (inclusive) that are
a **perfect square** or **perfect cube** (or both).

**Input:** n (1 ≤ n ≤ 10⁹)
**Output:** Count of such numbers""",
    test_cases=json.dumps([
        {"input":"10","output":"4","explanation_en":"1,4,8,9"},
        {"input":"1","output":"1"},
        {"input":"100","output":"14","hidden":True},
        {"input":"1000000000","output":"32290","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
dict(
    title_ka="ყველაზე გრძელი ქვესტრიქონი", title_en="Longest Unique Substring",
    difficulty="medium", xp=85, category_ka="ორი პოინტერი", category_en="Two Pointers",
    description_ka="""## ყველაზე გრძელი ქვესტრიქონი

სტრიქონი **S**. იპოვე ყველაზე გრძელი ქვესტრიქონი,
**რომელშიც არცერთი სიმბოლო არ მეორდება**.

**შეყვანა:** სტრიქონი S
**გამოტანა:** მაქსიმალური სიგრძე""",
    description_en="""## Longest Unique Substring

Given string **S**. Find the length of the longest substring
**with all distinct characters**.

**Input:** String S
**Output:** Maximum length""",
    test_cases=json.dumps([
        {"input":"abcabcbb","output":"3"},
        {"input":"bbbbb","output":"1"},
        {"input":"pwwkew","output":"3"},
        {"input":"abcdefgh","output":"8","hidden":True},
    ]), time_limit=2.0, memory_limit=256
),
# ══════════ HARD ══════════
dict(
    title_ka="ყველაზე გრძელი საერთო ქვემიმდევრობა", title_en="Longest Common Subsequence",
    difficulty="hard", xp=150, category_ka="დინამიური პროგრამირება", category_en="DP",
    description_ka="""## ყველაზე გრძელი საერთო ქვემიმდევრობა (LCS)

ორი სტრიქონი **A** და **B**. იპოვე მათი **LCS**-ის სიგრძე.
ქვემიმდევრობა — სიმბოლოები ერთი თანმიმდევრობით, მაგრამ არ არის აუცილებელი მეზობლები იყვნენ.

**შეყვანა:** ორი სტრიქონი (სიგრძე ≤ 5000)
**გამოტანა:** LCS-ის სიგრძე""",
    description_en="""## Longest Common Subsequence (LCS)

Two strings **A** and **B**. Find the length of their **LCS**.
A subsequence maintains relative order but doesn't need to be contiguous.

**Input:** Two strings (length ≤ 5000)
**Output:** LCS length""",
    test_cases=json.dumps([
        {"input":"abcde\nace","output":"3","explanation_en":"ace"},
        {"input":"abc\nabc","output":"3"},
        {"input":"abc\ndef","output":"0"},
        {"input":"abcbdab\nbdcaba","output":"4","hidden":True},
    ]), time_limit=5.0, memory_limit=512
),
dict(
    title_ka="უმოკლესი გზა გრაფში", title_en="Shortest Path in Graph",
    difficulty="hard", xp=160, category_ka="გრაფი", category_en="Graph",
    description_ka="""## უმოკლესი გზა გრაფში (Dijkstra)

**n** ქალაქი, **m** ორმხრივი გზა. თითოეულ გზას აქვს წონა.
იპოვე უმოკლესი გზა **1 → n**. თუ გზა არ არსებობს, გამოიტანე **-1**.

**შეყვანა:** n, m; შემდეგ m ხაზი: u v w
**გამოტანა:** მინიმალური მანძილი""",
    description_en="""## Shortest Path in Graph (Dijkstra)

**n** cities, **m** bidirectional roads with weights.
Find the shortest path from **1 to n**. Output **-1** if unreachable.

**Input:** n, m; then m lines: u v w
**Output:** Minimum distance""",
    test_cases=json.dumps([
        {"input":"4 4\n1 2 1\n2 3 2\n3 4 3\n1 4 10","output":"6"},
        {"input":"2 0","output":"-1"},
        {"input":"3 3\n1 2 5\n2 3 3\n1 3 9","output":"8","hidden":True},
    ]), time_limit=3.0, memory_limit=512
),
dict(
    title_ka="ზურგჩანთის ამოცანა", title_en="0/1 Knapsack",
    difficulty="hard", xp=155, category_ka="დინამიური პროგრამირება", category_en="DP",
    description_ka="""## ზურგჩანთის ამოცანა (0/1 Knapsack)

ზურგჩანთის ტევადობა **W**. **n** ნივთი (წონა wᵢ, ღირებულება vᵢ).
შეარჩიე ნივთები: **წონა ≤ W**, **ღირებულება მაქსიმალური**.

**შეყვანა:** n, W; შემდეგ n ხაზი: wᵢ vᵢ
**გამოტანა:** მაქსიმალური ღირებულება""",
    description_en="""## 0/1 Knapsack

Knapsack capacity **W**. **n** items (weight wᵢ, value vᵢ).
Select items: **total weight ≤ W**, **maximize total value**.

**Input:** n, W; then n lines: wᵢ vᵢ
**Output:** Maximum value""",
    test_cases=json.dumps([
        {"input":"3 4\n1 1\n3 4\n4 5","output":"5"},
        {"input":"4 5\n1 2\n2 3\n3 4\n4 5","output":"7"},
        {"input":"1 0\n1 100","output":"0","hidden":True},
        {"input":"3 10\n5 10\n4 40\n3 30","output":"70","hidden":True},
    ]), time_limit=3.0, memory_limit=512
),
dict(
    title_ka="Range Sum Query", title_en="Range Sum Query",
    difficulty="hard", xp=165, category_ka="მონაცემთა სტრუქტურები", category_en="Data Structures",
    description_ka="""## Range Sum Query (Segment Tree)

**n** რიცხვის მასივი. q ოპერაცია:
- `1 i x` — i-ური ელემენტი გახდეს x
- `2 l r` — [l, r] დიაპაზონის ჯამი

**შეყვანა:** n, მასივი, q, q ოპერაცია
**გამოტანა:** "2" ტიპის პასუხები""",
    description_en="""## Range Sum Query (Segment Tree)

Array of **n** numbers. q operations:
- `1 i x` — set element at index i to x
- `2 l r` — sum of elements in range [l, r]

**Input:** n, array, q, q operations
**Output:** Answers to type "2" queries""",
    test_cases=json.dumps([
        {"input":"5\n1 2 3 4 5\n3\n2 1 3\n1 2 10\n2 1 5","output":"6\n22"},
        {"input":"3\n1 1 1\n2\n2 1 3\n2 2 2","output":"3\n1"},
        {"input":"4\n4 3 2 1\n2\n1 1 10\n2 1 4","output":"16","hidden":True},
    ]), time_limit=3.0, memory_limit=512
),
dict(
    title_ka="მაქსიმალური ნაკადი", title_en="Maximum Flow",
    difficulty="hard", xp=180, category_ka="გრაფი", category_en="Graph",
    description_ka="""## მაქსიმალური ნაკადი (Max Flow)

მიმართული გრაფი — წყალსადენი სისტემა. თითოეულ წიბოს აქვს გამტარუნარიანობა.
იპოვე მაქსიმალური ნაკადი **Source (1) → Sink (n)**.

**შეყვანა:** n, m; შემდეგ m ხაზი: u v c
**გამოტანა:** მაქსიმალური ნაკადი""",
    description_en="""## Maximum Flow

A directed graph representing a pipeline. Each edge has capacity.
Find maximum flow from **Source (1) to Sink (n)**.

**Input:** n, m; then m lines: u v c
**Output:** Maximum flow""",
    test_cases=json.dumps([
        {"input":"4 5\n1 2 3\n1 3 2\n2 4 2\n3 4 2\n2 3 1","output":"4"},
        {"input":"2 1\n1 2 5","output":"5"},
        {"input":"3 3\n1 2 10\n2 3 5\n1 3 7","output":"12","hidden":True},
    ]), time_limit=5.0, memory_limit=512
),
dict(
    title_ka="მინიმალური დამფარავი ხე", title_en="Minimum Spanning Tree",
    difficulty="hard", xp=170, category_ka="გრაფი", category_en="Graph",
    description_ka="""## მინიმალური დამფარავი ხე (MST)

**n** კუნძული. ყველა კუნძული უნდა დაუკავშირდეს.
იპოვე **მინიმალური ჯამური ხარჯი** ხიდების ასაშენებლად.

**შეყვანა:** n, m; შემდეგ m ხაზი: u v w
**გამოტანა:** MST-ის ჯამური ღირებულება""",
    description_en="""## Minimum Spanning Tree (Kruskal/Prim)

**n** islands. All must be connected.
Find the **minimum total cost** to build bridges.

**Input:** n, m; then m lines: u v w
**Output:** Total MST cost""",
    test_cases=json.dumps([
        {"input":"4 6\n1 2 1\n1 3 3\n1 4 4\n2 3 2\n2 4 3\n3 4 1","output":"4"},
        {"input":"2 1\n1 2 5","output":"5"},
        {"input":"3 3\n1 2 1\n2 3 2\n1 3 4","output":"3","hidden":True},
    ]), time_limit=3.0, memory_limit=512
),
dict(
    title_ka="პალინდრომული დანაწილება", title_en="Palindrome Partitioning",
    difficulty="hard", xp=160, category_ka="დინამიური პროგრამირება", category_en="DP",
    description_ka="""## პალინდრომული დანაწილება

სტრიქონი **S**. იპოვე **მინიმალური ჭრების** რაოდენობა,
რომ ყველა ნაწილი იყოს პალინდრომი.

**შეყვანა:** სტრიქონი S (სიგრძე ≤ 2000)
**გამოტანა:** მინიმალური ჭრები""",
    description_en="""## Palindrome Partitioning

String **S**. Find the minimum number of **cuts** so that
every part is a palindrome.

**Input:** String S (length ≤ 2000)
**Output:** Minimum cuts""",
    test_cases=json.dumps([
        {"input":"aab","output":"1","explanation_en":"aa|b"},
        {"input":"a","output":"0"},
        {"input":"ab","output":"1"},
        {"input":"ababbbabbababa","output":"3","hidden":True},
    ]), time_limit=5.0, memory_limit=512
),
dict(
    title_ka="მოგზაური გამყიდველი (TSP)", title_en="Travelling Salesman (TSP)",
    difficulty="hard", xp=200, category_ka="დინამიური პროგრამირება", category_en="DP",
    description_ka="""## მოგზაური გამყიდველი (TSP — Bitmask DP)

გამყიდველმა უნდა მოინახულოს **n** ქალაქი ზუსტად ერთხელ
და დაბრუნდეს საწყის ქალაქში (0). იპოვე **მინიმალური მარშრუტი**.

**შეყვანა:** n (≤ 20), შემდეგ n×n მატრიცა
**გამოტანა:** მინიმალური მანძილი""",
    description_en="""## Travelling Salesman (TSP — Bitmask DP)

A salesman must visit **n** cities exactly once
and return to the start (city 0). Find the **minimum route**.

**Input:** n (≤ 20), then n×n distance matrix
**Output:** Minimum distance""",
    test_cases=json.dumps([
        {"input":"4\n0 10 15 20\n10 0 35 25\n15 35 0 30\n20 25 30 0","output":"80"},
        {"input":"2\n0 5\n5 0","output":"10"},
        {"input":"3\n0 1 2\n1 0 3\n2 3 0","output":"6","hidden":True},
    ]), time_limit=10.0, memory_limit=512
),
dict(
    title_ka="მაქსიმალური XOR ქვემასი", title_en="Maximum XOR Subarray",
    difficulty="hard", xp=175, category_ka="ბიტების მანიპულაცია", category_en="Bit Manipulation",
    description_ka="""## მაქსიმალური XOR ქვემასი

**n** რიცხვის მასივი. იპოვე უწყვეტი ქვემასი,
რომლის ელემენტების **XOR ჯამი მაქსიმალურია**.

**შეყვანა:** n, შემდეგ n რიცხვი
**გამოტანა:** მაქსიმალური XOR""",
    description_en="""## Maximum XOR Subarray

Array of **n** numbers. Find the contiguous subarray
whose **XOR sum is maximum**.

**Input:** n, then n numbers
**Output:** Maximum XOR value""",
    test_cases=json.dumps([
        {"input":"4\n1 2 3 4","output":"7"},
        {"input":"3\n8 1 2","output":"11"},
        {"input":"5\n3 8 2 6 5","output":"15","hidden":True},
    ]), time_limit=3.0, memory_limit=512
),
dict(
    title_ka="მატრიცების გამრავლების ჯაჭვი", title_en="Matrix Chain Multiplication",
    difficulty="hard", xp=185, category_ka="დინამიური პროგრამირება", category_en="DP",
    description_ka="""## მატრიცების გამრავლების ჯაჭვი

**n** მატრიცა. M₁ ზომა p₀×p₁, M₂ ზომა p₁×p₂...
იპოვე ფრჩხილების ისეთი დასმა, რომ **სკალარული გამრავლებების**
რაოდენობა **მინიმალური** იყოს.

**შეყვანა:** n+1 რიცხვი (განზომილებები)
**გამოტანა:** ოპერაციების მინიმალური რაოდენობა""",
    description_en="""## Matrix Chain Multiplication

**n** matrices. M₁ is p₀×p₁, M₂ is p₁×p₂...
Find the optimal parenthesization that **minimizes
the number of scalar multiplications**.

**Input:** n+1 numbers (dimensions)
**Output:** Minimum number of operations""",
    test_cases=json.dumps([
        {"input":"4\n10 30 5 60","output":"4500"},
        {"input":"3\n2 3 4","output":"24"},
        {"input":"2\n10 20","output":"0"},
        {"input":"5\n5 10 3 12 5","output":"405","hidden":True},
    ]), time_limit=5.0, memory_limit=512
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
                title_ka       = t["title_ka"],
                title_en       = t["title_en"],
                difficulty     = t["difficulty"],
                xp             = t["xp"],
                category_ka    = t.get("category_ka"),
                category_en    = t.get("category_en"),
                description_ka = t.get("description_ka"),
                description_en = t.get("description_en"),
                test_cases     = t.get("test_cases"),
                time_limit     = t.get("time_limit", 2.0),
                memory_limit   = t.get("memory_limit", 256),
            )
            db.session.add(task)
        db.session.commit()
        print(f"✅ {len(TASKS)} tasks seeded successfully.")

if __name__ == "__main__":
    seed()