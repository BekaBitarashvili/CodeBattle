from flask import Flask, session
from extensions import db, login_manager
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "გთხოვთ გაიაროთ ავტორიზაცია."

    # ── Language context processor ──────────────────
    @app.context_processor
    def inject_lang():
        lang = session.get("lang", "ka")
        def t(ka, en=""):
            return ka if lang == "ka" else (en or ka)
        return dict(t=t, lang=lang)

    # Register blueprints
    from routes.main      import main_bp
    from routes.auth      import auth_bp
    from routes.tasks     import tasks_bp
    from routes.ratings   import ratings_bp
    from routes.olympiad  import olympiad_bp
    from routes.dashboard import dashboard_bp
    from routes.about     import about_bp
    from routes.help      import help_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,       url_prefix="/auth")
    app.register_blueprint(tasks_bp,      url_prefix="/tasks")
    app.register_blueprint(ratings_bp,    url_prefix="/ratings")
    app.register_blueprint(olympiad_bp,   url_prefix="/olympiad")
    app.register_blueprint(dashboard_bp,  url_prefix="/dashboard")
    app.register_blueprint(about_bp,      url_prefix="/about")
    app.register_blueprint(help_bp,       url_prefix="/help")

    with app.app_context():
        db.create_all()
        _seed_initial_data()

    return app


