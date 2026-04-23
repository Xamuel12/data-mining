import os
from flask import Flask, render_template, redirect, url_for, request, flash, Response

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from sklearn.cluster import KMeans

app = Flask(__name__)

# Configuration for Online Database (Postgres) or local SQLite
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
database_url = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        occupation = request.form.get('occupation')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, age=int(
            age), occupation=occupation, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Login failed. Check your credentials.')
    return render_template('login.html')


@app.route('/data-mining')
@login_required
def data_mining():
    page = request.args.get('page', 1, type=int)
    algorithm = request.args.get('algorithm', 'kmeans')
    per_page = 20

    try:
        dataset_path = 'data/riye_dataset_clean.csv'
        if not os.path.exists(dataset_path):
            return render_template('data_mining.html', error=f"Dataset not found: {dataset_path}")

        df = pd.read_csv(dataset_path)
        df_encoded = pd.get_dummies(df.dropna())

        if df_encoded.empty:
            return render_template('data_mining.html', error="No clean data for analysis")

        # Algorithm selection
        if algorithm == 'kmeans':
            model = KMeans(n_clusters=3, n_init=10, random_state=42)
        elif algorithm == 'dbscan':
            from sklearn.cluster import DBSCAN
            model = DBSCAN(eps=0.5, min_samples=5)
        elif algorithm == 'hierarchical':
            from sklearn.cluster import AgglomerativeClustering
            model = AgglomerativeClustering(n_clusters=3)
        else:
            model = KMeans(n_clusters=3, n_init=10, random_state=42)

        clusters = model.fit_predict(df_encoded)
        df['Cluster'] = clusters

        # Cluster stats
        cluster_counts = df['Cluster'].value_counts().sort_index().to_dict()

        # Pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_df = df.iloc[start_idx:end_idx]
        data_html = paginated_df.to_html(
            classes='table table-striped', escape=False)

        total_pages = (len(df) + per_page - 1) // per_page

        return render_template('data_mining.html',
                               data=data_html,
                               result=f"{algorithm.upper()} clustering complete. Total rows: {len(df)}",
                               cluster_stats=cluster_counts,
                               total_rows=len(df),
                               page=page,
                               total_pages=total_pages,
                               algorithm=algorithm,
                               algorithms=['kmeans', 'dbscan', 'hierarchical'])
    except Exception as e:
        return render_template('data_mining.html', error=str(e))


@app.route('/download-clustered')
@login_required
def download_clustered():
    try:
        dataset_path = 'data/riye_dataset_clean.csv'
        if not os.path.exists(dataset_path):
            flash('Dataset file not found.')
            return redirect(url_for('data_mining'))
        df = pd.read_csv(dataset_path)
        df_encoded = pd.get_dummies(df.dropna())
        if df_encoded.empty:
            flash('No clean data available for clustering.')
            return redirect(url_for('data_mining'))
        kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
        df['Cluster'] = kmeans.fit_predict(df_encoded)
        csv = df.to_csv(index=False)
        return Response(csv, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=clustered_cultural_data.csv'})
    except Exception as e:
        flash(f'Download failed: {str(e)}')
        return redirect(url_for('data_mining'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Initialize database tables on import (for Vercel serverless)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
