from django.core.management.base import BaseCommand
from core.models import Profile, SkillCategory, Skill, Project, Experience, Education
from datetime import date


class Command(BaseCommand):
    help = "Loads sample data for the portfolio"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        profile = Profile.objects.create(
            name="Madhini Ganesh Reddy",
            title="Data Analyst & Machine Learning Engineer",
            tagline="Transforming data into actionable insights with Python, ML, and predictive analytics",
            about="""Data Analyst and Machine Learning Engineer with strong expertise in Python, SQL, and predictive modeling. Experienced in building ETL pipelines, developing RESTful APIs using Flask, and creating interactive dashboards in Power BI. Proven ability to improve model performance by 15% and optimize data workflows by 35%. Skilled in delivering scalable solutions and actionable insights from complex datasets.""",
            email="madhini@email.com",
            linkedin="https://linkedin.com/in/madhini-ganesh-reddy",
            github="https://github.com/Madhiniganeshreddy123",
        )
        self.stdout.write(self.style.SUCCESS(f"Created profile: {profile.name}"))

        categories_data = [
            {
                "name": "Programming",
                "skills": [
                    {"name": "Python", "icon": "fab fa-python", "proficiency": 95},
                    {"name": "SQL", "icon": "fas fa-database", "proficiency": 90},
                    {"name": "Flask", "icon": "fas fa-flask", "proficiency": 85},
                ],
            },
            {
                "name": "Machine Learning",
                "skills": [
                    {"name": "Scikit-learn", "icon": "fas fa-cogs", "proficiency": 90},
                    {"name": "TensorFlow", "icon": "fas fa-brain", "proficiency": 80},
                    {
                        "name": "NLP (NLTK)",
                        "icon": "fas fa-language",
                        "proficiency": 85,
                    },
                    {"name": "Random Forest", "icon": "fas fa-tree", "proficiency": 85},
                    {"name": "LSTM", "icon": "fas fa-network-wired", "proficiency": 75},
                ],
            },
            {
                "name": "Data Analysis",
                "skills": [
                    {"name": "Pandas", "icon": "fas fa-table", "proficiency": 95},
                    {"name": "NumPy", "icon": "fas fa-calculator", "proficiency": 90},
                    {"name": "EDA", "icon": "fas fa-search", "proficiency": 90},
                    {
                        "name": "Statistical Analysis",
                        "icon": "fas fa-chart-bar",
                        "proficiency": 85,
                    },
                ],
            },
            {
                "name": "Visualization & Tools",
                "skills": [
                    {
                        "name": "Power BI",
                        "icon": "fas fa-chart-line",
                        "proficiency": 90,
                    },
                    {"name": "Tableau", "icon": "fas fa-chart-pie", "proficiency": 80},
                    {
                        "name": "Matplotlib",
                        "icon": "fas fa-chart-area",
                        "proficiency": 85,
                    },
                    {
                        "name": "Seaborn",
                        "icon": "fas fa-wave-square",
                        "proficiency": 80,
                    },
                    {"name": "Git/GitHub", "icon": "fab fa-git-alt", "proficiency": 85},
                    {"name": "Jupyter", "icon": "fas fa-Jupyter", "proficiency": 95},
                ],
            },
            {
                "name": "Data Engineering",
                "skills": [
                    {
                        "name": "ETL Pipelines",
                        "icon": "fas fa-pipeline",
                        "proficiency": 85,
                    },
                    {"name": "Power Query", "icon": "fas fa-query", "proficiency": 80},
                    {
                        "name": "Advanced Excel",
                        "icon": "fas fa-file-excel",
                        "proficiency": 90,
                    },
                    {"name": "MySQL", "icon": "fas fa-server", "proficiency": 85},
                    {
                        "name": "PostgreSQL",
                        "icon": "fas fa-database",
                        "proficiency": 80,
                    },
                ],
            },
        ]

        for cat_data in categories_data:
            category = SkillCategory.objects.create(
                name=cat_data["name"], order=categories_data.index(cat_data)
            )
            for skill_data in cat_data["skills"]:
                Skill.objects.create(
                    name=skill_data["name"],
                    icon=skill_data["icon"],
                    proficiency=skill_data["proficiency"],
                    category=category,
                )
            self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))

        projects_data = [
            {
                "title": "Customer Behaviour Analysis",
                "description": "Analyzed 50K+ customer records to identify purchasing trends and behavioral patterns. Reduced ETL processing time by 35% through SQL query optimization. Applied RFM segmentation improving customer engagement by 22%. Built Power BI dashboards for real-time revenue tracking.",
                "tech_stack": "Python, SQL, Power BI, Pandas, RFM Analysis",
                "github_link": "",
                "demo_link": "",
                "is_featured": True,
                "image": "images/dashboard.png",
            },
            {
                "title": "Multimodal Sentiment Analysis",
                "description": "Processed and analyzed 10K+ multimodal data points combining text and audio signals. Achieved 90% F1-score using ensemble ML models. Used NLTK, Transformers, and Librosa for NLP and audio processing.",
                "tech_stack": "Python, NLTK, Transformers, Librosa, Tableau, TensorFlow",
                "github_link": "",
                "demo_link": "",
                "is_featured": True,
                "image": "images/sentiment-analysis.jpeg",
            },
            {
                "title": "Real-Time QR Code System",
                "description": "Built a full-stack QR code generator application using Flask and REST API architecture. Improved QR code generation speed by 40% through backend optimization. Developed analytics dashboard for monitoring.",
                "tech_stack": "Python, Flask, REST API, HTML, CSS, JavaScript",
                "github_link": "",
                "demo_link": "",
                "is_featured": True,
                "image": "images/qr-code.jpeg",
            },
        ]

        for proj_data in projects_data:
            proj, created = Project.objects.update_or_create(
                title=proj_data["title"], defaults=proj_data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} project: {proj.title}"))
        self.stdout.write(
            self.style.SUCCESS(f"Processed {len(projects_data)} projects")
        )

        experiences_data = [
            {
                "title": "AI & Deep Learning Intern",
                "company": "Central Institute of Tools and Designs",
                "location": "Hyderabad, India",
                "start_date": "2025-01-01",
                "end_date": "2025-03-31",
                "is_current": False,
                "description": "Improved ML model accuracy by 15% using advanced feature engineering. Built and validated predictive models achieving 88% accuracy. Automated ETL workflows reducing manual processing by 30%. Developed Power BI dashboards for KPI visualization. Deployed ML models into production using Flask APIs.",
            },
        ]

        for exp_data in experiences_data:
            Experience.objects.create(**exp_data)
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(experiences_data)} experiences")
        )

        education_data = [
            {
                "degree": "B.Tech – Computer Science (AI & ML)",
                "institution": "Brilliant Institute of Engineering & Technology",
                "location": "Hyderabad",
                "start_year": 2021,
                "end_year": 2025,
                "description": "CGPA: 7.38",
            },
        ]

        for edu_data in education_data:
            Education.objects.create(**edu_data)
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(education_data)} education entries")
        )

        self.stdout.write(self.style.SUCCESS("Sample data loaded successfully!"))
