import os
import sys
from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
import pandas as pd
from sklearn.cluster import KMeans

# Load environment variables from .env file for local development
from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# ENVIRONMENT VARIABLES IMPORT
# =============================================================================
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
PORT = int(os.environ.get('PORT', 5000))

# Detect Vercel / serverless environment
IS_VERCEL = os.environ.get('VERCEL') == '1' or os.path.exists('/vercel')

# Validate required environment variables in production
if FLASK_ENV == 'production':
    if not SECRET_KEY:
        raise ValueError(
            "SECRET_KEY environment variable is required in production. "
            "Please set it in your deployment platform dashboard."
        )

# Use fallbacks for local development
if not SECRET_KEY:
    SECRET_KEY = 'dev-secret-key-change-in-production'
if not DATABASE_URL:
    # On serverless, only /tmp is writable
    if IS_VERCEL:
        DATABASE_URL = 'sqlite:////tmp/users.db'
    else:
        DATABASE_URL = 'sqlite:///users.db'

app = Flask(__name__)

# =============================================================================
# PRODUCTION CONFIGURATION
# =============================================================================
# Secret key - uses environment variable in production, fallback for local dev
app.config['SECRET_KEY'] = SECRET_KEY

# Database configuration - supports PostgreSQL (production) and SQLite (local)
database_url = DATABASE_URL
# Fix for Heroku/Vercel postgres:// vs postgresql://
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Verify connections before using them
    'pool_recycle': 300,    # Recycle connections after 5 minutes
}

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
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        age = request.form.get('age', '').strip()
        occupation = request.form.get('occupation', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate required fields
        if not all([first_name, last_name, age, occupation, username, password]):
            flash('All fields are required!')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html')

        try:
            # Check if username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists!')
                return render_template('signup.html')

            hashed_password = generate_password_hash(password)
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                age=int(age),
                occupation=occupation,
                username=username,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"SIGNUP ERROR: {e}")
            print(traceback.format_exc())
            flash(f'An error occurred while creating your account. Please try again.')
            return render_template('signup.html')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required!')
            return render_template('login.html')

        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Login failed. Check your credentials.')
        except Exception as e:
            import traceback
            print(f"LOGIN ERROR: {e}")
            print(traceback.format_exc())
            flash('An error occurred during login. Please try again.')

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
        import traceback
        print(f"DATA MINING ERROR: {e}")
        print(traceback.format_exc())
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


# =============================================================================
# HEALTH CHECK ENDPOINT (for monitoring)
# =============================================================================
@app.route('/health')
def health_check():
    db_status = 'unknown'
    try:
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    return jsonify({
        'status': 'healthy',
        'service': 'CultureExplore API',
        'database': db_status
    }), 200


# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================
def init_db():
    """Initialize database tables with error handling."""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables initialized successfully.")
    except Exception as e:
        import traceback
        print(f"⚠️ Database initialization warning: {e}")
        print(traceback.format_exc())


# Initialize on import (for serverless environments like Vercel)
init_db()

if __name__ == '__main__':
    debug_mode = FLASK_ENV != 'production'
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode)
