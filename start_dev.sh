#!/bin/bash
# ALX Project Nexus - Development Setup Script

echo "🚀 Starting ALX Project Nexus Development Environment"

# Function to start local RabbitMQ with management UI
start_rabbitmq_local() {
    echo "🐰 Starting local RabbitMQ with management UI..."
    echo "📍 RabbitMQ Management UI: http://localhost:15672 (admin/admin123)"
    echo "💡 This may require Docker to be installed locally"

    # Check if Docker is available
    if command -v docker &> /dev/null; then
        docker compose --profile postgres-local --profile rabbitmq-local up -d db-local rabbitmq-local redis
        echo "✅ PostgreSQL, RabbitMQ and Redis started with Docker"
        sleep 10  # Wait longer for services to start (PostgreSQL takes time)
    else
        echo "❌ Docker not found. Please install Docker to run services locally."
        echo "💡 Alternatively, run 'docker compose --profile postgres-local --profile rabbitmq-local up -d db-local rabbitmq-local redis'"
        exit 1
    fi
}

# Check if RabbitMQ is requested
if [[ "$1" == "--rabbitmq" ]] || [[ "$1" == "-r" ]]; then
    start_rabbitmq_local
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check Django installation
python3 -c "import django; print(f'✅ Django {django.get_version()} installed')" 2>/dev/null || {
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    pip install -r requirements.dev.txt
}

# Run Django checks
echo "🔍 Running Django system checks..."
python3 manage.py check

# Run migrations
echo "🗄️ Running database migrations..."
python3 manage.py migrate

# Create superuser if needed
echo "👤 Checking for superuser..."
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists') if User.objects.filter(is_superuser=True).exists() else print('No superuser found')" 2>/dev/null || {
    echo "👤 No superuser found. Creating one..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin user already exists')" | python3 manage.py shell
}

# Show service URLs
echo ""
echo "🌟 ALX Project Nexus Ready!"
echo "📍 API: http://localhost:8000"
echo "� API Docs: http://localhost:8000/api/docs/"
echo "⚙️ Admin Panel: http://localhost:8000/admin/"
if [[ "$1" == "--rabbitmq" ]] || [[ "$1" == "-r" ]]; then
    echo "🐰 RabbitMQ Management: http://localhost:15673 (admin/admin123)"
    echo "🔄 Redis: localhost:6379"
fi
echo ""
echo "🔑 Superuser: admin / admin123"
echo ""
echo "💡 To run Celery worker (requires local RabbitMQ):"
echo "   source venv/bin/activate && celery -A app worker -l info"
echo ""
echo "💡 To run with local RabbitMQ: ./start_dev.sh --rabbitmq"

# Add explicit configurations
export SECURE_SSL_REDIRECT=False
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False

python3 manage.py runserver --insecure 0.0.0.0:8000