def _seed_initial_data():
    from models import Task, Badge, News

    if not Task.query.first():
        tasks = [
            Task(title="Fibonacci Sequence",     difficulty="easy",   xp=30,  description="ააგე ფიბონაჩის მიმდევრობა n წევრამდე."),
            Task(title="Palindrome Check",        difficulty="easy",   xp=25,  description="განსაზღვრე, არის თუ არა სტრინგი პალინდრომი."),
            Task(title="FizzBuzz",                difficulty="easy",   xp=20,  description="კლასიკური FizzBuzz ამოცანა."),
            Task(title="Sum of Array",            difficulty="easy",   xp=25,  description="მასივის ელემენტების ჯამი."),
            Task(title="Reverse String",          difficulty="easy",   xp=20,  description="სტრინგის შებრუნება."),
            Task(title="Binary Search Tree",      difficulty="medium", xp=80,  description="BST-ის კვანძის ჩასმა/ძებნა."),
            Task(title="Graph BFS / DFS",         difficulty="medium", xp=90,  description="გრაფში სიგანე/სიღრმე-პირველი ძებნა."),
            Task(title="Stack with Min",          difficulty="medium", xp=70,  description="Stack, რომელიც O(1)-ში აბრუნებს მინიმუმს."),
            Task(title="LRU Cache",               difficulty="medium", xp=85,  description="LRU Cache-ის იმპლემენტაცია."),
            Task(title="Merge Intervals",         difficulty="medium", xp=75,  description="გადამფარავი ინტერვალების გაერთიანება."),
            Task(title="Dynamic Programming #3",  difficulty="hard",   xp=150, description="Longest Common Subsequence."),
            Task(title="Network Flow",            difficulty="hard",   xp=180, description="Max-Flow Min-Cut თეორემა."),
            Task(title="Segment Tree",            difficulty="hard",   xp=160, description="Segment Tree დიაპაზონური შეკითხვებისთვის."),
            Task(title="Dijkstra + Heap",         difficulty="hard",   xp=170, description="დეიქსტრას ალგორითმი heap-ით."),
            Task(title="Edit Distance DP",        difficulty="hard",   xp=155, description="Levenshtein Distance DP."),
        ]
        badges = [
            Badge(slug="first_blood",  name_ka="პირველი სისხლი",           name_en="First Blood",   emoji="🩸", description_ka="პირველი ამოხსნა",      description_en="First solve"),
            Badge(slug="warrior_7",    name_ka="7 დღის მეომარი",           name_en="7 Day Warrior", emoji="⚔️", description_ka="7 დღე streak",         description_en="7 day streak"),
            Badge(slug="speed_demon",  name_ka="სისწრაფის დემონი",         name_en="Speed Demon",   emoji="⚡", description_ka="< 5 წთ-ში ამოხსნა",   description_en="Solved in < 5 min"),
            Badge(slug="bug_hunter",   name_ka="ბაგ ჰანთერი",             name_en="Bug Hunter",    emoji="🐛", description_ka="პირველი bug-ის პოვნა", description_en="Found first bug"),
            Badge(slug="code_samurai", name_ka="კოდ სამურაი",             name_en="Code Samurai",  emoji="🥷", description_ka="50 ტასკი ამოხსნილი",   description_en="50 tasks solved"),
            Badge(slug="olympiad_win", name_ka="ოლიმპიადის გამარჯვებული", name_en="Olympiad Win",  emoji="🏆", description_ka="I ადგილი ოლიმპიადაში", description_en="1st place olympiad"),
            Badge(slug="night_owl",    name_ka="ღამის ბუ",                 name_en="Night Owl",     emoji="🌙", description_ka="00:00–06:00 შესვლა",   description_en="Login at midnight"),
            Badge(slug="sharpshooter", name_ka="სნაიპერი",                 name_en="Sharpshooter",  emoji="🎯", description_ka="100% სისწრაფე",        description_en="100% accuracy"),
            Badge(slug="top10",        name_ka="ტოპ 10",                   name_en="Top 10",        emoji="🌟", description_ka="ლიდერბორდი Top 10",   description_en="Leaderboard Top 10"),
            Badge(slug="on_fire",      name_ka="ცეცხლზეა",                name_en="On Fire",       emoji="🔥", description_ka="30 დღის streak",       description_en="30 day streak"),
        ]
        db.session.add_all(tasks + badges)
        db.session.commit()

    if not News.query.first():
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        news_items = [
            News(title_ka="CodeQuest პლატფორმა ოფიციალურად გაიხსნა!",
                 title_en="CodeQuest Platform is Officially Launched!",
                 body_ka="სიამაყით გვაქვს პლატფორმის გახსნის გამოცხადება. CodeQuest არის ქართული საგანმანათლებლო სივრცე პროგრამისტებისთვის, სადაც შეგიძლიათ გაიუმჯობესოთ კოდინგის უნარები ინტერაქტიური გამოწვევებით და ოლიმპიადებით.",
                 body_en="We are proud to announce the launch of our platform. CodeQuest is a Georgian educational space for programmers where you can improve coding skills through interactive challenges and olympiads.",
                 category_ka="გამოცხადება", category_en="Announcement", emoji="🚀", created_at=now - timedelta(days=1)),
            News(title_ka="მარტის ოლიმპიადა — რეგისტრაცია დაიწყო",
                 title_en="March Olympiad — Registration is Open",
                 body_ka="მარტის კოდინგის ოლიმპიადაზე რეგისტრაცია გახსნილია! შეჯიბრება გაიმართება 3–10 მარტს. გამარჯვებული მიიღებს MacBook Pro-ს, მეორე ადგილი — iPad-ს.",
                 body_en="Registration for the March coding olympiad is now open! Competition runs March 3–10. 1st place wins a MacBook Pro, 2nd place an iPad.",
                 category_ka="ოლიმპიადა", category_en="Olympiad", emoji="🏆", created_at=now - timedelta(days=2)),
            News(title_ka="ახალი ბეჯები: Bug Hunter და Night Owl",
                 title_en="New Badges: Bug Hunter and Night Owl",
                 body_ka="დაემატა ახალი ბეჯები. Bug Hunter — კოდში შეცდომის პოვნისას. Night Owl — შუაღამისა და 6 საათის შუალედში სისტემაში შესვლისას.",
                 body_en="New badges added. Bug Hunter — for finding bugs in code. Night Owl — for logging in between midnight and 6 AM.",
                 category_ka="განახლება", category_en="Update", emoji="🎖️", created_at=now - timedelta(days=4)),
            News(title_ka="Python კურსი — 15 ახალი ტასკი",
                 title_en="Python Course — 15 New Tasks",
                 body_ka="Python-ის სექციაში დაემატა 15 ახალი ტასკი. Fibonacci Sequence, Palindrome Check, Dynamic Programming სერია. ყოველი ამოხსნა XP-ს გამოიმუშავებს.",
                 body_en="15 new tasks added to the Python section: Fibonacci Sequence, Palindrome Check, Dynamic Programming series. Each solve earns XP.",
                 category_ka="კურსი", category_en="Course", emoji="🐍", created_at=now - timedelta(days=6)),
            News(title_ka="ლიდერბორდი განახლდა — ახალი Top 10",
                 title_en="Leaderboard Updated — New Top 10",
                 body_ka="ამ კვირის ლიდერბორდი განახლდა. Top 3: ნიკა ბ. (12,400 XP), მარიამ კ. (10,800 XP), გიორგი მ. (9,200 XP).",
                 body_en="This week's leaderboard updated. Top 3: Nika B. (12,400 XP), Mariam K. (10,800 XP), Giorgi M. (9,200 XP).",
                 category_ka="რეიტინგი", category_en="Ratings", emoji="📊", created_at=now - timedelta(days=8)),
            News(title_ka="Daily Streak — როგორ მუშაობს",
                 title_en="Daily Streak — How it Works",
                 body_ka="ყოველ დღე ერთი ტასკის ამოხსნა ზრდის Streak-ს. 7 დღე = '7 Day Warrior', 30 დღე = 'On Fire' ბეჯი.",
                 body_en="Solving one task every day increases your Streak. 7 days = '7 Day Warrior', 30 days = 'On Fire' badge.",
                 category_ka="სიახლე", category_en="News", emoji="🔥", created_at=now - timedelta(days=10)),
            News(title_ka="JavaScript ამოცანები — ახლა ხელმისაწვდომია",
                 title_en="JavaScript Tasks — Now Available",
                 body_ka="JavaScript-ის ამოცანები ახლა ხელმისაწვდომია: Closure-ები, Promises, Async/Await და სხვა.",
                 body_en="JavaScript tasks are now available: Closures, Promises, Async/Await and more.",
                 category_ka="განახლება", category_en="Update", emoji="💛", created_at=now - timedelta(days=12)),
            News(title_ka="CodeQuest პარტნიორობა TBC-სთან",
                 title_en="CodeQuest Partnership with TBC",
                 body_ka="ვაცხადებთ პარტნიორობას TBC-სთან. ტოპ მომხმარებლებს შეუძლიათ მიიწვიონ TBC Tech-ის გასაუბრებაზე.",
                 body_en="We announce a partnership with TBC. Top users may be invited to interview at TBC Tech.",
                 category_ka="პარტნიორობა", category_en="Partnership", emoji="🤝", created_at=now - timedelta(days=15)),
            News(title_ka="C++ და Java — ბეტა ვერსია გახსნილია",
                 title_en="C++ and Java — Beta Version Open",
                 body_ka="C++ და Java-ს ამოცანები ბეტა რეჟიმში ხელმისაწვდომია. შეცდომის შემჩნევისას გვაცნობეთ.",
                 body_en="C++ and Java tasks are available in beta. Please report any bugs you find.",
                 category_ka="ბეტა", category_en="Beta", emoji="⚙️", created_at=now - timedelta(days=18)),
            News(title_ka="18,000 რეგისტრირებული მომხმარებელი!",
                 title_en="18,000 Registered Users!",
                 body_ka="CodeQuest-ზე 18,000 მომხმარებელია! ამ მილსტოუნის აღსანიშნავად ყველა მიიღებს 200 ბონუს XP-ს.",
                 body_en="CodeQuest has reached 18,000 users! To celebrate, every user receives 200 bonus XP.",
                 category_ka="მილსტოუნი", category_en="Milestone", emoji="🎉", created_at=now - timedelta(days=20)),
            News(title_ka="ლოგინის ბაგი დაფიქსირდა",
                 title_en="Login Bug Resolved",
                 body_ka="გამოსწორდა ლოგინის პრობლემა. გთხოვთ, ნებისმიერი სხვა პრობლემა მოგვახსენოთ.",
                 body_en="The login issue has been fixed. Please report any other problems.",
                 category_ka="ბაგფიქსი", category_en="Bugfix", emoji="🔧", created_at=now - timedelta(days=22)),
            News(title_ka="ახალი ფუნქცია: კოდის გაზიარება",
                 title_en="New Feature: Code Sharing",
                 body_ka="ახლა შეგიძლიათ გაუზიაროთ ამოხსნა სხვებს. გაზიარების ღილაკი გამოჩნდება ამოხსნის შემდეგ.",
                 body_en="You can now share your solution with others. A share button appears after a successful submission.",
                 category_ka="ფუნქცია", category_en="Feature", emoji="📤", created_at=now - timedelta(days=25)),
        ]
        db.session.add_all(news_items)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
