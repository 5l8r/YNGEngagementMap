import pandas as pd
import random
from faker import Faker
import subprocess
import os

# Initialize Faker
fake = Faker()

# Define chapters and their corresponding zip codes
chapters = {
    'YNG Los Angeles': ['90001', '90002', '90003', '90004', '90005', '90006', '90007', '90008', '90009', '90010', '90011', '90012', '90013', '90014', '90015', '90016'],
    'YNG LA Universities': ['90089', '90095', '90024', '90025', '90027', '90028', '90034', '90035', '90036', '90037', '90038', '90039', '90040', '90041', '90042', '90043'],
    'YNG San Francisco': ['94102', '94103', '94104', '94105', '94107', '94108', '94109', '94110', '94111', '94112', '94114', '94115', '94116', '94117', '94118', '94121'],
    'YNG San Diego': ['92101', '92102', '92103', '92104', '92105', '92106', '92107', '92108', '92109', '92110', '92111', '92113', '92114', '92115', '92116', '92117'],
    'YNG Utah': ['84101', '84102', '84103', '84104', '84105', '84106', '84107', '84108', '84109', '84110', '84111', '84112', '84113', '84114', '84115', '84116'],
    'YNG Las Vegas': ['89101', '89102', '89103', '89104', '89105', '89106', '89107', '89108', '89109', '89110', '89111', '89112', '89113', '89114', '89115', '89116'],
    'YNG Seattle': ['98101', '98102', '98103', '98104', '98105', '98106', '98107', '98108', '98109', '98110', '98111', '98112', '98113', '98114', '98115', '98116']
}

# Define email domains
email_domains = ['gmail.com', 'yahoo.com', 'icloud.com', 'outlook.com', 'stanford.edu', 'ucla.edu', 'company.com', 'aol.com', 'mac.com']

# Define interests and industries
interests = [
    'Skiing', 'Rock Climbing', 'Surfing', 'Reading', 'Travelling', 'Cooking', 'Gardening',
    'Photography', 'Painting', 'Music', 'Sports', 'Hiking', 'Gaming', 'Technology', 'Finance'
]

industries = [
    'Automotive', 'Banking', 'Construction', 'Entertainment', 'Financial Services', 
    'Information Technology', 'Legal Services', 'Manufacturing', 'Pharmaceuticals', 
    'Public Sector', 'Real Estate', 'Student'
]

# Function to create a fake email
def create_fake_email(name):
    domain = random.choice(email_domains + [fake.domain_name()])
    return f"{name.replace(' ', '.').lower()}@{domain}"

# Function to create a fake phone number
def create_fake_phone_number():
    return f"+1 (555) {fake.msisdn()[6:9]}-{fake.msisdn()[9:13]}"

# Function to create a fake entry
def create_fake_entry():
    name = fake.name()
    chapter_affiliation = random.choice(list(chapters.keys()))
    zip_code = random.choice(chapters[chapter_affiliation])
    linkedin = f"{name.replace(' ', '').lower()}" if random.random() > 0.2 else 'NP'
    instagram = f"{name.replace(' ', '').lower()}" if random.random() > 0.2 else 'NP'
    phone_number = create_fake_phone_number() if random.random() > 0.2 else 'NP'
    email = create_fake_email(name)
    linkedin_public = random.choice(['yes', 'no']) if linkedin != 'NP' else 'NP'
    instagram_public = random.choice(['yes', 'no']) if instagram != 'NP' else 'NP'
    phone_public = random.choice(['yes', 'no']) if phone_number != 'NP' else 'NP'
    email_public = random.choice(['yes', 'no'])
    member_interests = ', '.join(random.sample(interests, k=random.randint(1, 3)))
    industry = random.choice(industries)
    return [
        name, chapter_affiliation, zip_code, linkedin, instagram, phone_number, email,
        linkedin_public, instagram_public, phone_public, email_public, member_interests, industry
    ]

# Generate fake data
data = [create_fake_entry() for _ in range(500)]  # Generating 500 fake records

# Create a DataFrame
df = pd.DataFrame(data, columns=[
    'Name', 'Chapter Affiliation', 'Zip Code', 'LinkedIn', 'Instagram', 'Phone Number', 'Email',
    'LinkedIn Public', 'Instagram Public', 'Phone Number Public', 'Email Public', 'Interests', 'Industry'
])

# Save to CSV
df.to_csv('data/yng_fake_members.csv', index=False)

print("Fake data generated and saved to 'data/yng_fake_members.csv'.")

# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
geocode_script_path = os.path.join(current_dir, 'geocode_data.py')

# Execute the geocode_data.py script and capture output and errors
try:
    result = subprocess.run(["python", geocode_script_path], check=True, capture_output=True, text=True)
    print("geocode_data.py executed successfully.")
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error executing geocode_data.py.")
    print("Output:", e.stdout)
    print("Error:", e.stderr)
