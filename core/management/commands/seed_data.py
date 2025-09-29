"""
Django management command to seed the database with sample data for development and testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import User, JobAdvert, JobApplication, Skill, Category, JobAdvertSkill, JobAdvertCategory

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with sample data for development and testing'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database with sample data...')

        # Create superuser
        self.create_superuser()

        # Create users
        users = self.create_users()

        # Create skills
        skills = self.create_skills()

        # Create categories
        categories = self.create_categories()

        # Create job adverts
        jobs = self.create_job_adverts(users, skills, categories)

        # Create job applications
        self.create_job_applications(users, jobs)

        self.stdout.write(self.style.SUCCESS('✅ Database seeded successfully!'))
        self.stdout.write('🔑 Admin credentials: admin / admin123')
        self.stdout.write('👥 Sample users created with passwords matching usernames')

    def create_superuser(self):
        """Create superuser"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('👑 Superuser "admin" created')
        else:
            self.stdout.write('👑 Superuser "admin" already exists')

    def create_users(self):
        """Create extensive sample users"""
        users_data = [
            # Job Seekers
            {
                'username': 'john_doe',
                'email': 'john.doe@example.com',
                'password': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'job_seeker',
                'bio': 'Experienced Python developer with 5 years of experience in web development, machine learning, and data analysis.',
                'location': 'San Francisco, CA',
                'website': 'https://johndoe.dev',
                'phone_number': '+1-555-0123'
            },
            {
                'username': 'sarah_smith',
                'email': 'sarah.smith@example.com',
                'password': 'sarah_smith',
                'first_name': 'Sarah',
                'last_name': 'Smith',
                'user_type': 'job_seeker',
                'bio': 'Full-stack developer passionate about React and Django. Love building scalable web applications.',
                'location': 'New York, NY',
                'website': 'https://sarahsmith.tech',
                'phone_number': '+1-555-0124'
            },
            {
                'username': 'mike_johnson',
                'email': 'mike.johnson@example.com',
                'password': 'mike_johnson',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'user_type': 'job_seeker',
                'bio': 'DevOps engineer with expertise in AWS, Docker, and Kubernetes. Passionate about automation and scalability.',
                'location': 'Austin, TX',
                'website': 'https://mikejohnson.io',
                'phone_number': '+1-555-0125'
            },
            {
                'username': 'emily_davis',
                'email': 'emily.davis@example.com',
                'password': 'emily_davis',
                'first_name': 'Emily',
                'last_name': 'Davis',
                'user_type': 'job_seeker',
                'bio': 'UI/UX designer with 4 years of experience. Expert in Figma, Adobe Creative Suite, and user research.',
                'location': 'Los Angeles, CA',
                'website': 'https://emilydavis.design',
                'phone_number': '+1-555-0126'
            },
            {
                'username': 'alex_wilson',
                'email': 'alex.wilson@example.com',
                'password': 'alex_wilson',
                'first_name': 'Alex',
                'last_name': 'Wilson',
                'user_type': 'job_seeker',
                'bio': 'Data scientist specializing in machine learning and predictive analytics. PhD in Computer Science.',
                'location': 'Boston, MA',
                'website': 'https://alexwilson.ai',
                'phone_number': '+1-555-0127'
            },
            {
                'username': 'lisa_brown',
                'email': 'lisa.brown@example.com',
                'password': 'lisa_brown',
                'first_name': 'Lisa',
                'last_name': 'Brown',
                'user_type': 'job_seeker',
                'bio': 'Mobile app developer with expertise in React Native and Flutter. Love creating beautiful mobile experiences.',
                'location': 'Miami, FL',
                'website': 'https://lisabrown.dev',
                'phone_number': '+1-555-0128'
            },
            {
                'username': 'david_miller',
                'email': 'david.miller@example.com',
                'password': 'david_miller',
                'first_name': 'David',
                'last_name': 'Miller',
                'user_type': 'job_seeker',
                'bio': 'Cybersecurity specialist with 6 years of experience in penetration testing and security auditing.',
                'location': 'Washington, DC',
                'website': 'https://davidmiller.security',
                'phone_number': '+1-555-0129'
            },
            {
                'username': 'anna_garcia',
                'email': 'anna.garcia@example.com',
                'password': 'anna_garcia',
                'first_name': 'Anna',
                'last_name': 'Garcia',
                'user_type': 'job_seeker',
                'bio': 'Product manager with background in software engineering. Passionate about building products that users love.',
                'location': 'Denver, CO',
                'website': 'https://annagarcia.pm',
                'phone_number': '+1-555-0130'
            },

            # Employers
            {
                'username': 'tech_corp',
                'email': 'hr@techcorp.com',
                'password': 'tech_corp',
                'user_type': 'employer',
                'company_name': 'TechCorp Inc.',
                'location': 'Austin, TX',
                'bio': 'Leading technology company specializing in AI and machine learning solutions. 500+ employees worldwide.',
                'website': 'https://techcorp.com',
                'phone_number': '+1-555-0200'
            },
            {
                'username': 'startup_ai',
                'email': 'careers@startup.ai',
                'password': 'startup_ai',
                'user_type': 'employer',
                'company_name': 'Startup.ai',
                'location': 'Seattle, WA',
                'bio': 'Fast-growing startup building the future of AI-powered applications. Series A funded.',
                'website': 'https://startup.ai',
                'phone_number': '+1-555-0201'
            },
            {
                'username': 'dev_agency',
                'email': 'jobs@devagency.com',
                'password': 'dev_agency',
                'user_type': 'employer',
                'company_name': 'DevAgency',
                'location': 'Remote',
                'bio': 'Professional software development and consulting services. 50+ developers worldwide.',
                'website': 'https://devagency.com',
                'phone_number': '+1-555-0202'
            },
            {
                'username': 'fintech_solutions',
                'email': 'careers@fintechsolutions.com',
                'password': 'fintech_solutions',
                'user_type': 'employer',
                'company_name': 'FinTech Solutions',
                'location': 'New York, NY',
                'bio': 'Leading fintech company revolutionizing digital banking and payment solutions.',
                'website': 'https://fintechsolutions.com',
                'phone_number': '+1-555-0203'
            },
            {
                'username': 'healthcare_ai',
                'email': 'hr@healthcareai.com',
                'password': 'healthcare_ai',
                'user_type': 'employer',
                'company_name': 'Healthcare AI Corp',
                'location': 'San Diego, CA',
                'bio': 'AI-powered healthcare solutions improving patient outcomes and medical research.',
                'website': 'https://healthcareai.com',
                'phone_number': '+1-555-0204'
            },
            {
                'username': 'ecommerce_plus',
                'email': 'jobs@ecommerceplus.com',
                'password': 'ecommerce_plus',
                'user_type': 'employer',
                'company_name': 'Ecommerce Plus',
                'location': 'Chicago, IL',
                'bio': 'Next-generation e-commerce platform with advanced analytics and AI recommendations.',
                'website': 'https://ecommerceplus.com',
                'phone_number': '+1-555-0205'
            },
            {
                'username': 'green_energy_tech',
                'email': 'careers@greenenergy.tech',
                'password': 'green_energy_tech',
                'user_type': 'employer',
                'company_name': 'Green Energy Tech',
                'location': 'Portland, OR',
                'bio': 'Sustainable technology company developing renewable energy solutions.',
                'website': 'https://greenenergy.tech',
                'phone_number': '+1-555-0206'
            },
            {
                'username': 'cybersecurity_pro',
                'email': 'hr@cybersecuritypro.com',
                'password': 'cybersecurity_pro',
                'user_type': 'employer',
                'company_name': 'Cybersecurity Pro',
                'location': 'Atlanta, GA',
                'bio': 'Enterprise cybersecurity solutions protecting businesses from digital threats.',
                'website': 'https://cybersecuritypro.com',
                'phone_number': '+1-555-0207'
            }
        ]

        users = []
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(**user_data)
                users.append(user)
                self.stdout.write(f'👤 Created user: {user.username} ({user.get_user_type_display()})')
            else:
                user = User.objects.get(username=user_data['username'])
                users.append(user)
                self.stdout.write(f'👤 User {user.username} already exists')

        return users

    def create_skills(self):
        """Create extensive sample skills"""
        skills_data = [
            # Programming Languages
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby',
            'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB',

            # Web Frameworks
            'Django', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'FastAPI', 'Flask',
            'Spring Boot', 'Laravel', 'ASP.NET', 'Next.js', 'Nuxt.js', 'Svelte',

            # Databases
            'PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Elasticsearch', 'SQLite', 'Oracle',
            'SQL Server', 'Cassandra', 'DynamoDB', 'InfluxDB', 'Neo4j',

            # Cloud & DevOps
            'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins',
            'GitHub Actions', 'GitLab CI', 'CircleCI', 'Ansible', 'Chef', 'Puppet',

            # Data & AI
            'Machine Learning', 'Deep Learning', 'Data Science', 'TensorFlow', 'PyTorch',
            'Pandas', 'NumPy', 'Scikit-learn', 'Apache Spark', 'Hadoop', 'Kafka', 'Airflow',

            # Mobile & Frontend
            'React Native', 'Flutter', 'Ionic', 'Xamarin', 'HTML5', 'CSS3', 'Sass', 'Less',
            'Tailwind CSS', 'Bootstrap', 'Material-UI', 'Ant Design',

            # Testing & Quality
            'Selenium', 'Cypress', 'Jest', 'Mocha', 'Chai', 'pytest', 'unittest', 'JUnit',
            'TestNG', 'Postman', 'SoapUI', 'Load Testing',

            # Methodologies
            'Agile', 'Scrum', 'Kanban', 'Waterfall', 'DevOps', 'CI/CD', 'TDD', 'BDD',
            'Microservices', 'Serverless', 'REST APIs', 'GraphQL', 'gRPC',

            # Security
            'Penetration Testing', 'Vulnerability Assessment', 'OWASP', 'SSL/TLS',
            'OAuth', 'JWT', 'SAML', 'PKI', 'Cryptography',

            # Business & Soft Skills
            'Project Management', 'Product Management', 'Business Analysis', 'System Analysis',
            'Technical Writing', 'Public Speaking', 'Leadership', 'Team Management',
            'Client Relations', 'Negotiation', 'Problem Solving'
        ]

        skills = []
        for skill_name in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_name,
                defaults={'description': f'Professional proficiency in {skill_name}'}
            )
            skills.append(skill)
            if created:
                self.stdout.write(f'🛠️ Created skill: {skill.name}')
            else:
                self.stdout.write(f'🛠️ Skill {skill.name} already exists')

        return skills

    def create_categories(self):
        """Create extensive sample categories"""
        categories_data = [
            {'name': 'Software Development', 'description': 'Software engineering and development roles'},
            {'name': 'Data Science & Analytics', 'description': 'Data analysis, machine learning, and AI positions'},
            {'name': 'DevOps & Infrastructure', 'description': 'Infrastructure, deployment, and operations engineering'},
            {'name': 'UI/UX Design', 'description': 'User interface and user experience design roles'},
            {'name': 'Product Management', 'description': 'Product strategy and management positions'},
            {'name': 'Quality Assurance', 'description': 'Testing and quality assurance roles'},
            {'name': 'Mobile Development', 'description': 'iOS, Android, and cross-platform mobile development'},
            {'name': 'Cybersecurity', 'description': 'Information security and cybersecurity positions'},
            {'name': 'Cloud Computing', 'description': 'Cloud architecture and cloud-native development'},
            {'name': 'Database Administration', 'description': 'Database design, optimization, and administration'},
            {'name': 'Systems Administration', 'description': 'System administration and IT operations'},
            {'name': 'Business Intelligence', 'description': 'Business intelligence and data visualization'},
            {'name': 'Technical Writing', 'description': 'Technical documentation and content creation'},
            {'name': 'Sales Engineering', 'description': 'Technical sales and solutions engineering'},
            {'name': 'Customer Success', 'description': 'Customer support and success management'},
            {'name': 'Human Resources', 'description': 'HR and talent acquisition roles'},
            {'name': 'Finance Technology', 'description': 'Financial technology and fintech positions'},
            {'name': 'Healthcare Technology', 'description': 'Health tech and medical software development'},
            {'name': 'E-commerce', 'description': 'E-commerce platform development and management'},
            {'name': 'Gaming', 'description': 'Game development and interactive entertainment'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'📁 Created category: {category.name}')
            else:
                self.stdout.write(f'📁 Category {category.name} already exists')

        return categories

    def create_job_adverts(self, users, skills, categories):
        """Create sample job adverts"""
        # Get employer users
        employers = [user for user in users if user.user_type == 'employer']

        jobs_data = [
            # TechCorp Jobs
            {
                'employer': employers[0],  # tech_corp
                'title': 'Senior Python Developer',
                'description': 'We are looking for a Senior Python Developer to join our growing team. You will be working on scalable web applications using Django, FastAPI, and modern Python frameworks.',
                'requirements': '4+ years Python, Django ORM, PostgreSQL, Git, Docker, AWS',
                'location': 'San Francisco, CA (Hybrid)',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 120000,
                'salary_max': 160000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 245,
                'applications_count': 12,
                'skills': ['Python', 'Django', 'PostgreSQL', 'REST APIs', 'Git', 'Docker', 'AWS'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[0],
                'title': 'React Frontend Developer',
                'description': 'Join our frontend team to build beautiful, responsive user interfaces using React and TypeScript.',
                'requirements': '3+ years React, TypeScript, CSS3, responsive design',
                'location': 'Austin, TX',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 90000,
                'salary_max': 120000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 167,
                'applications_count': 8,
                'skills': ['React', 'TypeScript', 'CSS3', 'JavaScript', 'HTML5'],
                'categories': ['Software Development', 'UI/UX Design']
            },
            {
                'employer': employers[0],
                'title': 'Data Scientist',
                'description': 'Work with large datasets to extract insights and build predictive models using machine learning.',
                'requirements': 'PhD/MS in Data Science, Python, TensorFlow, scikit-learn, SQL',
                'location': 'Boston, MA',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 140000,
                'salary_max': 180000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 134,
                'applications_count': 6,
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'SQL'],
                'categories': ['Data Science & Analytics']
            },

            # Startup.ai Jobs
            {
                'employer': employers[1],  # startup_ai
                'title': 'Full-Stack Developer',
                'description': 'Join our AI startup and work on cutting-edge applications that leverage machine learning and web technologies.',
                'requirements': '3+ years full-stack, React, Node.js, MongoDB, Docker',
                'location': 'Remote',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 100000,
                'salary_max': 130000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 189,
                'applications_count': 8,
                'skills': ['React', 'Node.js', 'MongoDB', 'REST APIs', 'Docker', 'AWS'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[1],
                'title': 'Machine Learning Engineer',
                'description': 'Build and deploy machine learning models that power our AI-driven products and services.',
                'requirements': '3+ years ML experience, Python, TensorFlow/PyTorch, MLOps',
                'location': 'Seattle, WA',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 130000,
                'salary_max': 170000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 156,
                'applications_count': 9,
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'Docker'],
                'categories': ['Data Science & Analytics']
            },
            {
                'employer': employers[1],
                'title': 'Product Manager',
                'description': 'Drive product strategy and roadmap for our AI-powered platform.',
                'requirements': '3+ years product management, technical background preferred',
                'location': 'Remote',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 110000,
                'salary_max': 140000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 98,
                'applications_count': 12,
                'skills': ['Product Management', 'Agile', 'Data Analysis', 'Leadership'],
                'categories': ['Product Management']
            },

            # DevAgency Jobs
            {
                'employer': employers[2],  # dev_agency
                'title': 'Junior Frontend Developer',
                'description': 'Great opportunity to work on diverse client projects and grow your skills in modern web development.',
                'requirements': '1-2 years frontend, React, JavaScript, HTML5, CSS3',
                'location': 'Austin, TX',
                'job_type': 'full_time',
                'experience_level': 'entry',
                'salary_min': 60000,
                'salary_max': 75000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 156,
                'applications_count': 23,
                'skills': ['React', 'JavaScript', 'HTML5', 'CSS3', 'TypeScript'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[2],
                'title': 'Senior Backend Developer',
                'description': 'Lead backend development for enterprise clients using cutting-edge technologies.',
                'requirements': '5+ years backend development, Node.js/Python, microservices',
                'location': 'Remote',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 130000,
                'salary_max': 170000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 145,
                'applications_count': 7,
                'skills': ['Node.js', 'Python', 'PostgreSQL', 'Microservices', 'Docker'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[2],
                'title': 'UI/UX Designer',
                'description': 'Create beautiful and intuitive user experiences for web and mobile applications.',
                'requirements': '3+ years design experience, Figma, Adobe Creative Suite',
                'location': 'Los Angeles, CA',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 80000,
                'salary_max': 110000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 123,
                'applications_count': 15,
                'skills': ['Figma', 'Adobe Creative Suite', 'Prototyping', 'User Research'],
                'categories': ['UI/UX Design']
            },

            # FinTech Solutions Jobs
            {
                'employer': employers[3],  # fintech_solutions
                'title': 'Blockchain Developer',
                'description': 'Develop decentralized finance applications using blockchain technology.',
                'requirements': '3+ years blockchain development, Solidity, Web3.js, DeFi protocols',
                'location': 'New York, NY',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 140000,
                'salary_max': 180000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 201,
                'applications_count': 11,
                'skills': ['Solidity', 'Web3.js', 'Ethereum', 'Smart Contracts', 'DeFi'],
                'categories': ['Software Development', 'Finance Technology']
            },
            {
                'employer': employers[3],
                'title': 'Security Engineer',
                'description': 'Ensure the security of our financial platforms and protect against cyber threats.',
                'requirements': '4+ years cybersecurity, penetration testing, compliance frameworks',
                'location': 'New York, NY (Hybrid)',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 150000,
                'salary_max': 190000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 178,
                'applications_count': 8,
                'skills': ['Penetration Testing', 'OWASP', 'Cryptography', 'Compliance', 'Python'],
                'categories': ['Cybersecurity']
            },

            # Healthcare AI Jobs
            {
                'employer': employers[4],  # healthcare_ai
                'title': 'Medical Data Analyst',
                'description': 'Analyze healthcare data to improve patient outcomes and medical research.',
                'requirements': 'MS in Health Informatics, Python, R, SQL, HIPAA compliance',
                'location': 'San Diego, CA',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 90000,
                'salary_max': 120000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 134,
                'applications_count': 9,
                'skills': ['Python', 'R', 'SQL', 'Healthcare Analytics', 'HIPAA'],
                'categories': ['Data Science & Analytics', 'Healthcare Technology']
            },
            {
                'employer': employers[4],
                'title': 'Healthcare Software Engineer',
                'description': 'Build software solutions that improve healthcare delivery and patient care.',
                'requirements': '4+ years software development, healthcare domain knowledge preferred',
                'location': 'San Diego, CA (Hybrid)',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 130000,
                'salary_max': 160000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 156,
                'applications_count': 6,
                'skills': ['Python', 'Django', 'React', 'Healthcare IT', 'HL7'],
                'categories': ['Software Development', 'Healthcare Technology']
            },

            # Ecommerce Plus Jobs
            {
                'employer': employers[5],  # ecommerce_plus
                'title': 'E-commerce Backend Developer',
                'description': 'Build scalable e-commerce platforms with advanced features and analytics.',
                'requirements': '4+ years backend development, e-commerce experience, payment processing',
                'location': 'Chicago, IL',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 120000,
                'salary_max': 150000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 189,
                'applications_count': 14,
                'skills': ['Python', 'PostgreSQL', 'Redis', 'Payment Processing', 'Microservices'],
                'categories': ['Software Development', 'E-commerce']
            },
            {
                'employer': employers[5],
                'title': 'Performance Marketing Manager',
                'description': 'Drive growth through data-driven marketing campaigns and analytics.',
                'requirements': '3+ years performance marketing, Google Ads, Facebook Ads, analytics',
                'location': 'Remote',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 80000,
                'salary_max': 110000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 145,
                'applications_count': 18,
                'skills': ['Google Ads', 'Facebook Ads', 'Analytics', 'A/B Testing', 'SEO'],
                'categories': ['Marketing']
            },

            # Green Energy Tech Jobs
            {
                'employer': employers[6],  # green_energy_tech
                'title': 'IoT Solutions Architect',
                'description': 'Design and implement IoT solutions for renewable energy systems.',
                'requirements': '5+ years IoT development, embedded systems, sensor networks',
                'location': 'Portland, OR',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 140000,
                'salary_max': 180000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 123,
                'applications_count': 7,
                'skills': ['IoT', 'Embedded Systems', 'Python', 'C++', 'MQTT'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[6],
                'title': 'Sustainability Data Analyst',
                'description': 'Analyze environmental data to optimize renewable energy production.',
                'requirements': '3+ years data analysis, environmental science background preferred',
                'location': 'Portland, OR (Hybrid)',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 85000,
                'salary_max': 115000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 98,
                'applications_count': 11,
                'skills': ['Python', 'Data Analysis', 'Environmental Science', 'SQL', 'Tableau'],
                'categories': ['Data Science & Analytics']
            },

            # Cybersecurity Pro Jobs
            {
                'employer': employers[7],  # cybersecurity_pro
                'title': 'Senior Security Consultant',
                'description': 'Provide cybersecurity consulting services to enterprise clients.',
                'requirements': '7+ years cybersecurity, CISSP certification, client-facing experience',
                'location': 'Atlanta, GA',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 160000,
                'salary_max': 200000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 167,
                'applications_count': 9,
                'skills': ['Penetration Testing', 'CISSP', 'Risk Assessment', 'Compliance', 'Leadership'],
                'categories': ['Cybersecurity']
            },
            {
                'employer': employers[7],
                'title': 'SOC Analyst',
                'description': 'Monitor and respond to security incidents in our Security Operations Center.',
                'requirements': '2+ years SOC experience, SIEM tools, incident response',
                'location': 'Atlanta, GA (Shift Work)',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 90000,
                'salary_max': 120000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 134,
                'applications_count': 16,
                'skills': ['SIEM', 'Incident Response', 'Python', 'Network Security', 'Linux'],
                'categories': ['Cybersecurity']
            },

            # Additional Diverse Jobs
            {
                'employer': employers[3],  # fintech_solutions
                'title': 'Mobile App Developer',
                'description': 'Develop innovative mobile banking applications for iOS and Android platforms.',
                'requirements': '3+ years mobile development, React Native or Flutter, financial services experience',
                'location': 'New York, NY',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 110000,
                'salary_max': 140000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 178,
                'applications_count': 13,
                'skills': ['React Native', 'Swift', 'Kotlin', 'Mobile Development', 'REST APIs'],
                'categories': ['Mobile Development', 'Finance Technology']
            },
            {
                'employer': employers[4],  # healthcare_ai
                'title': 'Clinical Informatics Specialist',
                'description': 'Bridge the gap between clinical practice and information technology in healthcare.',
                'requirements': 'Clinical background + IT experience, EHR systems, healthcare regulations',
                'location': 'San Diego, CA',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 95000,
                'salary_max': 125000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 145,
                'applications_count': 8,
                'skills': ['EHR Systems', 'Healthcare IT', 'Data Analysis', 'Clinical Research'],
                'categories': ['Healthcare Technology', 'Data Science & Analytics']
            },
            {
                'employer': employers[5],  # ecommerce_plus
                'title': 'Customer Experience Designer',
                'description': 'Design exceptional customer journeys for our e-commerce platform.',
                'requirements': '4+ years UX design, e-commerce experience, customer research',
                'location': 'Chicago, IL (Hybrid)',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 100000,
                'salary_max': 130000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 156,
                'applications_count': 12,
                'skills': ['UX Design', 'Customer Research', 'Prototyping', 'Analytics', 'A/B Testing'],
                'categories': ['UI/UX Design', 'E-commerce']
            },
            {
                'employer': employers[6],  # green_energy_tech
                'title': 'Renewable Energy Software Engineer',
                'description': 'Develop software for monitoring and optimizing renewable energy systems.',
                'requirements': '3+ years software development, IoT experience, C++/Python, real-time systems',
                'location': 'Portland, OR',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'salary_min': 105000,
                'salary_max': 135000,
                'salary_currency': 'USD',
                'is_remote': False,
                'is_active': True,
                'views_count': 123,
                'applications_count': 9,
                'skills': ['Python', 'C++', 'IoT', 'Real-time Systems', 'PostgreSQL'],
                'categories': ['Software Development']
            },
            {
                'employer': employers[7],  # cybersecurity_pro
                'title': 'Threat Intelligence Analyst',
                'description': 'Research and analyze cyber threats to protect our clients from emerging risks.',
                'requirements': '4+ years threat intelligence, OSINT, threat hunting, report writing',
                'location': 'Remote',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'salary_min': 120000,
                'salary_max': 150000,
                'salary_currency': 'USD',
                'is_remote': True,
                'is_active': True,
                'views_count': 145,
                'applications_count': 7,
                'skills': ['Threat Intelligence', 'OSINT', 'Python', 'Report Writing', 'Malware Analysis'],
                'categories': ['Cybersecurity']
            }
        ]

        jobs = []

        # Convert skill/category names to objects
        skill_dict = {skill.name: skill for skill in skills}
        category_dict = {cat.name: cat for cat in categories}

        for job_data in jobs_data:
            job_skills = job_data.pop('skills')
            job_categories = job_data.pop('categories')

            # Set default deadline if not provided
            if 'application_deadline' not in job_data:
                job_data['application_deadline'] = timezone.now().date() + timedelta(days=30)

            job, created = JobAdvert.objects.get_or_create(
                title=job_data['title'],
                employer=job_data['employer'],
                defaults=job_data
            )

            jobs.append(job)
            if created:
                # Add skills and categories
                for skill_name in job_skills:
                    if skill_name in skill_dict:
                        JobAdvertSkill.objects.create(
                            job_advert=job,
                            skill=skill_dict[skill_name],
                            importance_level=4
                        )

                for cat_name in job_categories:
                    if cat_name in category_dict:
                        JobAdvertCategory.objects.create(
                            job_advert=job,
                            category=category_dict[cat_name]
                        )

                self.stdout.write(f'💼 Created job: {job.title} at {job.employer.company_name}')
            else:
                self.stdout.write(f'💼 Job {job.title} already exists')

        return jobs

    def create_job_applications(self, users, jobs):
        """Create sample job applications"""
        # Get job seeker users
        job_seekers = [user for user in users if user.user_type == 'job_seeker']

        applications_data = [
            {
                'job_seeker': job_seekers[0],  # john_doe
                'job_advert': jobs[0],  # Senior Python Developer
                'cover_letter': '''
                Dear Hiring Manager,

                I am writing to express my interest in the Senior Python Developer position at TechCorp Inc.
                With over 5 years of experience in Python development and Django frameworks, I am confident
                in my ability to contribute effectively to your team.

                In my current role, I have successfully delivered multiple large-scale web applications using
                Django REST Framework and PostgreSQL. I have strong experience with API design, database
                optimization, and agile development practices.

                I am particularly drawn to TechCorp's innovative approach and the opportunity to work on
                cutting-edge AI solutions. I am excited about the possibility of bringing my technical expertise
                and passion for quality code to your organization.

                Thank you for considering my application. I look forward to the opportunity to discuss how
                my skills and experience can contribute to TechCorp's continued success.

                Best regards,
                John Doe
                ''',
                'status': 'pending'
            },
            {
                'job_seeker': job_seekers[1],  # sarah_smith
                'job_advert': jobs[1],  # Full-Stack Developer
                'cover_letter': '''
                Hello Startup.ai Team,

                I am thrilled to apply for the Full-Stack Developer position at Startup.ai. As someone who is
                deeply passionate about both frontend and backend development, I am excited by your mission
                to build the future of AI-powered applications.

                My background includes extensive experience with React and Node.js, which aligns perfectly
                with the technical requirements of this role. I have successfully developed and deployed
                multiple full-stack applications, including those with real-time features and complex state management.

                What particularly attracts me to Startup.ai is the opportunity to work at the intersection
                of web development and artificial intelligence. I am eager to contribute my skills in React
                development while learning about AI integration and deployment.

                I am confident that my technical expertise, combined with my enthusiasm for innovative
                technologies, would make me a valuable addition to your team.

                Looking forward to discussing how I can contribute to Startup.ai's mission.

                Best regards,
                Sarah Smith
                ''',
                'status': 'reviewed'
            },
            {
                'job_seeker': job_seekers[0],  # john_doe
                'job_advert': jobs[2],  # Junior Frontend Developer
                'cover_letter': '''
                Dear DevAgency Team,

                I am applying for the Junior Frontend Developer position at DevAgency. While my primary
                background is in backend development, I have been expanding my frontend skills and am
                eager to grow further in this area.

                Recently, I have been working on several React projects and have gained proficiency in
                modern JavaScript, CSS frameworks, and responsive design principles. I understand that
                this is a junior-level position and am enthusiastic about the opportunity to learn from
                your experienced team.

                I believe that my strong foundation in JavaScript and programming concepts, combined with
                my growing frontend skills, make me a good fit for this role. I am committed to continuous
                learning and am excited about the chance to work on diverse projects.

                Thank you for considering my application. I would welcome the opportunity to discuss how
                my background and enthusiasm can contribute to DevAgency's projects.

                Best regards,
                John Doe
                ''',
                'status': 'interview'
            }
        ]

        for app_data in applications_data:
            job_seeker = app_data['job_seeker']
            job_advert = app_data['job_advert']

            # Check if application already exists
            if not JobApplication.objects.filter(
                job_seeker=job_seeker,
                job_advert=job_advert
            ).exists():
                JobApplication.objects.create(**app_data)
                self.stdout.write(f'📄 Created application: {job_seeker.username} → {job_advert.title}')
            else:
                self.stdout.write(f'📄 Application {job_seeker.username} → {job_advert.title} already exists')
