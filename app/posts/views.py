from . import post_bp
from flask import render_template, flash, redirect, url_for, session, request, abort
from app import db
from app.posts.models import Post, Tag
from app.posts.forms import PostForm
from app.models import User


@post_bp.route('/')
def all_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("all_posts.html", posts=posts, title_tag="Усі пости")


@post_bp.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()

    users = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(u.id, u.username) for u in users]

    tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(t.id, t.name) for t in tags]

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data
        )

        selected_tags = []
        for tag_id in form.tags.data:
            tag_obj = db.session.get(Tag, tag_id)
            if tag_obj:
                selected_tags.append(tag_obj)
        new_post.tags = selected_tags

        db.session.add(new_post)
        db.session.commit()

        flash(f"Пост '{new_post.title}' успішно додано!", 'success')
        return redirect(url_for('posts.all_posts'))

    return render_template("add_post.html", form=form, title_tag="Створити новий пост")


@post_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    users = db.session.scalars(db.select(User)).all()
    form.author_id.choices = [(u.id, u.username) for u in users]

    tags = db.session.scalars(db.select(Tag)).all()
    form.tags.choices = [(t.id, t.name) for t in tags]

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [t.id for t in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        post.posted = form.publish_date.data

        selected_tags = []
        for tag_id in form.tags.data:
            tag_obj = db.session.get(Tag, tag_id)
            if tag_obj:
                selected_tags.append(tag_obj)
        post.tags = selected_tags

        db.session.commit()
        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template(
        "add_post.html",
        form=form,
        title_tag="Редагувати пост"
    )


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for('posts.all_posts'))
    return render_template("delete_confirm.html", post=post)