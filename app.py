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
        from datetime import datetime as _dt
        def now_fn(): return _dt.utcnow()
        return dict(t=t, lang=lang, now_fn=now_fn)

    # Register blueprints
    from routes.main      import main_bp
    from routes.auth      import auth_bp
    from routes.tasks     import tasks_bp
    from routes.ratings   import ratings_bp
    from routes.olympiad  import olympiad_bp
    from routes.dashboard import dashboard_bp
    from routes.about     import about_bp
    from routes.help      import help_bp
    from routes.admin     import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,       url_prefix="/auth")
    app.register_blueprint(tasks_bp,      url_prefix="/tasks")
    app.register_blueprint(ratings_bp,    url_prefix="/ratings")
    app.register_blueprint(olympiad_bp,   url_prefix="/olympiad")
    app.register_blueprint(dashboard_bp,  url_prefix="/dashboard")
    app.register_blueprint(about_bp,      url_prefix="/about")
    app.register_blueprint(help_bp,       url_prefix="/help")
    app.register_blueprint(admin_bp,      url_prefix="/admin")

    with app.app_context():
        db.create_all()
        _seed_initial_data()

    return app


def _seed_initial_data():
    from models import Task, Badge, News

    if not Badge.query.first():
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
        db.session.add_all(badges)
        db.session.commit()

    if not News.query.first():
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        # Unsplash images — tech/coding themed, stable URLs
        IMGS = [
            "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",  # circuit board
            "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&q=80",  # coding screen
            "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80",  # trophy/award
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80",  # python code
            "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&q=80",  # leaderboard/team
            "https://images.unsplash.com/photo-1506765515384-028b60a970df?w=800&q=80",  # streak/fire
            "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800&q=80",  # javascript
            "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=800&q=80",  # partnership
            "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&q=80",  # cpp/java laptop
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80",  # milestone/team
            "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&q=80",  # bugfix
            "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&q=80",  # code sharing
        ]
        news_items = [
            News(title_ka="CodeMama პლატფორმა ოფიციალურად გაიხსნა!",
                 title_en="CodeMama Platform is Officially Launched!",
                 body_ka="სიამაყით გვაქვს პლატფორმის გახსნის გამოცხადება. CodeMama არის ქართული საგანმანათლებლო სივრცე პროგრამისტებისთვის, სადაც შეგიძლიათ გაიუმჯობესოთ კოდინგის უნარები ინტერაქტიური გამოწვევებით და ოლიმპიადებით.",
                 body_en="We are proud to announce the launch of our platform. CodeMama is a Georgian educational space for programmers where you can improve coding skills through interactive challenges and olympiads.",
                 category_ka="გამოცხადება", category_en="Announcement", emoji="🚀",
                 image_url=IMGS[0], created_at=now - timedelta(days=1)),
            News(title_ka="მარტის ოლიმპიადა — რეგისტრაცია დაიწყო",
                 title_en="March Olympiad — Registration is Open",
                 body_ka="მარტის კოდინგის ოლიმპიადაზე რეგისტრაცია გახსნილია! შეჯიბრება გაიმართება 3–10 მარტს. გამარჯვებული მიიღებს MacBook Pro-ს, მეორე ადგილი — iPad-ს.",
                 body_en="Registration for the March coding olympiad is now open! Competition runs March 3–10. 1st place wins a MacBook Pro, 2nd place an iPad.",
                 category_ka="ოლიმპიადა", category_en="Olympiad", emoji="🏆",
                 image_url=IMGS[1], created_at=now - timedelta(days=2)),
            News(title_ka="ახალი ბეჯები: Bug Hunter და Night Owl",
                 title_en="New Badges: Bug Hunter and Night Owl",
                 body_ka="დაემატა ახალი ბეჯები. Bug Hunter — კოდში შეცდომის პოვნისას. Night Owl — შუაღამისა და 6 საათის შუალედში სისტემაში შესვლისას.",
                 body_en="New badges added. Bug Hunter — for finding bugs in code. Night Owl — for logging in between midnight and 6 AM.",
                 category_ka="განახლება", category_en="Update", emoji="🎖️",
                 image_url=IMGS[2], created_at=now - timedelta(days=4)),
            News(title_ka="Python კურსი — 15 ახალი ტასკი",
                 title_en="Python Course — 15 New Tasks",
                 body_ka="Python-ის სექციაში დაემატა 15 ახალი ტასკი. Fibonacci Sequence, Palindrome Check, Dynamic Programming სერია. ყოველი ამოხსნა XP-ს გამოიმუშავებს.",
                 body_en="15 new tasks added to the Python section: Fibonacci Sequence, Palindrome Check, Dynamic Programming series. Each solve earns XP.",
                 category_ka="კურსი", category_en="Course", emoji="🐍",
                 image_url=IMGS[3], created_at=now - timedelta(days=6)),
            News(title_ka="ლიდერბორდი განახლდა — ახალი Top 10",
                 title_en="Leaderboard Updated — New Top 10",
                 body_ka="ამ კვირის ლიდერბორდი განახლდა. Top 3: ნიკა ბ. (12,400 XP), მარიამ კ. (10,800 XP), გიორგი მ. (9,200 XP).",
                 body_en="This week's leaderboard updated. Top 3: Nika B. (12,400 XP), Mariam K. (10,800 XP), Giorgi M. (9,200 XP).",
                 category_ka="რეიტინგი", category_en="Ratings", emoji="📊",
                 image_url=IMGS[4], created_at=now - timedelta(days=8)),
            News(title_ka="Daily Streak — როგორ მუშაობს",
                 title_en="Daily Streak — How it Works",
                 body_ka="ყოველ დღე ერთი ტასკის ამოხსნა ზრდის Streak-ს. 7 დღე = '7 Day Warrior', 30 დღე = 'On Fire' ბეჯი.",
                 body_en="Solving one task every day increases your Streak. 7 days = '7 Day Warrior', 30 days = 'On Fire' badge.",
                 category_ka="სიახლე", category_en="News", emoji="🔥",
                 image_url=IMGS[5], created_at=now - timedelta(days=10)),
            News(title_ka="JavaScript ამოცანები — ახლა ხელმისაწვდომია",
                 title_en="JavaScript Tasks — Now Available",
                 body_ka="JavaScript-ის ამოცანები ახლა ხელმისაწვდომია: Closure-ები, Promises, Async/Await და სხვა.",
                 body_en="JavaScript tasks are now available: Closures, Promises, Async/Await and more.",
                 category_ka="განახლება", category_en="Update", emoji="💛",
                 image_url=IMGS[6], created_at=now - timedelta(days=12)),
            News(title_ka="CodeMama პარტნიორობა TBC-სთან",
                 title_en="CodeMama Partnership with TBC",
                 body_ka="ვაცხადებთ პარტნიორობას TBC-სთან. ტოპ მომხმარებლებს შეუძლიათ მიიწვიონ TBC Tech-ის გასაუბრებაზე.",
                 body_en="We announce a partnership with TBC. Top users may be invited to interview at TBC Tech.",
                 category_ka="პარტნიორობა", category_en="Partnership", emoji="🤝",
                 image_url=IMGS[7], created_at=now - timedelta(days=15)),
            News(title_ka="C++ და Java — ბეტა ვერსია გახსნილია",
                 title_en="C++ and Java — Beta Version Open",
                 body_ka="C++ და Java-ს ამოცანები ბეტა რეჟიმში ხელმისაწვდომია. შეცდომის შემჩნევისას გვაცნობეთ.",
                 body_en="C++ and Java tasks are available in beta. Please report any bugs you find.",
                 category_ka="ბეტა", category_en="Beta", emoji="⚙️",
                 image_url=IMGS[8], created_at=now - timedelta(days=18)),
            News(title_ka="18,000 რეგისტრირებული მომხმარებელი!",
                 title_en="18,000 Registered Users!",
                 body_ka="CodeMama-ზე 18,000 მომხმარებელია! ამ მილსტოუნის აღსანიშნავად ყველა მიიღებს 200 ბონუს XP-ს.",
                 body_en="CodeMama has reached 18,000 users! To celebrate, every user receives 200 bonus XP.",
                 category_ka="მილსტოუნი", category_en="Milestone", emoji="🎉",
                 image_url=IMGS[9], created_at=now - timedelta(days=20)),
            News(title_ka="ლოგინის ბაგი დაფიქსირდა",
                 title_en="Login Bug Resolved",
                 body_ka="გამოსწორდა ლოგინის პრობლემა. გთხოვთ, ნებისმიერი სხვა პრობლემა მოგვახსენოთ.",
                 body_en="The login issue has been fixed. Please report any other problems.",
                 category_ka="ბაგფიქსი", category_en="Bugfix", emoji="🔧",
                 image_url=IMGS[10], created_at=now - timedelta(days=22)),
            News(title_ka="ახალი ფუნქცია: კოდის გაზიარება",
                 title_en="New Feature: Code Sharing",
                 body_ka="ახლა შეგიძლიათ გაუზიაროთ ამოხსნა სხვებს. გაზიარების ღილაკი გამოჩნდება ამოხსნის შემდეგ.",
                 body_en="You can now share your solution with others. A share button appears after a successful submission.",
                 category_ka="ფუნქცია", category_en="Feature", emoji="📤",
                 image_url=IMGS[11], created_at=now - timedelta(days=25)),
        ]
        db.session.add_all(news_items)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)