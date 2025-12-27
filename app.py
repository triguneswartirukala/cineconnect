import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "cineconnect_secret_key"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= HELPERS =================
def get_unread_notifications():
    if "user_id" not in session:
        return 0
    conn = get_db()
    count = conn.execute(
        "SELECT COUNT(*) FROM notifications WHERE user_id=? AND seen=0",
        (session["user_id"],)
    ).fetchone()[0]
    conn.close()
    return count

def is_following(a, b):
    conn = get_db()
    r = conn.execute(
        "SELECT 1 FROM followers WHERE follower_id=? AND following_id=?",
        (a, b)
    ).fetchone()
    conn.close()
    return r is not None

# ================= AUTH =================
@app.route("/")
def index():
    return redirect("/feed") if "user_id" in session else redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/feed")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
                (
                    request.form["email"],
                    request.form["username"],
                    request.form["password"],
                    request.form["role"]
                )
            )
            conn.commit()
        except:
            pass
        conn.close()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ================= FEED (PRIVATE) =================
@app.route("/feed", methods=["GET", "POST"])
def feed():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    if request.method == "POST":
        content = request.form.get("content")
        media = request.files.get("media")
        filename = None
        if media and media.filename:
            filename = secure_filename(media.filename)
            media.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        conn.execute(
            "INSERT INTO posts (user_id, content, media) VALUES (?, ?, ?)",
            (session["user_id"], content, filename)
        )
        conn.commit()

    posts = conn.execute("""
        SELECT posts.*, users.username, users.profile_pic
        FROM posts
        JOIN users ON users.id = posts.user_id
        WHERE posts.user_id = ?
           OR posts.user_id IN (
               SELECT following_id FROM followers WHERE follower_id = ?
           )
        ORDER BY posts.id DESC
    """, (session["user_id"], session["user_id"])).fetchall()

    comments = conn.execute("""
        SELECT comments.*, users.username
        FROM comments
        JOIN users ON users.id = comments.user_id
        ORDER BY comments.id ASC
    """).fetchall()

    conn.close()
    return render_template("feed.html", posts=posts, comments=comments, unread_count=get_unread_notifications())

# ================= EXPLORE =================
@app.route("/explore")
def explore():
    if "user_id" not in session:
        return redirect("/login")

    q = request.args.get("q", "")
    conn = get_db()
    users, posts = [], []

    if q:
        users = conn.execute(
            "SELECT username, profile_pic FROM users WHERE username LIKE ?",
            (f"%{q}%",)
        ).fetchall()

        posts = conn.execute("""
            SELECT posts.*, users.username, users.profile_pic
            FROM posts
            JOIN users ON users.id = posts.user_id
            WHERE posts.content LIKE ?
            ORDER BY posts.id DESC
        """, (f"%{q}%",)).fetchall()

    conn.close()
    return render_template("explore.html", users=users, posts=posts, unread_count=get_unread_notifications())

# ================= PROFILE =================
@app.route("/profile")
@app.route("/profile/<username>")
def profile(username=None):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username or session["username"],)
    ).fetchone()

    posts = conn.execute(
        "SELECT * FROM posts WHERE user_id=? ORDER BY id DESC",
        (user["id"],)
    ).fetchall()

    followers = conn.execute(
        "SELECT COUNT(*) FROM followers WHERE following_id=?",
        (user["id"],)
    ).fetchone()[0]

    following = conn.execute(
        "SELECT COUNT(*) FROM followers WHERE follower_id=?",
        (user["id"],)
    ).fetchone()[0]

    is_follow = is_following(session["user_id"], user["id"])
    conn.close()

    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        followers_count=followers,
        following_count=following,
        is_following=is_follow,
        unread_count=get_unread_notifications()
    )

# ================= COMMENTS (THREADS) =================
@app.route("/comment/<int:post_id>", methods=["POST"])
def comment_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    conn.execute("""
        INSERT INTO comments (user_id, post_id, content, parent_id)
        VALUES (?, ?, ?, ?)
    """, (
        session["user_id"],
        post_id,
        request.form["content"],
        request.form.get("parent_id")
    ))

    post = conn.execute("SELECT user_id FROM posts WHERE id=?", (post_id,)).fetchone()
    if post and post["user_id"] != session["user_id"]:
        conn.execute("""
            INSERT INTO notifications (user_id, actor_id, type, post_id, seen)
            VALUES (?, ?, 'comment', ?, 0)
        """, (post["user_id"], session["user_id"], post_id))

    conn.commit()
    conn.close()
    return redirect("/feed")

# ================= LIKE =================
@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    post = conn.execute("SELECT user_id FROM posts WHERE id=?", (post_id,)).fetchone()
    try:
        conn.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)",
                     (session["user_id"], post_id))
        if post and post["user_id"] != session["user_id"]:
            conn.execute("""
                INSERT INTO notifications (user_id, actor_id, type, post_id, seen)
                VALUES (?, ?, 'like', ?, 0)
            """, (post["user_id"], session["user_id"], post_id))
        conn.commit()
    except:
        pass
    conn.close()
    return redirect("/feed")

# ================= FOLLOW =================
@app.route("/follow/<int:user_id>", methods=["POST"])
def follow(user_id):
    if user_id == session.get("user_id"):
        return redirect("/feed")
    conn = get_db()
    try:
        conn.execute("INSERT INTO followers VALUES (?, ?)", (session["user_id"], user_id))
        conn.execute("""
            INSERT INTO notifications (user_id, actor_id, type, post_id, seen)
            VALUES (?, ?, 'follow', NULL, 0)
        """, (user_id, session["user_id"]))
        conn.commit()
    except:
        pass
    conn.close()
    return redirect(request.referrer or "/feed")

@app.route("/unfollow/<int:user_id>", methods=["POST"])
def unfollow(user_id):
    conn = get_db()
    conn.execute("DELETE FROM followers WHERE follower_id=? AND following_id=?",
                 (session["user_id"], user_id))
    conn.commit()
    conn.close()
    return redirect(request.referrer or "/feed")

# ================= NOTIFICATIONS =================
@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    data = conn.execute("""
        SELECT notifications.*, users.username
        FROM notifications
        JOIN users ON users.id = notifications.actor_id
        WHERE notifications.user_id=?
        ORDER BY notifications.id DESC
    """, (session["user_id"],)).fetchall()
    conn.execute("UPDATE notifications SET seen=1 WHERE user_id=?", (session["user_id"],))
    conn.commit()
    conn.close()

    return render_template("notifications.html", notifications=data, unread_count=0)

# ================= CHATS =================
@app.route("/chats")
def chats():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    users = conn.execute("""
        SELECT users.username, users.profile_pic
        FROM followers
        JOIN users ON users.id = followers.following_id
        WHERE followers.follower_id=?
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "chats.html",
        users=users,
        unread_count=get_unread_notifications()
    )


@app.route("/chat/<username>", methods=["GET", "POST"])
def chat(username):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    other = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if not other:
        conn.close()
        return redirect("/chats")

    if request.method == "POST":
        msg = request.form.get("content")
        if msg:
            conn.execute("""
                INSERT INTO messages (sender_id, receiver_id, content)
                VALUES (?, ?, ?)
            """, (session["user_id"], other["id"], msg))
            conn.commit()

    messages = conn.execute("""
        SELECT messages.*, users.username
        FROM messages
        JOIN users ON users.id = messages.sender_id
        WHERE (sender_id=? AND receiver_id=?)
           OR (sender_id=? AND receiver_id=?)
        ORDER BY messages.id ASC
    """, (session["user_id"], other["id"], other["id"], session["user_id"])).fetchall()

    conn.close()

    return render_template(
        "chat.html",
        other=other,
        messages=messages,
        unread_count=get_unread_notifications()
    )

# ================= RUN =================
if __name__ == "__main__":
    

    app.run()
